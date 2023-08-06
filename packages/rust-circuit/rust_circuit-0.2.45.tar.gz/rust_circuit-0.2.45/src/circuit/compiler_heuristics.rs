use crate::hashmaps::FxHashMap as HashMap;

use crate::pyo3_prelude::*;
use num_bigint::BigUint;

use super::{
    algebraic_rewrite::{add_outer_product_broadcasts_on_top, distribute, get_removable_axes},
    circuit_optimizer::{OptimizationContext, OptimizationSettings},
    circuit_utils::{sum_of_node_sizes_cached, total_flops_cached},
    deep_map_op_context,
    deep_rewrite::compiler_simp,
    prelude::*,
    Einsum,
};

#[pyfunction]
pub fn maybe_distribute_py(node: &Einsum) -> Option<CircuitRc> {
    maybe_distribute_uncached(node, &mut Default::default())
}

pub fn maybe_distribute(node: &Einsum, context: &mut OptimizationContext) -> Option<CircuitRc> {
    let key = node.info().hash;
    match context.cache.distributed.get(&key) {
        Some(z) => z.clone(),
        None => {
            let result = maybe_distribute_uncached(node, context);
            context.cache.distributed.insert(key, result.clone());
            result
        }
    }
}

/// only is reasonable if adds have gone through add_pull_removable, but meant to not crash otherwise
/// this is simpler than python version, maybe worse than it
pub fn maybe_distribute_uncached(
    node: &Einsum,
    context: &mut OptimizationContext,
) -> Option<CircuitRc> {
    for (i, operand) in node.children().enumerate() {
        if node.max_non_input_size() >= BigUint::from(context.settings.distribute_min_size)
            && let Circuit::Add(add) = &**operand
            && (add_outer_product_broadcasts_on_top(add).is_some() ||  add.children().any(|child| {
                !get_removable_axes(&child).is_empty()
                || matches!(&**child, Circuit::Einsum(_) | Circuit::Scatter(_))
               }))

        {
            let noderc = node.clone().rc();
            let result = compiler_simp(&distribute(node, i, true).unwrap().rc(),context);
            if result.info().max_non_input_size < node.info().max_non_input_size ||total_flops_cached(result.clone(),&mut context.cache.flops)<total_flops_cached(noderc.clone(),&mut context.cache.flops)||sum_of_node_sizes_cached(result.clone(),&mut context.cache.sum_of_node_sizes)<sum_of_node_sizes_cached(noderc,&mut context.cache.sum_of_node_sizes){
                return Some(result);
            }
        }
    }
    None
}

#[pyfunction]
#[pyo3(name = "deep_maybe_distribute")]
pub fn deep_maybe_distribute_py(node: CircuitRc, settings: OptimizationSettings) -> CircuitRc {
    let mut context = OptimizationContext {
        settings,
        cache: Default::default(),
    };
    deep_maybe_distribute(&node, &mut context)
}

pub fn deep_maybe_distribute(node: &Circuit, context: &mut OptimizationContext) -> CircuitRc {
    deep_map_op_context(
        node,
        &|x: &Circuit, context: &mut OptimizationContext| match x {
            Circuit::Einsum(ein) => maybe_distribute(ein, context),
            _ => None,
        },
        context,
        &mut HashMap::new(),
    )
    .unwrap_or(node.clone().rc())
}
