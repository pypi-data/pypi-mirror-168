use crate::pyo3_prelude::*;

use super::{deep_map_unwrap, prelude::*, Add, Einsum, Index, Rearrange};

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
    canonicalize_node(&circuit)
}

pub fn canonicalize_node(circuit: &Circuit) -> CircuitRc {
    match &*circuit {
        Circuit::Rearrange(rearrange) => Rearrange::try_new(
            rearrange.node.clone(),
            rearrange
                .spec
                .conform_to_input_shape(&rearrange.node.info().shape, false)
                .unwrap()
                .canonicalize(true),
            circuit.name_cloned(),
        )
        .unwrap()
        .rc(),
        Circuit::Index(index) => Index::try_new(
            index.node.clone(),
            index.index.canonicalize(&index.node.info().shape),
            index.name_cloned(),
        )
        .unwrap()
        .rc(),
        Circuit::Add(add) => {
            let mut nodes_sorted = add.nodes.clone();
            nodes_sorted.sort_by_key(numel_sort_key);
            Add::try_new(nodes_sorted, add.name_cloned()).unwrap().rc()
        }
        Circuit::Einsum(einsum) => {
            let mut args_sorted = einsum.args.clone();
            args_sorted.sort_by_key(|(node, _ints)| numel_sort_key(node));
            Einsum::try_new(args_sorted, einsum.out_axes.clone(), einsum.name_cloned())
                .unwrap()
                .normalize_ints()
                .rc()
        }
        _ => circuit.clone().rc(),
    }
}

#[pyfunction]
pub fn deep_canonicalize(circuit: CircuitRc) -> CircuitRc {
    deep_map_unwrap(&circuit, &canonicalize_node)
}
