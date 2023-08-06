use crate::hashmaps::FxHashMap as HashMap;
use std::iter::zip;

use macro_rules_attribute::apply;

use super::{prelude::*, HashBytes, NamedAxes};
use crate::cached_lambda;
use crate::pyo3_prelude::*;

pub fn set_named_axes<T: CircuitNode + Clone>(node: &T, named_axes: NamedAxes) -> T {
    if let Some(real_named_axes) = &named_axes {
        assert!(real_named_axes.len() == node.info().rank());
    }
    let mut result: T = node.clone();
    result.info_mut().named_axes = named_axes.clone();
    let mut result = result.init_info().unwrap();
    result.info_mut().named_axes = named_axes;
    result
}

#[pyfunction]
#[pyo3(name = "set_named_axes")]
pub fn set_named_axes_py(circuit: CircuitRc, named_axes: NamedAxes) -> CircuitRc {
    set_named_axes(&**circuit, named_axes).rc()
}
pub fn merge_named_axes(a: &NamedAxes, b: &NamedAxes) -> NamedAxes {
    if a.is_none() && b.is_none() {
        return None;
    } else if a.is_some() && b.is_some() {
        let a = a.clone().unwrap();
        let b = b.clone().unwrap();
        assert!(a.len() == b.len());
        Some(
            zip(a, b)
                .map(|(ai, bi)| bi.clone().or(ai.clone()))
                .collect(),
        )
    } else {
        a.clone().or(b.clone())
    }
}

pub fn named_axes_backward<T: CircuitNode + Clone>(
    circuit: &T,
    named_axes: &NamedAxes,
) -> Vec<NamedAxes> {
    let named_axes = named_axes.clone().unwrap();
    let child_axis_map = circuit.child_axis_map();
    child_axis_map
        .iter()
        .map(|z| {
            Some(
                z.iter()
                    .map(|x| (*x).and_then(|i| named_axes[i].clone()))
                    .collect(),
            )
        })
        .collect()
}

#[pyfunction]
pub fn propagate_named_axes(circuit: CircuitRc, named_axes: NamedAxes) -> CircuitRc {
    #[apply(cached_lambda)]
    #[key((circ.info().hash, axes.clone()), (HashBytes, NamedAxes))]
    fn recurse(circ: Circuit, axes: NamedAxes) -> CircuitRc {
        let new_out_axes = merge_named_axes(&circ.info().named_axes, &axes);
        let new_child_axes = named_axes_backward(&circ, &new_out_axes);
        let child_axis_names: HashMap<HashBytes, NamedAxes> = zip(circ.children(), new_child_axes)
            .map(|(c, a)| (c.info().hash, a))
            .collect();

        set_named_axes(&circ, new_out_axes)
            .map_children_unwrap(|childy| {
                recurse(
                    childy.clone(),
                    child_axis_names[&childy.info().hash].clone(),
                )
            })
            .rc()
    }
    recurse((**circuit).clone(), named_axes)
}
