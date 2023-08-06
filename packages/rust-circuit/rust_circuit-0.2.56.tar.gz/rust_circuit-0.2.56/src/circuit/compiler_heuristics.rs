use crate::hashmaps::FxHashMap as HashMap;

use crate::{circuit::canonicalize::deep_canonicalize, pyo3_prelude::*, timed};
use num_bigint::BigUint;

use super::{
    algebraic_rewrite::distribute,
    circuit_optimizer::{OptimizationContext, OptimizationSettings},
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
    if context.cache.times_distributed > 10000 {
        println!("compiler hit distribute limit");
        return None;
    }
    for (i, operand) in node.children().enumerate() {
        if let Circuit::Add(_add) = &**operand && !_add.nodes.is_empty()&& ( operand.info().numel() >= BigUint::from(context.settings.distribute_min_size.unwrap_or(context.cache.max_single_tensor_numel)))

        {
            let result = timed!(deep_canonicalize( compiler_simp(&distribute(node, i, true).unwrap().rc(),context),context),1,context.settings.verbose>=3);
            context.cache.times_distributed+=1;
            return Some(result);
        }
    }
    None
}

#[pyfunction]
#[pyo3(name = "deep_maybe_distribute")]
pub fn deep_maybe_distribute_py(node: CircuitRc, settings: OptimizationSettings) -> CircuitRc {
    let mut context = &mut OptimizationContext::new_settings(settings);
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
