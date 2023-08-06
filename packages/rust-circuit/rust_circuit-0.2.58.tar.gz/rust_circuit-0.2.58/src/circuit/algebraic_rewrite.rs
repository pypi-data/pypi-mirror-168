use crate::{
    circuit::EinsumAxes,
    hashmaps::{AHashSet as HashSet, FxHashMap as HashMap},
};
use std::{
    collections::hash_map::Entry::{self, Vacant},
    iter::zip,
    rc::Rc,
};

use bit_iter::BitIter;
use itertools::Itertools;

use crate::{all_imports::RInts, pyo3_prelude::*, sv, util::BitMask128};

use super::{
    circuit_optimizer::OptimizationContext, computational_node::EinsumArgs, deep_map_op_context,
    evaluate_fn, prelude::*, py_circuit_items::PY_CIRCUIT_ITEMS, Add, Concat, Einsum,
    GeneralFunction, HashBytes, Index, Rearrange, ScalarConstant, Scatter, Symbol,
};
use crate::{
    filter_by_variant,
    opt_einsum::optimize_einsum_spec_cached,
    rearrange_spec::{shape_to_op_shape, RearrangeSpec},
    tensor_util::{
        compose, Shape, Slice, TensorAxisIndex, TensorIndex, TensorInvariantError, USlice,
    },
    union_find::UnionFind,
    unwrap,
    util::{
        filter_out_idx, filter_to_idx, intersection_all, inverse_permutation, is_unique,
        unique_to_appearance, EinInt,
    },
};

#[pyfunction]
pub fn add_flatten_once(add: &Add) -> Option<Add> {
    let mut did_anything = false;
    let new_operands: Vec<CircuitRc> = add
        .nodes
        .iter()
        .flat_map(|node| match &*node.0 {
            Circuit::Add(inner_add) => {
                did_anything = true;
                inner_add.nodes.clone()
            }
            _ => {
                vec![node.clone()]
            }
        })
        .collect();
    if !did_anything {
        return None;
    }
    Some(Add::try_new(new_operands, add.name_cloned()).unwrap())
}

#[pyfunction]
pub fn add_collapse_scalar_inputs(add: &Add) -> Option<Add> {
    let nodes = add.nodes.iter().map(|x| x.0.clone());
    let (scalar_inputs, non_scalar_inputs): (Vec<ScalarConstant>, Vec<Rc<Circuit>>) =
        filter_by_variant!(nodes, Circuit, ScalarConstant, ScalarConstant);
    if scalar_inputs.len() <= 1 {
        None
    } else {
        let new_scalar: f64 = scalar_inputs.iter().map(|node| node.value).sum();
        let mut new_inputs: Vec<CircuitRc> =
            non_scalar_inputs.iter().map(|x| x.clone().into()).collect();
        let new_scalar_input = ScalarConstant::new(new_scalar, add.info().shape.clone(), None).rc();
        new_inputs.push(new_scalar_input);
        Some(Add::try_new(new_inputs, add.name_cloned()).unwrap())
    }
}

#[pyfunction]
pub fn add_elim_zeros(add: &Add) -> Option<Add> {
    let mut did_anything = false;
    let new_operands = add
        .nodes
        .iter()
        .filter_map(|node| match &***node {
            Circuit::ScalarConstant(scalar) => {
                if scalar.value == 0.0 && scalar.info().rank() == 0 {
                    did_anything = true;
                    None
                } else {
                    Some(node.clone())
                }
            }
            _ => Some(node.clone()),
        })
        .collect();
    if !did_anything {
        None
    } else {
        Some(Add::try_new(new_operands, add.name_cloned()).unwrap())
    }
}

#[pyfunction]
pub fn add_deduplicate(add: &Add) -> Option<Add> {
    let mut duplicate_counts: HashMap<HashBytes, i32> = HashMap::new();
    let mut hash_to_node: HashMap<HashBytes, CircuitRc> = HashMap::new();
    for node in add.nodes.iter() {
        *duplicate_counts.entry(node.info().hash).or_insert(0) += 1;
        hash_to_node.insert(node.info().hash, node.clone());
    }
    if duplicate_counts.len() == add.nodes.len() {
        None
    } else {
        let deduped_inputs = hash_to_node
            .iter()
            .map(|(hash, node)| {
                let count = duplicate_counts[hash];
                if count > 1 {
                    Einsum::scalar_mul(node, count as f64, None).rc()
                } else {
                    node.clone()
                }
            })
            .collect();
        Some(Add::try_new(deduped_inputs, add.name_cloned()).unwrap())
    }
}

#[pyfunction]
pub fn remove_add_few_input(add: &Add) -> Option<CircuitRc> {
    if add.nodes.is_empty() {
        Some(ScalarConstant::new(0f64, add.info().shape.clone(), None).rc())
    } else if add.nodes.len() == 1 {
        Some(
            add_make_broadcasts_explicit(add)
                .unwrap_or(add.clone())
                .nodes[0]
                .clone(),
        )
    } else {
        None
    }
}

pub fn make_einsum_ints_same_one_layer(einsum: &Einsum) -> Einsum {
    let mut top_int_map: HashMap<u8, u8> = HashMap::new();
    let mut next_global_int: u8 = 0;
    for i in einsum.axes_in_input() {
        if let Vacant(e) = top_int_map.entry(i) {
            e.insert(next_global_int);
            next_global_int += 1;
        }
    }
    // don't know the number of result ints, so UF for really high amount?
    let mut unionfind = UnionFind::new(300);
    let int_maps: Vec<Option<HashMap<u8, u8>>> = einsum
        .args
        .iter()
        .map(|(node, ints)| match &*node.0 {
            Circuit::Einsum(einsum) => {
                let mut bottom_int_map: HashMap<u8, u8> = HashMap::new();

                for (bottom_int, top_int) in zip(&einsum.out_axes, ints) {
                    if !bottom_int_map.contains_key(bottom_int) {
                        bottom_int_map.insert(*bottom_int, top_int_map[top_int]);
                    } else {
                        unionfind.union(
                            bottom_int_map[bottom_int] as usize,
                            top_int_map[top_int] as usize,
                        )
                    }
                }
                for bottom_int in einsum.axes_in_input() {
                    if let Vacant(e) = bottom_int_map.entry(bottom_int) {
                        e.insert(next_global_int);
                        next_global_int += 1;
                    }
                }
                Some(bottom_int_map)
            }

            _ => None,
        })
        .collect();

    let new_args = zip(&einsum.args, int_maps)
        .map(|((node, ints), int_map_op)| {
            let new_operand_axes = ints
                .iter()
                .map(|x| unionfind.find(top_int_map[x] as usize) as u8)
                .collect();
            match &*node.0 {
                Circuit::Einsum(inner) => {
                    let int_map = int_map_op.unwrap();
                    let new_args_inner = inner
                        .args
                        .iter()
                        .map(|(child, inner_op_ints)| {
                            (
                                child.clone(),
                                inner_op_ints
                                    .iter()
                                    .map(|i| unionfind.find(int_map[i] as usize) as u8)
                                    .collect(),
                            )
                        })
                        .collect();
                    (
                        inner
                            .evolve(
                                Some(new_args_inner),
                                Some(
                                    inner
                                        .out_axes
                                        .iter()
                                        .map(|i| unionfind.find(int_map[i] as usize) as u8)
                                        .collect(),
                                ),
                            )
                            .rc(),
                        new_operand_axes,
                    )
                }
                _ => (node.clone(), new_operand_axes),
            }
        })
        .collect();
    einsum.evolve(
        Some(new_args),
        Some(
            einsum
                .out_axes
                .iter()
                .map(|x| unionfind.find(top_int_map[x] as usize) as u8)
                .collect(),
        ),
    )
}

#[pyfunction]
pub fn einsum_flatten_once(einsum: &Einsum) -> Option<Einsum> {
    if einsum
        .args
        .iter()
        .all(|(node, _ints)| !matches!(&*node.0, Circuit::Einsum(_)))
    {
        return None;
    }
    let with_ints_same = make_einsum_ints_same_one_layer(einsum);
    Some(
        Einsum::try_new(
            with_ints_same
                .args
                .into_iter()
                .flat_map(|(node, ints)| match &*node.0 {
                    Circuit::Einsum(einsum) => einsum.args.clone(),
                    _ => vec![(node, ints)],
                })
                .collect(),
            with_ints_same.out_axes,
            None,
        )
        .unwrap(),
    )
}

/// nests einsum (similar to "rearrange_muls") according to an einops-style path with recycled IDs
#[pyfunction]
pub fn einsum_nest_path(einsum: &Einsum, path: Vec<Vec<usize>>) -> Einsum {
    let mut stack = einsum.args.clone();
    for contraction in path {
        let mut contraction = contraction.clone();
        contraction.sort();
        contraction.reverse();
        let mut args_here = vec![];
        for i in contraction {
            args_here.push(stack.remove(i))
        }
        let outer_indices = {
            if stack.is_empty() {
                einsum.out_axes.clone()
            } else {
                let outer_indices_set: HashSet<EinInt> = stack
                    .iter()
                    .map(|(_node, ints)| ints)
                    .chain(std::iter::once(&einsum.out_axes))
                    .flatten()
                    .copied()
                    .collect();
                let inner_indices_set: HashSet<EinInt> = args_here
                    .iter()
                    .flat_map(|(_node, ints)| ints)
                    .copied()
                    .collect();
                let mut outer_indices: EinsumAxes = inner_indices_set
                    .intersection(&outer_indices_set)
                    .copied()
                    .collect();
                outer_indices.sort();
                outer_indices
            }
        };
        stack.push((
            Einsum::try_new(args_here, outer_indices.clone(), None)
                .unwrap()
                .rc(),
            outer_indices,
        ))
    }
    assert!(stack.len() == 1);
    unwrap!((**stack[0].0).clone(), Circuit::Einsum)
}

#[pyfunction]
#[pyo3(name = "einsum_nest_optimize")]
pub fn einsum_nest_optimize_py(einsum: &Einsum) -> Option<Einsum> {
    einsum_nest_optimize(
        einsum,
        &mut OptimizationContext::new_settings_circuit(Default::default(), einsum.clone().rc()),
    )
}

pub fn einsum_nest_optimize(einsum: &Einsum, context: &mut OptimizationContext) -> Option<Einsum> {
    // by default dont pre-contract subsets of arrayconstants
    let path = optimize_einsum_spec_cached(
        einsum.get_spec(),
        None,
        Some(context.cache.max_single_tensor_numel),
        None,
        Some(filter_to_idx(&einsum.args, &|(x, _)| {
            matches!(&***x, Circuit::ArrayConstant(_))
        })),
    )?;
    // let path = einsum.get_spec().optimize_dp(None,None,None);
    Some(einsum_nest_path(einsum, path))
}

/// corresponds to python function `construct_diag`
pub fn expand_maybe_diag(
    node: &CircuitRc,
    in_ints: &EinsumAxes,
    out_ints: &EinsumAxes,
    int_sizes: &HashMap<u8, usize>,
) -> CircuitRc {
    if in_ints[..] == out_ints[..] {
        return node.clone();
    }

    // if no diag, just expand
    if is_unique(in_ints) && is_unique(out_ints) {
        return Rearrange::nrc_elim_identity(
            node.clone(),
            RearrangeSpec::expand(in_ints, out_ints, int_sizes),
            None,
        );
    }

    let mut cur_ints = in_ints.clone();
    let mut result = node.clone();

    // broadcast to have all diag dims
    let out_int_appearances = unique_to_appearance(&out_ints.iter().collect());
    let ints_to_add_before_einsum: EinsumAxes = out_int_appearances
        .iter()
        .filter(|(int, appearances)| appearances.len() > 1 && !in_ints.contains(int))
        .map(|x| **x.0)
        .collect();
    if !ints_to_add_before_einsum.is_empty() {
        cur_ints = in_ints
            .iter()
            .chain(ints_to_add_before_einsum.iter())
            .cloned()
            .collect();
        result = Rearrange::nrc_elim_identity(
            result,
            RearrangeSpec::expand(
                &(0_u8..in_ints.len() as u8).collect(),
                &(0_u8..cur_ints.len() as u8).collect(),
                &cur_ints
                    .iter()
                    .enumerate()
                    .map(|(i, int)| (i as u8, int_sizes[int]))
                    .collect(),
            ),
            None,
        )
    }

    // make diag
    let einsum_out_ints: EinsumAxes = out_ints
        .iter()
        .filter(|i| cur_ints.contains(i))
        .cloned()
        .collect();
    result = Einsum::nrc(vec![(result, cur_ints)], einsum_out_ints.clone(), None);
    cur_ints = einsum_out_ints;

    // add non-diag broadcast dims
    if cur_ints[..] != out_ints[..] {
        result = Rearrange::nrc_elim_identity(
            result,
            RearrangeSpec::expand(
                &(0_u8..out_ints.len() as u8)
                    .filter(|i| cur_ints.contains(&out_ints[*i as usize]))
                    .collect(),
                &(0_u8..out_ints.len() as u8).collect(),
                &out_ints
                    .iter()
                    .enumerate()
                    .map(|(i, int)| (i as u8, int_sizes[int]))
                    .collect(),
            ),
            None,
        );
    }

    result
}

pub fn make_broadcast(
    node: &CircuitRc,
    out_shape: &Shape,
) -> Result<CircuitRc, TensorInvariantError> {
    let rank_dif = out_shape.len() - node.info().rank();
    let input_ints = node
        .info()
        .shape
        .iter()
        .enumerate()
        .map(|(i, x)| {
            if *x == 1 {
                sv![]
            } else {
                sv![(i + rank_dif) as u8]
            }
        })
        .collect();
    let output_ints: RInts = (0..(out_shape.len())).map(|i| sv![i as u8]).collect();
    let int_sizes = out_shape.clone();
    Ok(Rearrange::nrc_elim_identity(
        node.clone(),
        RearrangeSpec::new_canon(input_ints, output_ints, shape_to_op_shape(&int_sizes)),
        None,
    ))
}

#[pyfunction]
pub fn einsum_elim_identity(einsum: &Einsum) -> Option<CircuitRc> {
    if einsum.args.len() == 1
        && einsum.out_axes[..] == einsum.args[0].1[..]
        && is_unique(&einsum.out_axes)
    {
        Some(einsum.args[0].0.clone())
    } else if einsum.args.is_empty() {
        Some(ScalarConstant::new(1.0, sv![], None).rc())
    } else {
        None
    }
}

#[pyfunction]
pub fn index_merge_scalar(index: &Index) -> Option<CircuitRc> {
    index.node.as_scalar_constant().map(|scalar| {
        ScalarConstant::new(
            scalar.value,
            index.info().shape.clone(),
            index.name_cloned(),
        )
        .rc()
    })
}

#[pyfunction]
pub fn index_elim_identity(index: &Index) -> Option<CircuitRc> {
    if index.index.is_identity(&index.node.info().shape) {
        Some(index.node.clone())
    } else {
        None
    }
}

#[pyfunction]
pub fn index_fuse(index: &Index) -> Option<Index> {
    index.node.as_index().map(|inner| {
        Index::try_new(
            inner.node.clone(),
            compose(&index.index, &inner.index),
            index.name_cloned(),
        )
        .unwrap()
    })
}

#[pyfunction]
pub fn rearrange_merge_scalar(rearrange: &Rearrange) -> Option<CircuitRc> {
    rearrange.node.as_scalar_constant().map(|scalar| {
        ScalarConstant::new(
            scalar.value,
            rearrange.info().shape.clone(),
            rearrange.name_cloned(),
        )
        .rc()
    })
}

#[pyfunction]
pub fn rearrange_elim_identity(rearrange: &Rearrange) -> Option<CircuitRc> {
    if rearrange.spec.is_identity() {
        Some(rearrange.node.clone())
    } else {
        None
    }
}

#[pyfunction]
pub fn concat_merge_uniform(concat: &Concat) -> Option<CircuitRc> {
    let maybe_scalars: Vec<Option<f64>> = concat
        .nodes
        .iter()
        .map(|x| match &***x {
            Circuit::ScalarConstant(scalar) => Some(scalar.value),
            _ => None,
        })
        .collect();
    if maybe_scalars[0].is_some() && maybe_scalars.iter().all(|x| *x == maybe_scalars[0]) {
        Some(
            ScalarConstant::new(
                maybe_scalars[0].unwrap(),
                concat.info().shape.clone(),
                concat.name_cloned(),
            )
            .rc(),
        )
    } else {
        None
    }
}

#[pyfunction]
pub fn concat_elim_identity(concat: &Concat) -> Option<CircuitRc> {
    if concat.nodes.len() == 1 {
        Some(concat.nodes[0].clone())
    } else {
        None
    }
}

pub fn get_removable_axes(circuit: &CircuitRc) -> HashSet<usize> {
    match &***circuit {
        Circuit::ScalarConstant(_scalar) => (0..circuit.info().rank()).collect(),
        Circuit::Rearrange(rearrange) => rearrange
            .spec
            .out_broadcast_axes()
            .iter()
            .copied()
            .collect(),
        _ => HashSet::new(),
    }
}

pub fn remove_axes(circuit: &CircuitRc, axes: &HashSet<usize>) -> Option<CircuitRc> {
    if axes.is_empty() {
        return Some(circuit.clone());
    }
    match &***circuit {
        Circuit::ScalarConstant(scalar) => Some(
            ScalarConstant::new(
                scalar.value,
                filter_out_idx(&scalar.info().shape, axes)
                    .into_iter()
                    .collect(),
                scalar.name_cloned(),
            )
            .rc(),
        ),
        Circuit::Rearrange(rearrange) => {
            // canonicalize first to make input 1s (), allowing us to remove them from output
            let spec = rearrange.spec.canonicalize(true);
            Some(Rearrange::nrc_elim_identity(
                rearrange.node.clone(),
                spec.filter_out_axes_unsafe(axes),
                rearrange.name_cloned(),
            ))
        }
        _ => {
            if circuit
                .info()
                .shape
                .iter()
                .enumerate()
                .all(|(i, l)| !axes.contains(&i) || *l == 1)
            {
                Some(Rearrange::nrc_elim_identity(
                    circuit.clone(),
                    // wow this chained construction is long, should change at some point
                    RearrangeSpec::ident(circuit.info().rank())
                        .conform_to_input_shape(&circuit.info().shape, false)
                        .unwrap()
                        .canonicalize(true)
                        .filter_out_axes_unsafe(axes),
                    None,
                ))
            } else {
                None
            }
        }
    }
}

#[pyfunction]
pub fn generalfunction_pull_removable_axes(node: &GeneralFunction) -> Option<CircuitRc> {
    if node.nodes.len() != 1 {
        return None;
    }
    let removable_axes_inp = get_removable_axes(&node.nodes[0]);
    let removable_batchable_inp: HashSet<usize> = removable_axes_inp
        .iter()
        .filter(|x| **x < node.nodes[0].info().rank() - node.spec.num_non_batchable_output_dims)
        .cloned()
        .collect();
    if removable_batchable_inp.is_empty() {
        return None;
    }
    let new_generalfunction = GeneralFunction::try_new(
        vec![remove_axes(&node.nodes[0], &removable_batchable_inp).unwrap()],
        node.spec.clone(),
        node.name_cloned(),
    )
    .unwrap();
    let removable_batchable_out: HashSet<usize> = removable_batchable_inp
        .iter()
        .map(|x| x + node.info().rank() - node.nodes[0].info().rank())
        .collect();
    Some(Rearrange::nrc_elim_identity(
        new_generalfunction.rc(),
        RearrangeSpec::unremove_axes(&removable_batchable_out, &node.info().shape),
        None,
    ))
}

#[pyfunction]
pub fn concat_pull_removable_axes(node: &Concat) -> Option<CircuitRc> {
    let removable_axes_per: Vec<HashSet<usize>> =
        node.nodes.iter().map(get_removable_axes).collect();
    let removable_axes = intersection_all(&removable_axes_per);
    let removable_non_axis: HashSet<usize> = removable_axes
        .iter()
        .filter(|x| **x != node.axis)
        .cloned()
        .collect();
    if removable_non_axis.is_empty() {
        return None;
    }
    let new_axis = node.axis
        - removable_non_axis
            .iter()
            .filter(|i| **i < node.axis)
            .count();
    let new_node = Concat::try_new(
        node.nodes
            .iter()
            .map(|node| remove_axes(node, &removable_non_axis).unwrap())
            .collect(),
        new_axis,
        node.name_cloned(),
    )
    .unwrap();
    Some(Rearrange::nrc_elim_identity(
        new_node.rc(),
        RearrangeSpec::unremove_axes(&removable_non_axis, &node.info().shape),
        None,
    ))
}

#[pyfunction]
pub fn einsum_pull_removable_axes(einsum: &Einsum) -> Option<CircuitRc> {
    let mut did_anything = false;
    let mut new_args: EinsumArgs = einsum
        .args
        .iter()
        .map(|(node, ints)| {
            let removable_axes = get_removable_axes(node);
            if !removable_axes.is_empty() {
                did_anything = true;
                (
                    remove_axes(node, &removable_axes).unwrap(),
                    filter_out_idx(ints, &removable_axes).into_iter().collect(),
                )
            } else {
                (node.clone(), ints.clone())
            }
        })
        .collect();
    if !did_anything {
        return None;
    }
    let ints_in_new_args: HashSet<u8> = new_args
        .iter()
        .flat_map(|(_node, ints)| ints.clone())
        .collect();

    // multiply by product of removed reduced axes
    let shape_map = einsum.shape_map().unwrap();
    let reduced_axes = einsum.reduced_axes();
    let scalar_mul: f64 = reduced_axes
        .iter()
        .filter(|i| !ints_in_new_args.contains(i))
        .map(|i| shape_map[i] as f64)
        .product();
    if scalar_mul != 1.0 {
        new_args.push((ScalarConstant::new(scalar_mul, sv![], None).rc(), sv![]));
    }

    let new_out_ints: EinsumAxes = einsum
        .out_axes
        .iter()
        .filter(|i| ints_in_new_args.contains(i))
        .copied()
        .collect();
    let new_einsum = Einsum::nrc(new_args, new_out_ints.clone(), einsum.name_cloned());
    if new_out_ints[..] == einsum.out_axes[..] {
        Some(new_einsum)
    } else {
        // for now failing on diags bc simp loop
        if is_unique(&einsum.out_axes) {
            Some(expand_maybe_diag(
                &new_einsum,
                &new_out_ints,
                &einsum.out_axes,
                &shape_map,
            ))
        } else {
            None
        }
    }
}

#[pyfunction]
pub fn add_pull_removable_axes(add: &Add, remove_non_common_axes: bool) -> Option<CircuitRc> {
    let mut removed_any_non_one_axes = false;
    let removable_axes: Vec<HashSet<usize>> = add
        .nodes_and_rank_differences()
        .iter()
        .map(|(x, rank_difference)| {
            let pre_broadcast = get_removable_axes(x);
            let pre_broadcast_with_ones: HashSet<usize> = pre_broadcast
                .union(
                    &x.info()
                        .shape
                        .iter()
                        .enumerate()
                        .filter_map(|(i, l)| {
                            if *l != add.info().shape[i + rank_difference] {
                                Some(i)
                            } else {
                                None
                            }
                        })
                        .collect(),
                )
                .copied()
                .collect();
            if remove_non_common_axes
                && !removed_any_non_one_axes
                && pre_broadcast_with_ones
                    .iter()
                    .any(|i| x.info().shape[*i] != 1)
            {
                removed_any_non_one_axes = true;
            }
            pre_broadcast_with_ones
                .iter()
                .map(|i| i + rank_difference)
                .chain(0..*rank_difference)
                .collect()
        })
        .collect();

    let intersection = intersection_all(&removable_axes);
    if (intersection.is_empty() && !remove_non_common_axes)
        || (remove_non_common_axes && !removed_any_non_one_axes)
    {
        return None;
    }
    let post_rearrange_spec = RearrangeSpec::new_canon(
        (0..add.info().rank())
            .filter(|x| !intersection.contains(x))
            .map(|x| sv![x as u8])
            .collect(),
        (0..add.info().rank()).map(|x| sv![x as u8]).collect(),
        shape_to_op_shape(&add.info().shape),
    );
    let new_operands = zip(add.nodes_and_rank_differences(), removable_axes)
        .map(|((node, _rank_dif), removable_here_base)| {
            let rank_difference = add.info().rank() - node.info().rank();
            if !remove_non_common_axes {
                let removable_common_in_rank: HashSet<usize> = intersection
                    .iter()
                    .filter_map(|i| i.checked_sub(rank_difference))
                    .collect();
                remove_axes(&node, &removable_common_in_rank).unwrap()
            } else {
                let removable_here = removable_here_base
                    .iter()
                    .filter_map(|i| i.checked_sub(rank_difference))
                    .collect();
                let raw_removed = remove_axes(&node, &removable_here).unwrap();

                // let removable_here_to_add_back = removable_here.iter().filter(|i|!intersection.contains(i+rank_dif))

                let mut output_ints: RInts = sv![];
                let mut count = 0;
                let mut started = false;
                for i in 0..node.info().rank() {
                    if removable_here.contains(&i) {
                        if started && !intersection.contains(&(i + rank_difference)) {
                            output_ints.push(sv![]);
                        }
                    } else {
                        output_ints.push(sv![count]);
                        count += 1;
                        started = true;
                    }
                }

                let broadcast_rspec = RearrangeSpec::new_canon(
                    (0..raw_removed.info().rank())
                        .map(|i| sv![i as u8])
                        .collect(),
                    output_ints,
                    shape_to_op_shape(&raw_removed.info().shape),
                );
                Rearrange::nrc_elim_identity(raw_removed, broadcast_rspec, None)
            }
        })
        .collect();
    let add_circuit = Add::nrc(new_operands, add.name_cloned());
    Some(Rearrange::nrc_elim_identity(
        add_circuit,
        post_rearrange_spec,
        None,
    ))
}

#[pyfunction]
pub fn add_make_broadcasts_explicit(add: &Add) -> Option<Add> {
    let mut did_anything = false;
    let new_nodes = add
        .nodes
        .iter()
        .map(|node| {
            if node.info().shape[..] != add.info().shape[..] {
                did_anything = true;
                make_broadcast(node, &add.info().shape).unwrap()
            } else {
                node.clone()
            }
        })
        .collect();
    if !did_anything {
        return None;
    }
    Some(Add::try_new(new_nodes, add.name_cloned()).unwrap())
}

/// should return result instead
#[pyfunction]
pub fn distribute(einsum: &Einsum, operand_idx: usize, do_broadcasts: bool) -> Option<Add> {
    einsum.args[operand_idx].0.as_add().and_then(|add_node| {
        let mut add = add_node.clone();
        if do_broadcasts && add.has_broadcast() {
            add = add_make_broadcasts_explicit(&add).unwrap();
        }
        if add.has_broadcast() || add.nodes.is_empty() {
            println!("distribute failed");
            add.compiler_print();
            return None;
        }
        let summands = add
            .nodes
            .iter()
            .map(|node| {
                let mut new_args = einsum.args.clone();
                new_args[operand_idx].0 = node.clone();
                Einsum::nrc(new_args, einsum.out_axes.clone(), None)
            })
            .collect();
        Some(Add::try_new(summands, None).unwrap())
    })
}

/// distribute all Adds that are direct children of this einsum
/// not necessarily very useful?
#[pyfunction]
pub fn distribute_all(einsum: &Einsum) -> Option<Add> {
    let add_op_idxs = filter_to_idx(&einsum.args, &|(node, _ints)| {
        matches!(&***node, Circuit::Add(_)) && node.children().count() > 0
    });
    if add_op_idxs.is_empty() {
        return None;
    }
    let mut distributed = distribute(einsum, add_op_idxs[0], true).unwrap();
    if add_op_idxs.len() > 1 {
        distributed = distributed
            .map_children(&mut |node: &Circuit| match &*node {
                Circuit::Einsum(inner) => {
                    Ok::<CircuitRc, CircuitConstructionError>(distribute_all(inner).unwrap().rc())
                }
                _ => {
                    panic!();
                }
            })
            .unwrap()
    }
    Some(add_flatten_once(&distributed).unwrap_or(distributed))
}

#[pyfunction]
pub fn einsum_of_permute_merge(einsum: &Einsum) -> Option<Einsum> {
    let mut did_anything = false;
    let new_args = einsum
        .args
        .iter()
        .map(|(node, ints)| {
            node.as_rearrange()
                .and_then(|rearrange| {
                    rearrange.spec.get_fwd_permutation().map(|permutation| {
                        did_anything = true;
                        (
                            rearrange.node.clone(),
                            permutation.iter().map(|i| ints[*i]).collect(),
                        )
                    })
                })
                .unwrap_or_else(|| (node.clone(), ints.clone()))
        })
        .collect();
    if !did_anything {
        return None;
    }
    Some(Einsum::try_new(new_args, einsum.out_axes.clone(), None).unwrap())
}

#[pyfunction]
pub fn permute_of_einsum_merge(rearrange: &Rearrange) -> Option<Einsum> {
    rearrange.spec.get_fwd_permutation().and_then(|perm| {
        rearrange.node.as_einsum().map(|einsum| {
            Einsum::try_new(
                einsum.args.clone(),
                inverse_permutation(&perm)
                    .iter()
                    .map(|i| einsum.out_axes[*i])
                    .collect(),
                None,
            )
            .unwrap()
        })
    })
}

#[pyfunction]
pub fn einsum_elim_zero(einsum: &Einsum) -> Option<ScalarConstant> {
    if einsum.children().any(|x| match &**x {
        Circuit::ScalarConstant(scalar) => scalar.value == 0.0,
        _ => false,
    }) {
        Some(ScalarConstant::new(0.0, einsum.info().shape.clone(), None))
    } else {
        None
    }
}

#[pyfunction]
pub fn einsum_merge_scalars(einsum: &Einsum) -> Option<Einsum> {
    let mut num_scalars_found = 0;
    let mut scalar_mul: f64 = 1.0;
    let mut new_args: Vec<(CircuitRc, EinsumAxes)> = einsum
        .args
        .iter()
        .filter(|(node, _ints)| match &***node {
            Circuit::ScalarConstant(scalar) => {
                if scalar.info().shape.is_empty() {
                    num_scalars_found += 1;
                    scalar_mul *= scalar.value;
                    false
                } else {
                    true
                }
            }
            _ => true,
        })
        .cloned()
        .collect();
    if num_scalars_found <= 1 {
        return None;
    }
    if scalar_mul != 1.0 {
        new_args.push((ScalarConstant::new(scalar_mul, sv![], None).rc(), sv![]))
    }
    Some(Einsum::try_new(new_args, einsum.out_axes.clone(), None).unwrap())
}

#[pyfunction]
pub fn index_split_axes(node: &Index, top_axes: std::collections::HashSet<usize>) -> Option<Index> {
    let mut bottom: Vec<TensorAxisIndex> = vec![];
    let mut top: Vec<TensorAxisIndex> = vec![];
    if top_axes.iter().any(|i| *i >= node.node.info().rank()) {
        return None;
    }
    for (i, idx) in node.index.0.iter().enumerate() {
        if top_axes.contains(&i) {
            bottom.push(TensorAxisIndex::Slice(Slice {
                start: None,
                stop: None,
            }));
            top.push(idx.clone());
        } else {
            bottom.push(idx.clone());
            match idx {
                TensorAxisIndex::Single(_single) => {}
                _ => top.push(TensorAxisIndex::Slice(Slice {
                    start: None,
                    stop: None,
                })),
            }
        }
    }
    Some(
        Index::try_new(
            Index::try_new(node.node.clone(), TensorIndex(bottom), None)
                .unwrap()
                .rc(),
            TensorIndex(top),
            None,
        )
        .unwrap(),
    )
}

#[pyfunction]
pub fn rearrange_fuse(node: &Rearrange) -> Option<Rearrange> {
    node.node.as_rearrange().and_then(|inner| {
        RearrangeSpec::fuse(&inner.spec, &node.spec)
            .map(|spec| {
                Rearrange::try_new(
                    inner.node.clone(),
                    spec.canonicalize(true),
                    node.name_cloned(),
                )
                .unwrap()
            })
            .ok()
    })
}
/// this does less than python version, maybe should expand
#[pyfunction]
pub fn generalfunction_evaluate_simple(node: &GeneralFunction) -> Option<CircuitRc> {
    if !node.nodes.is_empty()
        || node.spec.num_non_batchable_output_dims != 0
        || !node.spec.is_batchable()
    {
        return None;
    }
    node.nodes[0].as_scalar_constant().map(|_inner| {
        Python::with_gil(|py| {
            ScalarConstant::new(
                evaluate_fn(&Circuit::GeneralFunction(node.clone()))
                    .unwrap()
                    .tensor()
                    .getattr(py, "item")
                    .unwrap()
                    .call(py, (), None)
                    .unwrap()
                    .extract(py)
                    .unwrap(),
                sv![],
                node.name_cloned(),
            )
            .rc()
        })
    })
}

// #[pyfunction]
// pub fn push_down_index_small(node:&Index)->Option<CircuitRc>{
//         // if you don't specify which_axes, choose all axes that reduce dimension
//     let which_axes = which_axes.unwrap_or_else(|| {
//         zip(node.index.0, node.info().shape)
//             .enumerate()
//             .filter_map(|(i, (idx, l))| {
//                 if let TensorAxisIndex::Tensor(tensor) = idx {
//                     if tensor.shape()[0] >= l {
//                         None
//                     } else {
//                         Some(i)
//                     }
//                 } else {
//                     Some(i)
//                 }
//             }).collect()
//     });
// }

#[pyfunction]
pub fn push_down_index(node: &Index) -> Option<CircuitRc> {
    match &**node.node {
        Circuit::Add(inner) => {
            let new_operands = inner
                .nodes_and_rank_differences()
                .iter()
                .map(|(operand, rank_difference)| {
                    let index_here = (0..operand.info().rank())
                        .map(|i| {
                            let idx_here = node.index.0[i + rank_difference].clone();
                            if operand.info().shape[i] == inner.info().shape[i + rank_difference] {
                                idx_here
                            } else {
                                match idx_here {
                                    TensorAxisIndex::Single(_s) => TensorAxisIndex::Single(0),
                                    _ => TensorAxisIndex::IDENT,
                                }
                            }
                        })
                        .collect();
                    Index::nrc(operand.clone(), TensorIndex(index_here), None)
                })
                .collect();
            Some(Add::nrc(new_operands, inner.name_cloned()))
        }
        Circuit::Concat(inner) => {
            let index_non_axis = TensorIndex(
                node.index
                    .0
                    .iter()
                    .enumerate()
                    .map(|(i, idx)| {
                        if i == inner.axis {
                            TensorAxisIndex::IDENT
                        } else {
                            idx.clone()
                        }
                    })
                    .collect(),
            );
            if index_non_axis.is_identity(&inner.info().shape) {
                return None;
            }
            // todo: drop concat parts that get indexed out
            let new_axis = inner.axis
                - node.index.0[..inner.axis]
                    .iter()
                    .filter(|idx| matches!(idx, TensorAxisIndex::Single(_)))
                    .count();

            let new_concat = Concat::nrc(
                inner
                    .nodes
                    .iter()
                    .map(|operand| Index::nrc(operand.clone(), index_non_axis.clone(), None))
                    .collect(),
                new_axis,
                inner.name_cloned(),
            );
            let final_index = TensorIndex::new_single(
                node.index.0[inner.axis].clone(),
                new_axis,
                new_concat.info().rank(),
            );
            Some(Index::nrc(new_concat, final_index, None))
        }
        Circuit::GeneralFunction(inner) => {
            if !inner.spec.is_batchable()
                || inner.spec.num_non_batchable_output_dims == inner.info().rank()
            {
                None
            } else {
                let rank_to_pass = inner.info().rank() - inner.spec.num_non_batchable_output_dims;
                let new_operands = zip(&inner.nodes, &inner.spec.input_batchability)
                    .map(|(child, batchable)| {
                        if *batchable {
                            let ident_rank = child.info().rank() - rank_to_pass;
                            let index_passed = TensorIndex(
                                node.index.0[..rank_to_pass]
                                    .iter()
                                    .cloned()
                                    .chain(vec![TensorAxisIndex::IDENT; ident_rank])
                                    .collect(),
                            );
                            Index::nrc(child.clone(), index_passed, None)
                        } else {
                            child.clone()
                        }
                    })
                    .collect();
                let new_gf =
                    GeneralFunction::nrc(new_operands, inner.spec.clone(), inner.name_cloned());
                let passed_rank_now = rank_to_pass
                    - (0..rank_to_pass)
                        .filter(|i| matches!(node.index.0[*i], TensorAxisIndex::Single(_)))
                        .count();
                let index_top = TensorIndex(
                    vec![TensorAxisIndex::IDENT; passed_rank_now]
                        .iter()
                        .cloned()
                        .chain(node.index.0[rank_to_pass..].iter().cloned())
                        .collect(),
                );
                Some(Index::nrc(new_gf, index_top, None))
            }
        }
        Circuit::Einsum(inner) => {
            let mut int_indices: HashMap<u8, Option<TensorAxisIndex>> = HashMap::new();
            for (idx, int) in zip(&node.index.0, &inner.out_axes) {
                match int_indices.get(int) {
                    Some(_prev_idx) => {
                        // todo: equality on tensoraxisindex so we can pass if same
                        int_indices.insert(*int, None);
                    }
                    None => {
                        int_indices.insert(*int, Some(idx.clone()));
                    }
                }
            }
            let ints_filter_index = |ints: &EinsumAxes| -> EinsumAxes {
                ints.iter()
                    .filter_map(|i| {
                        match int_indices
                            .get(i)
                            .cloned()
                            .flatten()
                            .unwrap_or(TensorAxisIndex::IDENT)
                        {
                            TensorAxisIndex::Single(_) => None,
                            _ => Some(*i),
                        }
                    })
                    .collect()
            };
            let mut any_operand_index_nontrivial = false;
            let new_operands: Vec<(CircuitRc, EinsumAxes)> = inner
                .args
                .iter()
                .map(|(node, ints)| {
                    let index_here = TensorIndex(
                        ints.iter()
                            .map(|i| {
                                int_indices
                                    .get(i)
                                    .cloned()
                                    .flatten()
                                    .unwrap_or(TensorAxisIndex::IDENT)
                            })
                            .collect(),
                    );
                    if !index_here.is_identity(&node.info().shape) {
                        any_operand_index_nontrivial = true;
                    }
                    (
                        Index::nrc(node.clone(), index_here, None),
                        ints_filter_index(ints), // todo make function work with sv
                    )
                })
                .collect();
            if !any_operand_index_nontrivial {
                return None;
            }
            let new_einsum = Einsum::nrc(new_operands, ints_filter_index(&inner.out_axes), None);
            let out_index = TensorIndex(
                zip(&inner.out_axes, &node.index.0)
                    .filter_map(|(i, idx)| match int_indices.get(i).unwrap() {
                        None => Some(idx.clone()),
                        Some(int_idx) => match int_idx {
                            TensorAxisIndex::Single(_) => None,
                            _ => Some(TensorAxisIndex::IDENT),
                        },
                    })
                    .collect(),
            );
            Some(Index::nrc(new_einsum, out_index, None))
        }
        Circuit::Rearrange(inner) => {
            // doing this in python instead of porting to rust bc it has a lot of torch ops so likely wouldn't be faster in rust
            let python_result: Option<(TensorIndex, RearrangeSpec)> = Python::with_gil(|py| {
                PY_CIRCUIT_ITEMS
                    .circ_compiler_util
                    .getattr(py, "index_before_rearrange_rust")
                    .unwrap()
                    .call(
                        py,
                        (
                            node.index.clone(),
                            inner.spec.clone(),
                            inner.node.info().shape.clone(),
                            node.info().device_dtype.clone().unwrap_or_defaults().device,
                        ),
                        None,
                    )
                    .unwrap()
                    .extract(py)
                    .ok()
            });
            python_result.map(|(index, spec)| {
                let new_index = Index::nrc(inner.node.clone(), index, node.name_cloned());
                Rearrange::nrc_elim_identity(new_index, spec, inner.name_cloned())
            })
        }
        Circuit::Scatter(inner) => {
            // for now it just pushes indexes of Single(0) through axes size 1
            let mut new_outer = vec![];
            let mut new_scatter = vec![];
            let mut new_scatter_shape: Shape = sv![];
            let mut did_anything = false;
            let passed_index = zip(
                &node.index.0,
                zip(inner.index.all_uslices().unwrap(), &inner.info().shape),
            )
            .map(|(top_index, (bottom_scatter, l))| {
                if let TensorAxisIndex::Single(single) = top_index {
                    if bottom_scatter == (USlice { start: 0, stop: 1 }) && *single == 0 {
                        did_anything = true;
                        return top_index.clone();
                    }
                }
                new_outer.push(top_index.clone());
                new_scatter.push(bottom_scatter);
                new_scatter_shape.push(*l);
                TensorAxisIndex::IDENT
            })
            .collect();
            if !did_anything {
                return None;
            }
            let inner_node = Index::nrc(inner.node.clone(), TensorIndex(passed_index), None);
            let result = Some(Index::nrc(
                Scatter::nrc(
                    inner_node,
                    TensorIndex(new_scatter.iter().cloned().map(USlice::into).collect()),
                    new_scatter_shape,
                    None,
                ),
                TensorIndex(new_outer),
                None,
            ));
            result
        }
        _ => None,
    }
}

#[pyfunction]
pub fn concat_repeat_to_rearrange(concat: &Concat) -> Option<Concat> {
    if concat.nodes.is_empty() {
        return None;
    }
    let mut prev_node: CircuitRc = concat.nodes[0].clone();
    let mut same_seen = 1;
    let mut did_anything = false;
    let mut new_nodes: Vec<CircuitRc> = vec![];

    // add unique additional node to the end of the chain so that we have node != &prev_node at the end
    let extra_unique_node = Symbol::new_with_random_uuid(concat.info().shape.clone(), None).rc();

    for node in concat
        .nodes
        .iter()
        .dropping(1)
        .chain(std::iter::once(&extra_unique_node))
    {
        if node != &prev_node {
            if same_seen > 1 {
                did_anything = true;
                let mut int_sizes = prev_node.info().shape.clone();
                int_sizes.push(same_seen);
                new_nodes.push(Rearrange::nrc_elim_identity(
                    prev_node.clone(),
                    RearrangeSpec {
                        input_ints: (0..prev_node.info().rank()).map(|x| sv![x as u8]).collect(),
                        output_ints: (0..prev_node.info().rank())
                            .map(|x| {
                                if x == concat.axis {
                                    // create group which is (count, axis_size) for total dim size of
                                    // count * axis_size()
                                    sv![prev_node.info().rank() as u8, x as u8]
                                } else {
                                    sv![x as u8]
                                }
                            })
                            .collect(),
                        int_sizes: shape_to_op_shape(&int_sizes),
                    },
                    None,
                ));
            } else {
                new_nodes.push(prev_node.clone())
            }
            same_seen = 1;
        } else {
            same_seen += 1
        }
        prev_node = node.clone();
    }
    if !did_anything {
        return None;
    }
    Some(Concat::try_new(new_nodes, concat.axis, concat.name_cloned()).unwrap())
}

#[test]
fn basic_check_same_concat_shape() {
    let a = Symbol::new_with_random_uuid(sv![2, 3, 4, 5, 6], None).rc();
    let out = concat_repeat_to_rearrange(
        &Concat::try_new(vec![a.clone(), a.clone(), a], 3, None).unwrap(),
    )
    .unwrap();
    assert_eq!(out.info().shape[3], 15)
}

#[inline]
pub fn is_not_outer(a: BitMask128, b: BitMask128) -> bool {
    let union = a & b;
    union == a || union == b
}

/// this takes bitmasks of axes and produces bitmasks of indices into argument bitmasks that each don't have any outer products
pub fn bitmask_outer_product_sets(bitmasks: &Vec<BitMask128>) -> Vec<BitMask128> {
    let mut result: Vec<BitMask128> = vec![];
    let mut result_axes: Vec<BitMask128> = vec![];
    for (input_idx, bm) in bitmasks.iter().enumerate() {
        let mut did_anything = false;
        let mut result_index_out: usize = 0;
        for (result_index, result_ax) in result_axes.iter().enumerate() {
            if is_not_outer(*bm, *result_ax) {
                result[result_index] |= 1 << input_idx;
                did_anything = true;
                result_index_out = result_index;
                break;
            }
        }
        if !did_anything {
            result.push(1 << input_idx);
            result_axes.push(*bm);
        } else {
            result_axes[result_index_out] |= bm;
        }
    }
    result
}

#[test]
fn test_bitmask_outer_product_sets() {
    let ex: Vec<u128> = vec![1 + 4, 2 + 4, 4, 1];
    dbg!(&ex);
    dbg!(bitmask_outer_product_sets(&ex));
    dbg!(bitmask_outer_product_sets(&ex)
        .iter()
        .map(|x| BitIter::from(*x).collect())
        .collect::<Vec<Vec<usize>>>());
}

#[pyfunction]
pub fn add_outer_product_broadcasts_on_top(add: &Add) -> Option<Add> {
    let axis_sets: Vec<BitMask128> = add
        .nodes_and_rank_differences()
        .iter()
        .map(|(child, rank_dif)| {
            let mut bitmask: BitMask128 = 0;
            for (i, l) in child.info().shape.iter().enumerate() {
                if *l != 1 {
                    bitmask |= 1 << (rank_dif + i)
                }
            }
            bitmask
        })
        .collect();
    let outer_product_sets = bitmask_outer_product_sets(&axis_sets);
    if outer_product_sets.len() <= 1 {
        return None;
    }
    let new_operands = outer_product_sets
        .iter()
        .map(|operand_set_bitmask| {
            Add::try_new(
                BitIter::from(*operand_set_bitmask)
                    .map(|i| add.nodes[i].clone())
                    .collect(),
                None,
            )
            .unwrap()
            .rc()
        })
        .collect();
    Some(Add::try_new(new_operands, None).unwrap())
}

/// returns None if sub isn't subset
#[pyfunction]
pub fn extract_add(add: &Add, sub: &Add) -> Option<Add> {
    let mut counts = add.to_counts();

    for item in &sub.nodes {
        match counts.entry(item.clone()) {
            Entry::Occupied(mut entry) => {
                let new = entry.get().saturating_sub(1);
                if new == 0 {
                    entry.remove_entry();
                } else {
                    *entry.get_mut() = new;
                }
            }
            Entry::Vacant(_) => return None,
        }
    }
    *counts.entry(sub.clone().rc()).or_insert(0) += 1;

    Some(Add::try_from_counts(&counts, add.name_cloned()).unwrap())
}
