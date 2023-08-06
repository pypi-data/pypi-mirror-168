use super::{
    concat_rewrite::{split_sections, split_to_concat},
    deep_map_op,
    deep_rewrite::deep_pull_concat,
    prelude::*,
};
use crate::pyo3_prelude::*;
use crate::tensor_util::TensorAxisIndex;
use num_bigint::BigUint;

#[pyfunction]
pub fn batch_inputs_axis_len(
    circuit: CircuitRc,
    axis_len: usize,
    num_batches: usize,
    min_size: Option<usize>,
) -> CircuitRc {
    let sections = split_sections(axis_len, num_batches);
    let with_concatted_inputs = deep_map_op(&circuit, &|x: &Circuit| {
        if min_size
            .map(|ms| x.info().numel() > BigUint::from(ms))
            .unwrap_or(true)
        {
            if let Some(pos) = match x {
                Circuit::ArrayConstant(ac) => ac.info().shape.iter().position(|l| *l == axis_len),
                Circuit::Index(index) => index.index.0.iter().position(|l| {
                    if let TensorAxisIndex::Tensor(t) = l {
                        t.shape()[0] == axis_len
                    } else {
                        false
                    }
                }),
                _ => None,
            } {
                return Some(split_to_concat(x.clone().rc(), pos, sections.clone()).rc());
            }
        }
        None
    })
    .unwrap();
    deep_pull_concat(with_concatted_inputs, min_size)
}

#[pyfunction]
pub fn batch_largest(
    circuit: CircuitRc,
    num_batches: usize,
    min_size_to_batch: Option<usize>,
) -> CircuitRc {
    let biggest_numel = circuit.max_non_input_size();
    let with_concats = deep_map_op(&circuit, &|x: &Circuit| {
        if x.info().numel() == biggest_numel {
            let sections = split_sections(x.info().shape[0], num_batches);
            return Some(split_to_concat(x.clone().rc(), 0, sections).rc());
        }
        None
    })
    .unwrap();
    deep_pull_concat(with_concats, min_size_to_batch)
}
