use crate::pyo3_prelude::*;

use super::{deep_map_unwrap, visit_circuit, CircuitNode, CircuitRc};

#[pyfunction]
pub fn strip_names(circuit: CircuitRc) -> CircuitRc {
    let result = deep_map_unwrap(&circuit, |c| c.clone().rename(None).rc());
    let mut seen_name = false;
    visit_circuit(&result, |x| {
        seen_name = seen_name || x.name().is_some();
    });
    if seen_name {
        result.compiler_print();
        panic!();
    }
    result
}
