use crate::hashmaps::FxHashMap as HashMap;
use std::iter::zip;

use crate::pyo3_prelude::*;
use num_bigint::BigUint;

use super::{
    algebraic_rewrite::add_make_broadcasts_explicit, prelude::*, Add, Concat, Einsum,
    GeneralFunction, Index,
};
use crate::{
    tensor_util::{TensorAxisIndex, TensorIndex, USlice},
    util::{cumsum, outer_product, AsOp},
};
/// this nests arbitrarily deep
#[pyfunction]
pub fn einsum_pull_concat(einsum: &Einsum) -> Option<CircuitRc> {
    let mut did_anything = false;
    let mut int_sections: HashMap<u8, Vec<usize>> = HashMap::new();
    for (operand, ints) in &einsum.args {
        if let Circuit::Concat(concat) = &***operand
            && let int_here = ints[concat.axis]
            && einsum.out_axes.iter().filter(|z| **z == int_here).count() <= 1 {
            did_anything = true;
            let sections_here = concat.get_sections();
            match int_sections.get(&int_here) {
                None => {
                    int_sections.insert(int_here, sections_here);
                }
                Some(prev) if prev[..] != sections_here[..] => {
                    return None;
                }
                _  => {}
            }
        }
    }
    if !did_anything {
        return None;
    }

    // for each concat dimension that's reduced over, compute einsums seperately for each section and Add at the end
    // when there are multiple, we outer product and flat add

    // for each concat dimension that's kept, einsum seperately for each section and Concat at the end
    // if there are multiple, we outer product and nest concats
    let (int_sections_concat, int_sections_add): (Vec<u8>, _) = int_sections
        .keys()
        .cloned()
        .partition(|i| einsum.out_axes.contains(i));

    fn recurse(
        concat_picks: &HashMap<u8, usize>,
        int_sections_concat_left: &[u8],
        int_sections_add: &Vec<u8>,
        int_sections: &HashMap<u8, Vec<usize>>,
        einsum: &Einsum,
    ) -> CircuitRc {
        if int_sections_concat_left.is_empty() {
            let summands: Vec<CircuitRc> = outer_product(
                &int_sections_add
                    .iter()
                    .map(|i| (0..int_sections[i].len()).collect())
                    .collect::<Vec<_>>(),
            )
            .iter()
            .map(|summand_settings| {
                let einsum_args = einsum
                    .args
                    .iter()
                    .map(|(node, ints)| {
                        let index = TensorIndex(
                            ints.iter()
                                .map(|i| {
                                    if let Some(u) = concat_picks.get(i) {
                                        let sections = &int_sections[i];
                                        let cumsums = cumsum(sections);

                                        return TensorAxisIndex::new_plain_slice(
                                            cumsums[*u],
                                            cumsums[u + 1],
                                        );
                                    }
                                    if let Some(u) = int_sections_add.iter().position(|z| z == i) {
                                        let sections = &int_sections[i];
                                        let cumsums = cumsum(sections);

                                        return TensorAxisIndex::new_plain_slice(
                                            cumsums[summand_settings[u]],
                                            cumsums[summand_settings[u] + 1],
                                        );
                                    }
                                    TensorAxisIndex::IDENT
                                })
                                .collect(),
                        );
                        (
                            Index::try_new(node.clone(), index, None).unwrap().rc(),
                            ints.clone(),
                        )
                    })
                    .collect();

                Einsum::try_new(einsum_args, einsum.out_axes.clone(), einsum.name_cloned())
                    .unwrap()
                    .rc()
            })
            .collect();
            Add::try_new(summands, None).unwrap().rc()
        } else {
            let (ihere, new_int_sections_concat) = int_sections_concat_left.split_first().unwrap();
            let concattands: Vec<CircuitRc> = (0..int_sections[ihere].len())
                .map(|i| {
                    let mut new_picks = concat_picks.clone();
                    new_picks.insert(*ihere, i);
                    recurse(
                        &new_picks,
                        new_int_sections_concat,
                        int_sections_add,
                        int_sections,
                        einsum,
                    )
                })
                .collect();
            Concat::try_new(
                concattands,
                einsum.out_axes.iter().position(|x| x == ihere).unwrap(),
                None,
            )
            .unwrap()
            .rc()
        }
    }

    Some(recurse(
        &HashMap::new(),
        &int_sections_concat,
        &int_sections_add,
        &int_sections,
        einsum,
    ))
}

#[pyfunction]
pub fn add_pull_concat(add: &Add) -> Option<CircuitRc> {
    for (child, rank_difference) in add.nodes_and_rank_differences() {
        if let Circuit::Concat(concat) = &**child {
            if concat.info().shape[concat.axis] != 1 {
                let sections_here = concat.get_sections();
                let concat_axis = rank_difference + concat.axis;
                let add_explicit = add_make_broadcasts_explicit(add)
                    .unwrap_or(add.clone())
                    .rc();
                let concat_of_adds = split_to_concat(add_explicit, concat_axis, sections_here).rc();
                if add.info().shape[..] != concat_of_adds.info().shape[..] {
                    add.clone().rc().compiler_print();
                    concat_of_adds.compiler_print();
                    panic!();
                }
                return Some(concat_of_adds);
                // let concattands = (0..sections_here.len()).map(|i|{
                //     Add::try_new(add_of_concats.nodes.iter().map(|)
                // }).collect();
                // return Some(Concat::try_new(concattands,concat_axis,None).unwrap().rc())
            }
        }
    }
    None
}

// pub fn rearrange_pull_concat(rearrange: &Rearrange) -> Option<Concat> {}
#[pyfunction]
pub fn generalfunction_pull_concat(generalfunction: &GeneralFunction) -> Option<Concat> {
    let batch_rank =
        generalfunction.info().rank() - generalfunction.spec.num_non_batchable_output_dims;
    for operand in &generalfunction.nodes {
        if let Circuit::Concat(concat) = &***operand &&  concat.axis < batch_rank {
            let mut cur = 0;
            let new_operands = concat
                .nodes
                .iter()
                .map(|cnode| {
                    let span_here = cnode.info().shape[concat.axis];
                    let new_operands = zip(
                        &generalfunction.nodes,
                        &generalfunction.spec.input_batchability,
                    )
                    .map(|(node, batchability)| {
                        if !batchability {
                            node.clone()
                        } else if node == operand {
                            cnode.clone()
                        } else {
                            Index::try_new(
                                node.clone(),
                                TensorIndex::new_single(
                                    TensorAxisIndex::new_plain_slice(cur, cur + span_here),
                                    concat.axis,
                                    node.info().rank(),
                                ),
                                None,
                            )
                            .unwrap()
                            .rc()
                        }
                    })
                    .collect();
                    cur += span_here;
                    GeneralFunction::try_new(new_operands, generalfunction.spec.clone(), None)
                        .unwrap()
                        .rc()
                })
                .collect();
            return Some(Concat::try_new(new_operands, concat.axis, None).unwrap());
        }
    }
    None
}

#[pyfunction]
pub fn concat_fuse(concat: &Concat) -> Option<Concat> {
    let mut did_anything = false;
    let new_operands = concat
        .nodes
        .iter()
        .flat_map(|child| {
            if let Circuit::Concat(inner) = &***child && inner.axis == concat.axis {
                did_anything = true;
                inner.nodes.clone()
            } else{
                vec![child.clone()]
            }
        })
        .collect();
    if !did_anything {
        return None;
    }
    Some(Concat::try_new(new_operands, concat.axis, concat.name_cloned()).unwrap())
}

#[pyfunction]
pub fn concat_drop_size_zero(concat: &Concat) -> Option<Concat> {
    let mut did_anything = false;
    let new_nodes = concat
        .nodes
        .iter()
        .filter(|x| {
            if x.info().shape[concat.axis] == 0 {
                did_anything = true;
                false
            } else {
                true
            }
        })
        .cloned()
        .collect();
    if !did_anything {
        return None;
    }
    Some(Concat::try_new(new_nodes, concat.axis, concat.name_cloned()).unwrap())
}

#[pyfunction]
pub fn index_concat_drop_unreached(index: &Index) -> Option<CircuitRc> {
    // canon so we only have to work with positives
    let index_canon = index.index.canonicalize(&index.node.info().shape).0;
    let concat: &Concat = (**index.node).as_op()?;
    if concat
        .nodes
        .iter()
        .any(|x| x.info().numel() == BigUint::from(0usize))
    {
        return None;
    }
    let axis_index = &index_canon[concat.axis];
    let operand_starts: Vec<usize> = cumsum(
        &concat
            .nodes
            .iter()
            .map(|x| x.info().shape[concat.axis])
            .collect::<Vec<_>>(),
    );
    let (new_operands, new_index) = match axis_index {
        TensorAxisIndex::Single(single) => {
            let operand_idx = operand_starts
                .iter()
                .filter(|x| **x <= *single as usize)
                .count()
                - 1;
            (
                vec![concat.nodes[operand_idx].clone()],
                TensorAxisIndex::Single(single - operand_starts[operand_idx] as i64),
            )
        }
        TensorAxisIndex::Slice(slice) => {
            let uslice: Option<USlice> = (*slice).into();
            let uslice = uslice.unwrap();
            let operand_idxs: Vec<usize> = (0..concat.nodes.len())
                .filter(|i| {
                    operand_starts[*i] < uslice.stop && operand_starts[i + 1] > uslice.start
                })
                .collect();
            let start_point = operand_starts[operand_idxs[0]];
            (
                operand_idxs
                    .iter()
                    .map(|x| concat.nodes[*x].clone())
                    .collect(),
                TensorAxisIndex::new_plain_slice(
                    uslice.start - start_point,
                    uslice.stop - start_point,
                ),
            )
        }
        _ => (concat.nodes.clone(), axis_index.clone()),
    };
    if new_operands.len() == concat.nodes.len() {
        return None;
    }
    let mut new_tensor_index = index.index.clone();
    new_tensor_index.0[concat.axis] = new_index;
    Some(
        Index::try_new(
            Concat::try_new(new_operands, concat.axis, concat.name_cloned())
                .unwrap()
                .rc(),
            new_tensor_index,
            index.name_cloned(),
        )
        .unwrap()
        .rc(),
    )
}

#[pyfunction]
pub fn split_to_concat(circuit: CircuitRc, axis: usize, sections: Vec<usize>) -> Concat {
    assert!(axis < circuit.info().rank());
    let starts = cumsum(&sections);
    let operands: Vec<CircuitRc> = (0..sections.len())
        .map(|i| {
            Index::try_new(
                circuit.clone(),
                TensorIndex::new_single(
                    TensorAxisIndex::new_plain_slice(starts[i], starts[i + 1]),
                    axis,
                    circuit.info().rank(),
                ),
                None,
            )
            .unwrap()
            .rc()
        })
        .collect();
    Concat::try_new(operands, axis, None).unwrap()
}

pub fn split_sections(l: usize, sections: usize) -> Vec<usize> {
    let even_size = l / sections;
    let residual = l % sections;
    [
        vec![even_size + 1; residual],
        vec![even_size; sections - residual],
    ]
    .concat()
}

#[test]
fn test_split_sections() {
    dbg!(split_sections(10, 3));
}

// todo: order concats by axis?
