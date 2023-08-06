#![feature(core_intrinsics)]
#![feature(map_first_last)]
// Personally, I like or_fun_call as a lint. But currently code fails...
#![allow(clippy::too_many_arguments, clippy::or_fun_call)]

/// reexport
pub use pyo3;
pub use uuid;

#[cfg(not(feature = "real-pyo3"))]
mod pyo3_prelude {
    pub use fake_pyo3::noop as pymethods;
    pub use fake_pyo3::noop as getter;
    pub use fake_pyo3::noop as pyclass;
    pub use fake_pyo3::noop as pyfunction;
    pub use fake_pyo3::noop as pymodule;
    pub use fake_pyo3::noop as new;
    pub use fake_pyo3::noop as args;
    pub use fake_pyo3::noop as pyo3;
    pub use fake_pyo3::noop as staticmethod;
    /// This class ignores pyo3 attributes
    pub use fake_pyo3::FakePyClassDeriv as PyClassDeriv;
    pub use pyo3::prelude::{
        wrap_pyfunction, FromPyObject, GILGuard, IntoPy, IntoPyPointer, Py, PyAny, PyCell,
        PyClassInitializer, PyErr, PyModule, PyObject, PyRef, PyRefMut, PyResult, PyTryFrom,
        PyTryInto, Python, ToPyObject,
    };
}
#[cfg(feature = "real-pyo3")]
mod pyo3_prelude {
    pub use fake_pyo3::NoopPyClassDeriv as PyClassDeriv;
    pub use pyo3::prelude::*;
}

use crate::pyo3_prelude::*;

pub mod all_imports;
mod caching;
pub mod circuit;
pub mod hashmaps;
pub mod lazy;
pub mod opt_einsum;
pub mod py_types;
pub mod rearrange_spec;
pub mod smallvec;
pub mod tensor_util;
mod union_find;
pub mod util;

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[cfg(feature = "real-pyo3")]
#[pymodule]
fn rust_circuit(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    use circuit::algebraic_rewrite::{
        add_collapse_scalar_inputs, add_deduplicate, add_elim_zeros, add_flatten_once,
        add_make_broadcasts_explicit, add_pull_removable_axes, concat_elim_identity,
        concat_merge_uniform, concat_pull_removable_axes, concat_repeat_to_rearrange,
        deep_optimize_einsums, distribute, distribute_all, einsum_elim_identity, einsum_elim_zero,
        einsum_flatten_once, einsum_merge_scalars, einsum_nest_optimize, einsum_nest_path,
        einsum_of_permute_merge, einsum_pull_removable_axes, extract_add,
        generalfunction_pull_removable_axes, index_elim_identity, index_fuse, index_merge_scalar,
        index_split_axes, permute_of_einsum_merge, push_down_index, rearrange_elim_identity,
        rearrange_fuse, rearrange_merge_scalar, remove_add_few_input,
    };
    use circuit::batching::{batch_inputs_axis_len, batch_largest};
    use circuit::canonicalize::{canonicalize_node_py, deep_canonicalize};
    use circuit::circuit_manipulation::{
        deep_map_preorder_py, deep_map_py, filter_nodes_py, path_get, replace_nodes_py,
        update_nodes_py, update_path_py,
    };
    use circuit::circuit_optimizer::{optimize_and_evaluate, optimize_and_evaluate_many};
    use circuit::circuit_utils::{
        cast_circuit, count_nodes, toposort_circuit, total_arrayconstant_size, total_flops,
    };
    use circuit::compiler_heuristics::deep_maybe_distribute_py;
    use circuit::compiler_strip::strip_names;
    use circuit::concat_rewrite::{
        add_pull_concat, concat_drop_size_zero, concat_fuse, einsum_pull_concat,
        generalfunction_pull_concat, index_concat_drop_unreached, split_to_concat,
    };
    use circuit::deep_rewrite::{
        compiler_simp_py, compiler_simp_step_py, compiler_simp_until_same,
        deep_heuristic_nest_adds, deep_pull_concat, deep_pull_concat_messy, deep_push_down_index,
    };
    use circuit::diag_rewrite::{add_pull_diags, einsum_push_down_trace};
    use circuit::flat_concat;
    use circuit::named_axes::{propagate_named_axes, set_named_axes_py};
    use circuit::scatter_rewrite::{
        add_pull_scatter, einsum_pull_scatter, index_einsum_to_scatter, scatter_elim_identity,
        scatter_pull_removable_axes, scatter_to_concat,
    };
    use circuit::scheduled_execution::{scheduled_evaluate, PyOOMError};
    use opt_einsum::optimize_einsum_spec_cached;
    use pyo3::exceptions::PyValueError;

    // we assume throughout the codebase that usize is 8 bytes, and otherwise error here
    if !core::mem::size_of::<usize>() == 8 {
        return PyResult::Err(PyValueError::new_err("Only supports x64"));
    }

    m.add_class::<circuit::PyCircuitBase>()?;

    m.add_class::<rearrange_spec::RearrangeSpec>()?;
    m.add_class::<circuit::GeneralFunctionSpec>()?;
    m.add_class::<opt_einsum::EinsumSpec>()?;

    m.add_class::<circuit::Einsum>()?;
    m.add_class::<circuit::ArrayConstant>()?;
    m.add_class::<circuit::Symbol>()?;
    m.add_class::<circuit::ScalarConstant>()?;
    m.add_class::<circuit::Add>()?;
    m.add_class::<circuit::Rearrange>()?;
    m.add_class::<circuit::Index>()?;
    m.add_class::<circuit::GeneralFunction>()?;
    m.add_class::<circuit::Concat>()?;
    m.add_class::<circuit::Scatter>()?;
    m.add_class::<circuit::circuit_optimizer::OptimizationSettings>()?;
    m.add("PyOOMError", py.get_type::<PyOOMError>())?;

    m.add_class::<tensor_util::TorchDeviceDtype>()?;
    m.add_class::<tensor_util::TorchDeviceDtypeOp>()?;

    m.add_class::<circuit::PyGFSpecShapeGetter>()?;

    m.add_class::<circuit::scheduled_execution::Schedule>()?;
    m.add_class::<circuit::scheduled_execution::ScheduleStats>()?;

    m.add_function(wrap_pyfunction!(add_collapse_scalar_inputs, m)?)?;
    m.add_function(wrap_pyfunction!(add_deduplicate, m)?)?;
    m.add_function(wrap_pyfunction!(remove_add_few_input, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_flatten_once, m)?)?;
    m.add_function(wrap_pyfunction!(add_flatten_once, m)?)?;

    m.add_function(wrap_pyfunction!(einsum_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(index_merge_scalar, m)?)?;
    m.add_function(wrap_pyfunction!(index_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(index_fuse, m)?)?;
    m.add_function(wrap_pyfunction!(rearrange_fuse, m)?)?;
    m.add_function(wrap_pyfunction!(rearrange_merge_scalar, m)?)?;
    m.add_function(wrap_pyfunction!(rearrange_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(concat_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(concat_merge_uniform, m)?)?;
    m.add_function(wrap_pyfunction!(generalfunction_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(concat_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(add_make_broadcasts_explicit, m)?)?;
    m.add_function(wrap_pyfunction!(distribute, m)?)?;
    m.add_function(wrap_pyfunction!(distribute_all, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_of_permute_merge, m)?)?;
    m.add_function(wrap_pyfunction!(permute_of_einsum_merge, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_elim_zero, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_merge_scalars, m)?)?;
    m.add_function(wrap_pyfunction!(push_down_index, m)?)?;
    m.add_function(wrap_pyfunction!(index_split_axes, m)?)?;
    m.add_function(wrap_pyfunction!(add_elim_zeros, m)?)?;

    m.add_function(wrap_pyfunction!(compiler_simp_py, m)?)?;
    m.add_function(wrap_pyfunction!(compiler_simp_step_py, m)?)?;
    m.add_function(wrap_pyfunction!(compiler_simp_until_same, m)?)?;
    m.add_function(wrap_pyfunction!(deep_canonicalize, m)?)?;
    m.add_function(wrap_pyfunction!(canonicalize_node_py, m)?)?;

    m.add_function(wrap_pyfunction!(strip_names, m)?)?;
    m.add_function(wrap_pyfunction!(deep_maybe_distribute_py, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit::compiler_heuristics::maybe_distribute_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(einsum_nest_path, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_nest_optimize, m)?)?;
    m.add_function(wrap_pyfunction!(deep_optimize_einsums, m)?)?;

    m.add_function(wrap_pyfunction!(index_einsum_to_scatter, m)?)?;
    m.add_function(wrap_pyfunction!(scatter_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_pull_scatter, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_scatter, m)?)?;
    m.add_function(wrap_pyfunction!(scatter_pull_removable_axes, m)?)?;

    m.add_function(wrap_pyfunction!(cast_circuit, m)?)?;
    m.add_function(wrap_pyfunction!(count_nodes, m)?)?;
    m.add_function(wrap_pyfunction!(total_flops, m)?)?;
    m.add_function(wrap_pyfunction!(total_arrayconstant_size, m)?)?;

    m.add_function(wrap_pyfunction!(
        circuit::circuit_optimizer::optimize_circuit_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(optimize_einsum_spec_cached, m)?)?;
    m.add_function(wrap_pyfunction!(scatter_to_concat, m)?)?;
    m.add_function(wrap_pyfunction!(scheduled_evaluate, m)?)?;
    m.add_function(wrap_pyfunction!(optimize_and_evaluate, m)?)?;
    m.add_function(wrap_pyfunction!(optimize_and_evaluate_many, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit::circuit_optimizer::optimize_to_schedule,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit::circuit_optimizer::optimize_to_schedule_many,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(flat_concat, m)?)?;
    m.add_function(wrap_pyfunction!(deep_heuristic_nest_adds, m)?)?;
    m.add_function(wrap_pyfunction!(concat_fuse, m)?)?;
    m.add_function(wrap_pyfunction!(generalfunction_pull_concat, m)?)?;
    m.add_function(wrap_pyfunction!(index_concat_drop_unreached, m)?)?;
    m.add_function(wrap_pyfunction!(concat_drop_size_zero, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_pull_concat, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_concat, m)?)?;
    m.add_function(wrap_pyfunction!(split_to_concat, m)?)?;
    m.add_function(wrap_pyfunction!(deep_push_down_index, m)?)?;
    m.add_function(wrap_pyfunction!(deep_pull_concat_messy, m)?)?;
    m.add_function(wrap_pyfunction!(deep_pull_concat, m)?)?;
    m.add_function(wrap_pyfunction!(batch_inputs_axis_len, m)?)?;
    m.add_function(wrap_pyfunction!(batch_largest, m)?)?;
    m.add_function(wrap_pyfunction!(set_named_axes_py, m)?)?;
    m.add_function(wrap_pyfunction!(propagate_named_axes, m)?)?;
    m.add_function(wrap_pyfunction!(toposort_circuit, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_diags, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_push_down_trace, m)?)?;
    m.add_function(wrap_pyfunction!(concat_repeat_to_rearrange, m)?)?;
    m.add_function(wrap_pyfunction!(extract_add, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit::scatter_rewrite::concat_to_scatter,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit::debugging::opt_eval_each_subcircuit_until_fail,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit::algebraic_rewrite::add_outer_product_broadcasts_on_top,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit::circuit_utils::replace_all_randn_seeded,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(
        circuit::print::rust_expression_notation_circuit,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(deep_map_preorder_py, m)?)?;
    m.add_function(wrap_pyfunction!(deep_map_py, m)?)?;
    m.add_function(wrap_pyfunction!(filter_nodes_py, m)?)?;
    m.add_function(wrap_pyfunction!(replace_nodes_py, m)?)?;
    m.add_function(wrap_pyfunction!(update_nodes_py, m)?)?;
    m.add_function(wrap_pyfunction!(path_get, m)?)?;
    m.add_function(wrap_pyfunction!(update_path_py, m)?)?;

    // add more py function as desired or whatever...
    Ok(())
}
