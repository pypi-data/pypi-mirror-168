use crate::circuit::scatter_rewrite::concat_to_scatter;
use crate::hashmaps::{AHashSet as HashSet, FxHashMap as HashMap};

use crate::circuit::deep_map_op_context;
use crate::util::{apply_fn_until_same, mapping_until_end, AsOp};
use crate::{pyo3_prelude::*, timed_value};
use num_bigint::BigUint;

use super::{
    algebraic_rewrite::*,
    canonicalize::deep_canonicalize,
    circuit_optimizer::OptimizationContext,
    concat_rewrite::add_pull_concat,
    concat_rewrite::{
        concat_drop_size_zero, concat_fuse, einsum_pull_concat, generalfunction_pull_concat,
        index_concat_drop_unreached,
    },
    deep_map_unwrap, deep_map_unwrap_preorder,
    diag_rewrite::{add_pull_diags, einsum_push_down_trace},
    prelude::*,
    scatter_rewrite::{
        add_pull_scatter, einsum_pull_scatter, index_einsum_to_scatter, scatter_elim_identity,
        scatter_fuse, scatter_pull_removable_axes,
    },
    visit_circuit, Add, Concat, GeneralFunction, Index,
};

/// seperate _py function because pyfunctions cant take reference arguments
#[pyfunction]
#[pyo3(name = "compiler_simp_step")]
pub fn compiler_simp_step_py(circ: CircuitRc) -> Option<CircuitRc> {
    compiler_simp_step(&circ, &mut Default::default())
}

pub fn compiler_simp_step(
    circuit: &Circuit,
    context: &mut OptimizationContext,
) -> Option<CircuitRc> {
    macro_rules! f_wrap {
        ($f:expr) => {
            (stringify!($f), &|x| $f(x).map(|v| v.rc()))
        };
    }

    macro_rules! l_wrap {
        ($f:expr) => {
            (stringify!($f), &|x| $f(x))
        };
    }

    fn simp<'a, T: CircuitNode + Into<Circuit> + Clone>(
        x: &'a T,
        fns: &[(&'static str, &dyn Fn(&'a T) -> Option<CircuitRc>)],
        context: &mut OptimizationContext,
    ) -> Option<CircuitRc> {
        for (name, f) in fns {
            if let Some(result) = f(x) {
                if **result == x.clone().c() {
                    println!("{}", stringify!(f));
                    x.clone().rc().compiler_print();
                    result.compiler_print();
                    panic!()
                }
                if context.settings.log_simplifications {
                    if context.settings.verbose >= 3 {
                        println!("{}", name);
                    }
                    context.cache.simplification_log.push(name);
                }
                return Some(result);
            }
        }

        None
    }

    match &*circuit {
        Circuit::Add(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(&remove_add_few_input),
                f_wrap!(add_flatten_once),
                f_wrap!(add_elim_zeros),
                f_wrap!(add_collapse_scalar_inputs),
                f_wrap!(add_deduplicate),
                l_wrap!(|x| add_pull_removable_axes(x, true)),
                f_wrap!(add_pull_scatter),
                f_wrap!(add_pull_diags),
            ];
            simp(node, fns, context)
        }
        Circuit::Einsum(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                f_wrap!(&einsum_elim_zero),
                l_wrap!(einsum_elim_identity),
                f_wrap!(&einsum_flatten_once),
                f_wrap!(&einsum_of_permute_merge),
                f_wrap!(&einsum_merge_scalars),
                l_wrap!(einsum_pull_removable_axes),
                l_wrap!(einsum_pull_scatter),
                f_wrap!(&einsum_push_down_trace),
            ];
            simp(node, fns, context)
        }
        Circuit::Index(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(index_elim_identity),
                f_wrap!(&index_fuse),
                l_wrap!(index_merge_scalar),
                l_wrap!(index_einsum_to_scatter),
                l_wrap!(index_concat_drop_unreached),
            ];
            simp(node, fns, context)
        }
        Circuit::Rearrange(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(rearrange_elim_identity),
                f_wrap!(&rearrange_fuse),
                l_wrap!(rearrange_merge_scalar),
                f_wrap!(&permute_of_einsum_merge),
            ];
            simp(node, fns, context)
        }
        Circuit::Concat(node) => {
            let fns: &[(&'static str, &dyn Fn(&Concat) -> _)] = &[
                l_wrap!(concat_elim_identity),
                l_wrap!(concat_pull_removable_axes),
                l_wrap!(concat_merge_uniform),
                f_wrap!(&concat_drop_size_zero),
                f_wrap!(&concat_fuse),
                f_wrap!(&concat_repeat_to_rearrange),
                f_wrap!(&concat_to_scatter),
            ];
            simp(node, fns, context)
        }
        Circuit::GeneralFunction(node) => {
            let fns: &[(&'static str, &dyn Fn(&GeneralFunction) -> _)] = &[
                l_wrap!(generalfunction_pull_removable_axes),
                l_wrap!(generalfunction_evaluate_simple),
            ];
            simp(node, fns, context)
        }
        Circuit::Scatter(node) => {
            let fns: &[(&'static str, &dyn Fn(_) -> _)] = &[
                l_wrap!(scatter_elim_identity),
                f_wrap!(&scatter_fuse),
                f_wrap!(&scatter_pull_removable_axes),
            ];
            simp(node, fns, context)
        }
        _ => None,
    }
}

/// Deep simplification strategy
///
/// The strategy to apply `compiler_simp_step` to each node in the circuit from the bottom up (post-order).
/// Every time a node is simplified, we iterate over the children to make sure that any children we haven't
/// seen before get recursively fully simplified before continuing.
/// The final result is a fixed point where no further `compiler_simp_step` simplifications are possible.
#[pyfunction]
#[pyo3(name = "compiler_simp")]
pub fn compiler_simp_py(circ: CircuitRc) -> CircuitRc {
    let mut context = Default::default();
    compiler_simp(&circ, &mut context)
}

pub fn compiler_simp(circ: &Circuit, opt_context: &mut OptimizationContext) -> CircuitRc {
    /// check if any new children have not been simplified yet, and simplify them if so
    fn simplify_changed_descendants(
        circ: &Circuit,
        context: &mut OptimizationContext,
    ) -> Option<CircuitRc> {
        // if let Some(changed) = compiler_simp_step(circ){
        //     return simplify_changed_descendants(circ, simplified)
        // }
        circ.map_children_op(&mut |x: &Circuit| {
            if context.cache.simplified.contains_key(&x.info().hash) {
                None
            } else {
                Some(fully_simplify(x.clone().rc(), context))
            }
        })
        .map(|c| c.rc())
    }
    /// fully simplify a circuit and all its descendants recursively until we hit a fixed point
    fn fully_simplify(circ: CircuitRc, context: &mut OptimizationContext) -> CircuitRc {
        if let Some(result) = context.cache.simplified.get(&circ.info().hash) {
            return result.clone();
        }
        let mut result: CircuitRc = circ
            .map_children_unwrap(&mut |x: &Circuit| fully_simplify(x.clone().rc(), context))
            .rc();
        for iter_count in 0.. {
            match compiler_simp_step(&result, context) {
                Some(r) => result = simplify_changed_descendants(&r, context).unwrap_or(r),
                None => break,
            }
            if iter_count > 50 {
                result.compiler_print();
                compiler_simp_step(&result, context)
                    .unwrap()
                    .compiler_print();
                panic!();
            }
        }
        context
            .cache
            .simplified
            .insert(circ.info().hash, result.clone());
        result
    }
    fully_simplify(circ.clone().rc(), opt_context)
}

#[pyfunction]
pub fn compiler_simp_until_same(circ: CircuitRc) -> CircuitRc {
    let mut context = Default::default();

    apply_fn_until_same(&circ, |x: &CircuitRc| compiler_simp(x, &mut context))
}

#[pyfunction]
pub fn deep_push_down_index(circ: CircuitRc, min_size: Option<usize>) -> CircuitRc {
    deep_map_unwrap_preorder(&circ, |circ| {
        if min_size.is_none()
            || circ
                .children()
                .chain(std::iter::once(circ.clone().rc()))
                .any(|z| z.info().numel() >= BigUint::from(min_size.unwrap()))
        {
            circ.and_then_or_clone(&|index: &Index| {
                push_down_index(&index.and_then_or_clone(index_fuse))
            })
        } else {
            circ.clone().rc()
        }
    })
}

/// we want adds to be nested rather than flat so arguments can be dropped if they're only needed
/// in future adds
/// this is suboptimal in many ways. one is broadcasts allow outer products which should be avoided but aren't
/// for each add, greedily nest into preexisting adds
#[pyfunction]
pub fn deep_heuristic_nest_adds(circ: CircuitRc) -> CircuitRc {
    let circ = deep_canonicalize(circ, &mut Default::default());
    let mut seen_adds: HashSet<Add> = HashSet::new();
    visit_circuit(&circ, &mut |c: &Circuit| {
        if let Some(add) = c.as_add() {
            seen_adds.insert(add.clone());
        }
    });
    // TODO: profile and optimize these
    let mut intersections: HashSet<Add> = HashSet::new();
    for circ in &seen_adds {
        for circ2 in &seen_adds {
            let intersection = Add::try_new(
                circ.nodes
                    .iter()
                    .filter(|x| circ2.nodes.contains(x))
                    .cloned()
                    .collect(),
                None,
            )
            .unwrap();
            if intersection.nodes.len() >= 2 && &intersection != circ && &intersection != circ2 {
                intersections.insert(intersection);
            }
        }
    }
    seen_adds.extend(intersections);
    let mut mapping: HashMap<Add, Add> = HashMap::new();
    while let Some((sup, new_sup)) = (|| {
        for cand_sub in &seen_adds {
            if cand_sub.nodes.len() >= 2 {
                for cand_sup in &seen_adds {
                    if cand_sub != cand_sup {
                        if let Some(new) = extract_add(cand_sup, cand_sub) {
                            return Some((cand_sup.clone(), new));
                        }
                    }
                }
            }
        }
        None
    })() {
        seen_adds.remove(&sup);
        seen_adds.insert(new_sup.clone());
        mapping.insert(sup, new_sup.clone());
    }

    deep_map_unwrap_preorder(&circ, |c| {
        c.map_or_clone(|add: &Add| {
            let add = mapping_until_end(add, &mapping);

            if add.info().numel() > BigUint::from(100_000_000usize) {
                add_nest_ltr(&add)
            } else {
                add
            }
        })
    })
}

pub fn add_nest_ltr(add: &Add) -> Add {
    let (l, r) = add.nodes.split_at(2.min(add.nodes.len()));
    let base = Add::try_new(l.to_vec(), None).unwrap();
    r.iter().fold(base, |acc, x| {
        Add::try_new(vec![acc.rc(), x.clone()], None).unwrap()
    })
}

#[pyfunction]
#[pyo3(name = "add_nest_ltr")]
pub fn add_nest_ltr_py(add: Add) -> Add {
    add_nest_ltr(&add)
}

#[pyfunction]
pub fn deep_pull_concat_messy(circuit: CircuitRc, min_size: Option<usize>) -> CircuitRc {
    deep_map_unwrap(&circuit, &|x: &Circuit| {
        if min_size.is_none()
            || x.children()
                .chain(std::iter::once(x.clone().rc()))
                .any(|z| z.info().numel() >= BigUint::from(min_size.unwrap()))
        {
            match x {
                Circuit::Add(add) => add.and_then_or_clone(add_pull_concat),
                Circuit::GeneralFunction(func) => {
                    func.and_then_or_clone(generalfunction_pull_concat)
                }
                Circuit::Einsum(einsum) => einsum.and_then_or_clone(einsum_pull_concat),
                Circuit::Concat(concat) => concat.and_then_or_clone(concat_fuse),
                _ => x.clone().rc(),
            }
        } else {
            x.clone().rc()
        }
    })
}

#[pyfunction]
pub fn deep_pull_concat(circuit: CircuitRc, min_size: Option<usize>) -> CircuitRc {
    let mut cache = Default::default();
    let pulled = deep_pull_concat_messy(circuit, min_size);
    pulled.compiler_print();
    apply_fn_until_same(&pulled, |x: &CircuitRc| {
        let result = deep_push_down_index(compiler_simp(x, &mut cache), min_size);
        result.compiler_print();
        result
    })
}

#[pyfunction]
#[pyo3(name = "deep_optimize_einsums")]
pub fn deep_optimize_einsums_py(circ: CircuitRc) -> CircuitRc {
    deep_optimize_einsums(circ, &mut Default::default())
}

pub fn deep_optimize_einsums(circ: CircuitRc, context: &mut OptimizationContext) -> CircuitRc {
    deep_map_op_context(
        &**circ,
        &|x: &Circuit, context: &mut OptimizationContext| match x {
            Circuit::Einsum(ein) => {
                let (result, took) = timed_value!(einsum_nest_optimize(ein, context));
                let result = result?;
                if took.as_millis() > 10 {
                    context.cache.slow_einsum_log.push(ein.get_spec());
                }
                Some(result.rc())
            }
            _ => None,
        },
        context,
        &mut HashMap::new(),
    )
    .unwrap_or(circ.clone())
}
