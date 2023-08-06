use crate::pyo3_prelude::*;

use super::{deep_map_unwrap, CircuitNode, CircuitRc};

#[pyfunction]
pub fn strip_names(circuit: CircuitRc) -> CircuitRc {
    deep_map_unwrap(&circuit, |c| c.clone().rename(None).rc())
}
