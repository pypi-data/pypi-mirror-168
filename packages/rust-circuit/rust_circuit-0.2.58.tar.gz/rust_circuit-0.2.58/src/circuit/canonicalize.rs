use std::collections::HashMap;

use crate::pyo3_prelude::*;

use super::{
    circuit_optimizer::OptimizationContext, deep_map_op_context, prelude::*, Add, Einsum, Index,
    Rearrange,
};

/// takes circuitrc bc convenient
pub fn numel_sort_key(node: &CircuitRc) -> Vec<u8> {
    (usize::MAX - node.info().numel().to_u64_digits()[0] as usize)
        .to_be_bytes()
        .iter()
        .copied()
        .chain(node.variant_string().bytes())
        .chain(node.info().hash)
        .collect::<Vec<u8>>()
}

#[pyfunction]
#[pyo3(name = "canonicalize_node")]
pub fn canonicalize_node_py(circuit: CircuitRc) -> CircuitRc {
    canonicalize_node_op(&circuit).unwrap_or(circuit.clone())
}

pub fn canonicalize_node_op(circuit: &Circuit) -> Option<CircuitRc> {
    match &*circuit {
        Circuit::Rearrange(rearrange) => Some(Rearrange::nrc(
            rearrange.node.clone(),
            rearrange
                .spec
                .conform_to_input_shape(&rearrange.node.info().shape, false)
                .unwrap()
                .canonicalize(true),
            circuit.name_cloned(),
        )),
        Circuit::Index(index) => Some(Index::nrc(
            index.node.clone(),
            index.index.canonicalize(&index.node.info().shape),
            index.name_cloned(),
        )),
        Circuit::Add(add) => {
            let mut nodes_sorted = add.nodes.clone();
            nodes_sorted.sort_by_key(numel_sort_key);
            Some(Add::nrc(nodes_sorted, add.name_cloned()))
        }
        Circuit::Einsum(einsum) => {
            let mut args_sorted = einsum.args.clone();
            args_sorted.sort_by_key(|(node, _ints)| numel_sort_key(node));
            Some(
                Einsum::try_new(args_sorted, einsum.out_axes.clone(), einsum.name_cloned())
                    .unwrap()
                    .normalize_ints()
                    .rc(),
            )
        }
        _ => None,
    }
}

#[pyfunction]
#[pyo3(name = "deep_canonicalize")]
pub fn deep_canonicalize_py(circuit: CircuitRc) -> CircuitRc {
    deep_canonicalize(circuit, &mut Default::default())
}

pub fn deep_canonicalize(circuit: CircuitRc, context: &mut OptimizationContext) -> CircuitRc {
    deep_map_op_context(
        &circuit,
        &|x, _c: &mut HashMap<(), ()>| canonicalize_node_op(x),
        &mut HashMap::<(), ()>::new(),
        &mut context.cache.canonicalized,
    )
    .unwrap_or(circuit.clone())
}
