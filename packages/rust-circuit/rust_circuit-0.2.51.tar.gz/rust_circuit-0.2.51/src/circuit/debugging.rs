use crate::hashmaps::FxHashMap as HashMap;
use std::io::{Read, Write};

use crate::circuit::circuit_optimizer::OptimizationContext;
use crate::circuit::HashBytes;
use num_bigint::BigUint;

use super::{
    circuit_manipulation::replace_nodes,
    circuit_optimizer::{optimize_and_evaluate, optimize_circuit, OptimizationSettings},
    circuit_utils::toposort_circuit,
    evaluate_fn,
    print::rust_expression_notation_circuit,
    ArrayConstant, Circuit, CircuitNode, CircuitRc,
};
use crate::py_types::{Tensor, PY_TORCH};
use pyo3::prelude::*;

/// We need this to redirect Python stdout to Rust stdout
/// If we don't do this, then Python will print to its own stdout, which is not captured by Rust
/// so you only see the output if your entry point is a Python script
#[pyclass]
struct LoggingStdout;

#[pymethods]
impl LoggingStdout {
    fn write(&self, data: &str) {
        println!("{}", data);
    }
}

/// Print Python objects with Python's print function
pub fn python_print(obj: &PyObject) {
    Python::with_gil(move |py| {
        // import print and overwrite stdout with our logging stdout
        let builtins = py.import("builtins").unwrap();
        let sys = py.import("sys").unwrap();
        let prev = sys.getattr("stdout").unwrap();
        sys.setattr("stdout", LoggingStdout.into_py(py)).unwrap();
        let print = builtins.getattr("print").unwrap();
        // print(obj)
        print.call((obj,), None).unwrap();
        // restore stdout
        sys.setattr("stdout", prev).unwrap();
    });
}

pub fn is_close(a: Tensor, b: Tensor) -> Result<PyObject, PyErr> {
    Python::with_gil(|py| {
        PY_TORCH
            .getattr(py, "testing")
            .unwrap()
            .getattr(py, "assert_close")
            .unwrap()
            .call(py, (a, b), None)
    })
}

pub fn assert_is_close(a: CircuitRc, b: CircuitRc) {
    let a_ten = evaluate_fn(&a).unwrap();
    let b_ten = evaluate_fn(&b).unwrap();
    let close_result = is_close(a_ten.clone(), b_ten.clone());
    if close_result.is_err() {
        println!("{:?}", close_result);
        println!("LHS: {}", rust_expression_notation_circuit(a));
        println!("RHS: {}", rust_expression_notation_circuit(b));
        python_print(a_ten.tensor());
        python_print(b_ten.tensor());
        panic!("circuits did not evaluate to the same tensors");
    }
}

#[pyfunction]
pub fn opt_eval_each_subcircuit_until_fail(circuit: CircuitRc, settings: OptimizationSettings) {
    let max_numel = BigUint::from(2_000_000_000usize);
    let topo = toposort_circuit(circuit);
    for circ in topo {
        if circ.info().numel() < max_numel {
            let reference = evaluate_fn(&circ).unwrap();
            let optimized = optimize_and_evaluate(circ.clone(), settings);
            if optimized.is_ok() {
                let optimized = optimized.unwrap();
                let close_result = is_close(reference, optimized);
                if close_result.is_err() {
                    println!("{:?}", close_result);
                    circ.compiler_print();
                    optimize_circuit(
                        circ,
                        &mut OptimizationContext {
                            settings,
                            cache: Default::default(),
                        },
                    )
                    .compiler_print();
                }
            }
        }
    }
}

/// Replaces all great-grandchildren of the circuit with normal random array constants
///
/// Note: given an output of this function `ablated`, any current rewrite satisfies
/// `ablated == rewrite(ablated)`. However, if you serialize both sides to Rust via
/// rust_expression_notation_circuit the results may differ. For a concrete example,
/// take Index(Index(X, tensor1), tensor2), which can be simplified to Index(X, tensor3)
pub fn randn_ablate_great_grandchildren(circ: CircuitRc) -> CircuitRc {
    let great_grandchildren = circ
        .children()
        .flat_map(|child| child.children().collect::<Vec<_>>())
        .flat_map(|grandchild| grandchild.children().collect::<Vec<_>>());
    let mut replacements: HashMap<HashBytes, CircuitRc> = HashMap::new();
    for great_grandchild in great_grandchildren {
        let ablated = Circuit::ArrayConstant(ArrayConstant::randn_seeded(
            great_grandchild.info().shape.clone(),
            great_grandchild.name_cloned(),
            great_grandchild.info().device_dtype.clone(),
            great_grandchild.info().hash_usize(),
        ))
        .rc();
        replacements.insert(great_grandchild.info().hash, ablated);
    }
    replace_nodes(circ, &replacements)
}

/// Takes two supposedly equivalent circuits and
/// 1. Asserts the two circuits evaluate to the same value
/// 2. Appends a test case to the miscompile_tests.rs file (if it doesn't already exist and they evaluated to the same value)
///
/// **Assumes the working directory is the parent of the crate root, ie interp/circuit**
/// You will get file not found errors otherwise
pub fn create_circuit_test(
    prefix: &str,
    a: CircuitRc,
    b: CircuitRc,
) -> Result<(), Box<dyn std::error::Error>> {
    let max_numel = BigUint::from(2_000_000_000usize);
    if a.info().numel() >= max_numel || b.info().numel() >= max_numel {
        return Ok(()); // too big to test
    }
    if a.info().hash == b.info().hash {
        return Ok(()); // too trivial to write a test for
    }

    // check that they're equal right now
    assert_is_close(a.clone(), b.clone());

    // append to testing file if we don't have it already (compare hashes)
    let name = format!(
        "test_{}_{}_{}",
        prefix,
        a.info().hash_usize(),
        b.info().hash_usize()
    );
    let a_str = rust_expression_notation_circuit(a);
    let b_str = rust_expression_notation_circuit(b);
    let test = format!(
        "#[test]\
        \nfn {}() {{\
        \n    pyo3::prepare_freethreaded_python();\
        \n    let a = {};\
        \n    let b = {};\
        \n    assert_is_close(a, b);\
        \n}}\n",
        name,
        a_str.replace('\n', "\n    "),
        b_str.replace('\n', "\n    ")
    );

    let mut file = std::fs::OpenOptions::new()
        .read(true)
        .append(true)
        .open("rust_circuit/tests/miscompile_tests.rs")
        .map_err(|e| {
            format!("rust_circuit create test failed, you probably need to run your Python script with interp/circuit as your working directory. Original error: {}", e)
        })?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    if !contents.contains(name.as_str()) {
        file.write_all(test.as_bytes())?;
    }
    Ok(())
}
