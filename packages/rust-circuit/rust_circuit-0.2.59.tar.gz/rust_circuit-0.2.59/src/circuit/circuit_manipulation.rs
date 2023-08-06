use super::{
    deep_map, deep_map_preorder, deep_map_unwrap_preorder, prelude::*, visit_circuit,
    visit_circuit_fallable, HashBytes,
};
use crate::hashmaps::{AHashSet as HashSet, FxHashMap as HashMap};
use crate::pycall;
use pyo3::{pyfunction, PyObject, Python};

pub fn filter_nodes(circuit: CircuitRc, filter: &dyn Fn(&Circuit) -> bool) -> HashSet<CircuitRc> {
    let mut result: HashSet<CircuitRc> = HashSet::new();
    visit_circuit(&circuit, |circuit| {
        if filter(circuit) {
            result.insert(circuit.clone().rc());
        }
    });
    result
}

#[pyfunction]
#[pyo3(name = "filter_nodes")]
pub fn filter_nodes_py(
    circuit: CircuitRc,
    filter: PyObject,
) -> Result<HashSet<CircuitRc>, CircuitConstructionError> {
    let mut result: HashSet<CircuitRc> = HashSet::new();
    let err = visit_circuit_fallable(&circuit, |circuit| {
        let filter_result: Result<_, CircuitConstructionError> =
            pycall!(filter, (circuit.clone().rc(),), CircuitConstructionError);
        let filter_result = filter_result?;
        if filter_result {
            result.insert(circuit.clone().rc());
        }
        Ok(())
    });
    err.map(|_x| result)
}

#[pyfunction]
#[pyo3(name = "replace_nodes")]
pub fn replace_nodes_py(circuit: CircuitRc, map: HashMap<CircuitRc, CircuitRc>) -> CircuitRc {
    deep_map_unwrap_preorder(&circuit, |x: &Circuit| -> CircuitRc {
        let rc = x.clone().rc();
        map.get(&rc).cloned().unwrap_or(rc)
    })
}

/// Replaces child nodes recursively with a mapping
/// In pre-order so that high level nodes are replaced first
pub fn replace_nodes(circuit: CircuitRc, map: &HashMap<HashBytes, CircuitRc>) -> CircuitRc {
    deep_map_unwrap_preorder(&circuit, |x: &Circuit| -> CircuitRc {
        let rc = x.clone().rc();
        map.get(&rc.info().hash).cloned().unwrap_or(rc)
    })
}

#[pyfunction]
#[pyo3(name = "deep_map_preorder")]
pub fn deep_map_preorder_py(
    circuit: CircuitRc,
    f: PyObject,
) -> Result<CircuitRc, CircuitConstructionError> {
    deep_map_preorder(
        &circuit,
        |x: &Circuit| -> Result<CircuitRc, CircuitConstructionError> {
            pycall!(f, (x.clone().rc(),), CircuitConstructionError)
        },
    )
}

#[pyfunction]
#[pyo3(name = "deep_map")]
pub fn deep_map_py(circuit: CircuitRc, f: PyObject) -> Result<CircuitRc, CircuitConstructionError> {
    deep_map(&circuit, &|x: &Circuit| -> Result<
        CircuitRc,
        CircuitConstructionError,
    > {
        pycall!(f, (x.clone().rc(),), CircuitConstructionError)
    })
}

#[pyfunction]
#[pyo3(name = "update_nodes")]
pub fn update_nodes_py(
    circuit: CircuitRc,
    matcher: PyObject,
    updater: PyObject,
) -> Result<CircuitRc, CircuitConstructionError> {
    let nodes = filter_nodes_py(circuit.clone(), matcher)?;
    deep_map_preorder(&circuit, |x| {
        let xcloned = x.clone().rc();
        if nodes.contains(&xcloned) {
            pycall!(updater, (xcloned,), CircuitConstructionError)
        } else {
            Ok(xcloned)
        }
    })
}

pub type CircuitPath = Vec<usize>;

#[pyfunction]
pub fn path_get(circuit: CircuitRc, path: CircuitPath) -> Option<CircuitRc> {
    let mut cur = circuit;
    for i in path {
        let children: Vec<CircuitRc> = cur.children().collect();
        if i >= children.len() {
            return None;
        }
        cur = children[i].clone()
    }
    Some(cur)
}

pub fn update_path<F>(
    circuit: &Circuit,
    path: &CircuitPath,
    updater: F,
) -> Result<CircuitRc, CircuitConstructionError>
where
    F: Fn(&Circuit) -> Result<CircuitRc, CircuitConstructionError>,
{
    fn recurse<F>(
        circuit: &Circuit,
        path: &CircuitPath,
        path_idx: usize,
        updater: &F,
    ) -> Result<CircuitRc, CircuitConstructionError>
    where
        F: Fn(&Circuit) -> Result<CircuitRc, CircuitConstructionError>,
    {
        if path_idx == path.len() {
            return updater(circuit);
        }
        circuit
            .map_children_enumerate(|i, circuit| {
                if i == path[path_idx] {
                    recurse(circuit, path, path_idx + 1, updater)
                } else {
                    Ok(circuit.clone().rc())
                }
            })
            .map(|z| z.rc())
    }
    recurse(circuit, path, 0, &updater)
}

#[pyfunction]
#[pyo3(name = "update_path")]
pub fn update_path_py(
    circuit: CircuitRc,
    path: CircuitPath,
    updater: PyObject,
) -> Result<CircuitRc, CircuitConstructionError> {
    update_path(&circuit, &path, |x| {
        pycall!(updater, (x.clone().rc(),), CircuitConstructionError)
    })
}
