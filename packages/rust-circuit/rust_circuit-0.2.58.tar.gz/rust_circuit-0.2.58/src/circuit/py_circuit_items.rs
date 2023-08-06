use super::CircuitRc;
use crate::lazy::GILLazyPy;
use crate::pyo3_prelude::*;

pub struct PyCircuitItems {
    pub computational_node: PyObject,
    pub constant: PyObject,
    pub interop: PyObject,
    pub rust_to_py: PyObject,
    pub circ_compiler_util: PyObject,
}

pub static PY_CIRCUIT_ITEMS: GILLazyPy<PyCircuitItems> = GILLazyPy::new_py(|py| {
    let module = PyModule::from_code(
        py,
        include_str!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/py_circuit_interop.py"
        )),
        concat!(env!("CARGO_MANIFEST_DIR"), "/py_circuit_interop.py"),
        "py_circuit_interop",
    )
    .unwrap(); // TODO: fail more gracefully?

    let get = |s: &str| module.getattr(s).unwrap().into();

    let interop = get("interop");

    PyCircuitItems {
        computational_node: get("computational_node"),
        constant: get("constant"),
        rust_to_py: interop.getattr(py, "rust_to_py").unwrap().into(),
        interop,
        circ_compiler_util: get("circ_compiler_util"),
    }
});

pub fn circuit_rust_to_py(circ: CircuitRc) -> PyObject {
    Python::with_gil(|py| PY_CIRCUIT_ITEMS.rust_to_py.call(py, (circ,), None).unwrap())
}
