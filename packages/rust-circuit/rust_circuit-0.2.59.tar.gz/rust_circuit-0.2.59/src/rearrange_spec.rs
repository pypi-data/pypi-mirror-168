use crate::circuit::EinsumAxes;
use crate::hashmaps::{AHashSet as HashSet, FxHashMap as HashMap};
use crate::pyo3_prelude::*;
use crate::{
    circuit::py_circuit_items::PY_CIRCUIT_ITEMS,
    circuit::HashBytes,
    smallvec::Sv,
    sv,
    tensor_util::{Shape, TensorInvariantError},
    util::{dict_to_list, filter_out_idx, is_unique, vec_map_insert, EinInt, ALPHABET},
};
use itertools::{izip, Itertools};
use pyo3::exceptions;
use pyo3::types::IntoPyDict;
use std::{fmt::Debug, iter::zip};

use thiserror::Error;
use uuid::uuid;

/// OpSize is a memory optimization of Option<usize> that stores a 63-bit int and one "is this none" bit
#[derive(Copy, Clone, PartialEq, Eq)]
pub struct OpSize(pub u64);
pub type OpShape = Sv<[OpSize; 6]>;

impl OpSize {
    // sometimes into/from can't do type interference, so we have aliases
    fn t(self) -> Option<usize> {
        self.into()
    }

    fn f(val: Option<usize>) -> Self {
        val.into()
    }
    pub fn is_some(&self) -> bool {
        self.0 >> 63 == 0
    }
    pub fn is_none(&self) -> bool {
        self.0 >> 63 != 0
    }
    pub fn unwrap(self) -> u64 {
        assert!(self.is_some());
        self.0
    }
}

impl Debug for OpSize {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.t().fmt(f)
    }
}

impl From<Option<usize>> for OpSize {
    fn from(x: Option<usize>) -> Self {
        assert!(std::mem::size_of::<usize>() <= std::mem::size_of::<u64>()); // optimized out I assume
        match x {
            None => OpSize(1 << 63),
            Some(value) => {
                assert_eq!(value >> 63, 0);
                OpSize(value as u64)
            }
        }
    }
}

impl From<OpSize> for Option<usize> {
    fn from(x: OpSize) -> Self {
        if x.0 >> 63 == 1 {
            None
        } else {
            Some(x.0 as usize)
        }
    }
}

impl<'source> FromPyObject<'source> for OpSize {
    fn extract(obj: &'source PyAny) -> PyResult<Self> {
        Ok(OpSize::f(obj.extract()?))
    }
}

impl IntoPy<PyObject> for OpSize {
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.t().into_py(py)
    }
}

pub fn shape_to_op_shape(shape: &Shape) -> OpShape {
    shape.iter().map(|x| OpSize(*x as u64)).collect()
}

// RInnerInts distribution is heavy tailed - almost everything's 1, but there might be up to 10.
// we use multiple of 8 bc they're u8 and we'd just pad if we used less
pub type RInnerInts = Sv<[EinInt; 8]>;
pub type RInts = Sv<[RInnerInts; 8]>;

#[pyclass]
#[derive(Debug, Clone, PartialEq, Eq, PyClassDeriv)]
pub struct RearrangeSpec {
    #[pyo3(get)]
    pub input_ints: RInts,
    #[pyo3(get)]
    pub output_ints: RInts,
    #[pyo3(get)]
    pub int_sizes: OpShape,
}

#[cfg(not(feature = "real-pyo3"))]
impl<'source> FromPyObject<'source> for RearrangeSpec {
    fn extract(_: &'source PyAny) -> PyResult<Self> {
        unimplemented!()
    }
}

#[cfg(not(feature = "real-pyo3"))]
impl IntoPy<PyObject> for RearrangeSpec {
    fn into_py(self, _: Python<'_>) -> PyObject {
        unimplemented!()
    }
}

/// RearrangeSpec encodes the same thing as a python Einops.repeat string https://einops.rocks/api/repeat/
///
/// Dimension names are encoded as integers, so the einops operation
/// repeat('(a b) -> 10 a b', tensor, a=5) is encoded as
///   input_ints = [[0, 1]]
///   output_ints = [[2], [0], [1]]
///   int_sizes = [Some(5), None, Some(10)]
///
/// If a variable i is only on the right, it is a repeat dimension, and the number of repeats
/// must be specified as int_sizes[i] = Some(repeats).
/// If a variable is on the left, it must appear on the right (we don't allow reductions). This means
/// this doesn't support squeezes normally: '1 a -> a' is not allowed, but unsqueezes are allowed.
/// (You can however get a squeeze by doing '1 a -> (1 a)', although you should use Index instead.)
///
/// Most rearranges don't allocate new memory, including non-flattened repeats (which simply have stride 0).
/// See Rearrange::intermediate_cost_bound for details.
#[pymethods]
impl RearrangeSpec {
    #[new]
    pub fn new(input_ints: RInts, output_ints: RInts, int_sizes: OpShape) -> Self {
        // TODO: validation
        RearrangeSpec {
            input_ints,
            output_ints,
            int_sizes,
        }
    }

    #[staticmethod]
    pub fn flatten(rank: usize) -> Self {
        assert!(rank <= u8::MAX as usize + 1);
        RearrangeSpec {
            input_ints: (0..rank).map(|i| sv![i as u8]).collect(),
            output_ints: sv![(0..rank as u8).collect()],
            int_sizes: sv![OpSize::from(None); rank],
        }
    }

    #[staticmethod]
    pub fn unflatten(shape: Shape) -> Self {
        let rank = shape.len();
        assert!(rank <= u8::MAX as usize + 1);
        RearrangeSpec {
            input_ints: sv![(0..rank as u8).collect()],
            output_ints: (0..rank).map(|i| sv![i as u8]).collect(),
            int_sizes: shape_to_op_shape(&shape),
        }
    }

    #[staticmethod]
    pub fn ident(rank: usize) -> Self {
        RearrangeSpec {
            input_ints: (0..rank).map(|i| sv![i as u8]).collect(),
            output_ints: (0..rank).map(|i| sv![i as u8]).collect(),
            int_sizes: sv![OpSize::from(None); rank],
        }
    }
    pub fn to_py_rearrange_spec(&self, input_shape: Shape) -> PyObject {
        Python::with_gil(|py| {
            PY_CIRCUIT_ITEMS
                .circ_compiler_util
                .getattr(py, "RearrangeSpec")
                .unwrap()
                .getattr(py, "from_rust")
                .unwrap()
                .call(
                    py,
                    (self
                        .canonicalize(true)
                        .conform_to_input_shape(&input_shape, true)
                        .unwrap()
                        .fill_empty_ints(true)
                        .unwrap(),),
                    None,
                )
                .unwrap()
        })
    }
    pub fn ints_in_inp(&self) -> HashSet<EinInt> {
        self.ints_in_inp_it().collect()
    }
    pub fn ints_in_out(&self) -> HashSet<EinInt> {
        self.ints_in_out_it().collect()
    }
    pub fn is_permute(&self) -> bool {
        // because there are no squeezes, all we need is no splits/joins and equal input and output rank
        self.input_ints.iter().all(|x| x.len() == 1)
            && self.output_ints.iter().all(|x| x.len() == 1)
            && self.input_ints.len() == self.output_ints.len()
    }
    pub fn get_fwd_permutation(&self) -> Option<Vec<usize>> {
        if !self.is_permute() {
            return None;
        }
        let output_ints_single: Vec<u8> = self.output_ints.iter().map(|x| x[0]).collect();
        Some(
            self.input_ints
                .iter()
                .map(|ints| {
                    output_ints_single
                        .iter()
                        .position(|in_int| ints[0] == *in_int)
                        .unwrap()
                })
                .collect(),
        )
    }
    pub fn is_identity(&self) -> bool {
        self.input_ints == self.output_ints
    }

    pub fn is_valid(&self) -> bool {
        // check each int appears once in input and output
        let result = self.ints_in_inp_it().unique().count() == self.ints_in_inp_it().count()
            && is_unique(&self.ints_in_out_it().collect::<Vec<EinInt>>());
        // check each input is in output
        let ints_in_out = self.ints_in_out();
        let ints_in_inp = self.ints_in_inp();
        let result = result && ints_in_inp.difference(&ints_in_out).count() == 0;

        // check int_sizes is long enough
        let result = result
            && ints_in_out.iter().max().map(|&i| i as i64).unwrap_or(-1)
                < self.int_sizes.len() as i64;

        // check each int only in output has size
        let only_in_output: Vec<EinInt> = ints_in_out.difference(&ints_in_inp).copied().collect();
        let result = result
            && only_in_output
                .iter()
                .all(|x| self.int_sizes[*x as usize].is_some());
        // check only one wildcard per input axis
        let result = result
            && self.input_ints.iter().all(|x| {
                x.iter()
                    .filter(|y| self.int_sizes[**y as usize].is_none())
                    .count()
                    <= 1
            });
        result
    }

    pub fn to_einops_string(&self) -> String {
        let ints_in_output = self.ints_in_out();

        let input_letters = self
            .input_ints
            .iter()
            .map(|one_axis_ints| {
                let one_axis_letters = one_axis_ints
                    .iter()
                    .map(|i| {
                        if ints_in_output.contains(i) || self.int_sizes[*i as usize].is_none() {
                            ALPHABET[*i as usize].to_owned()
                        } else {
                            self.int_sizes[*i as usize].0.to_string()
                        }
                    })
                    .collect::<Vec<String>>();
                if one_axis_letters.len() == 1 {
                    one_axis_letters[0].to_owned()
                } else {
                    format!("({})", one_axis_letters.join(" "))
                }
            })
            .collect::<Vec<String>>()
            .join(" ");
        let ints_in_input = self.ints_in_inp();
        let output_letters = self
            .output_ints
            .iter()
            .map(|one_axis_ints| {
                let one_axis_letters = one_axis_ints
                    .iter()
                    .map(|i| {
                        if ints_in_input.contains(i) || self.int_sizes[*i as usize].is_none() {
                            ALPHABET[*i as usize].to_owned()
                        } else {
                            self.int_sizes[*i as usize].0.to_string()
                        }
                    })
                    .collect::<Vec<String>>();
                if one_axis_letters.len() == 1 {
                    one_axis_letters[0].to_owned()
                } else {
                    format!("({})", one_axis_letters.join(" "))
                }
            })
            .collect::<Vec<String>>()
            .join(" ");
        input_letters + " -> " + &output_letters
    }
    pub fn letter_sizes(&self) -> Vec<(String, u64)> {
        // because to_einops_string uses numerals on all added dims, we only need letter sizes for splits
        let ints_needing_sizes: HashSet<EinInt> = self
            .input_ints
            .iter()
            .filter(|x| x.len() > 1)
            .flatten()
            .copied()
            .collect();
        ints_needing_sizes
            .into_iter()
            .map(|x| {
                let size_here = self.int_sizes[x as usize];
                assert!(size_here.is_some());
                (ALPHABET[x as usize].to_owned(), size_here.0)
            })
            .collect()
    }
    pub fn to_einops_string_and_letter_sizes(&self) -> (String, Vec<(String, u64)>) {
        (self.to_einops_string(), self.letter_sizes())
    }
    /// apply rearrange to tensor
    pub fn apply(&self, tensor: &PyAny) -> PyResult<Py<PyAny>> {
        let (string, letter_sizes) = self.to_einops_string_and_letter_sizes();
        let result = Python::with_gil(|py| {
            let einops = PyModule::import(py, "einops").unwrap();
            let result = einops
                .getattr("repeat")
                .unwrap()
                .call((tensor, string), Some(letter_sizes.into_py_dict(py)))
                .unwrap();
            result.to_object(py)
        });
        Ok(result)
    }
    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }
    pub fn shapes(&self) -> Result<(Shape, Shape), TensorInvariantError> {
        if self.int_sizes.iter().any(|x| x.is_none()) {
            return Err(TensorInvariantError::RearrangeHasWildcardSizes { spec: self.clone() });
        }
        Ok((
            self.input_ints
                .iter()
                .map(|x| {
                    x.iter()
                        .map(|y| self.int_sizes[*y as usize].0 as usize)
                        .product()
                })
                .collect(),
            self.output_ints
                .iter()
                .map(|x| {
                    x.iter()
                        .map(|y| self.int_sizes[*y as usize].0 as usize)
                        .product()
                })
                .collect(),
        ))
    }
    /// which output axes are introduced entirely by rearrange, eg `a -> a b`->1, `a -> b (a c)`->0
    pub fn out_broadcast_axes(&self) -> Vec<usize> {
        let ints_in_inp = self.ints_in_inp();
        (0..self.output_ints.len())
            .filter(|i| {
                self.output_ints[*i]
                    .iter()
                    .all(|int| !ints_in_inp.contains(int))
            })
            .collect()
    }

    // TODO: Clean up the code examples once we implement RearrangeSpec.from_string
    /// Simplifies a RearrangeSpec using three rules (described below).
    /// # Examples
    /// 1. if special_case_ones, remove all indices of size 1
    /// ```
    /// # use rust_circuit::{sv, rearrange_spec::{OpSize, RearrangeSpec}};
    /// let spec = RearrangeSpec::new(
    ///     sv![sv![0, 1], sv![2, 3]],
    ///     sv![sv![3, 2, 1, 0]],
    ///     sv![OpSize(3), OpSize(1), OpSize(1), OpSize(1)],
    /// );
    /// let canonicalized_spec = RearrangeSpec::new(sv![sv![0], sv![]], sv![sv![0]], sv![OpSize(3)]);
    /// assert_eq!(spec.canonicalize(true), canonicalized_spec);
    /// ```
    /// 2. Merge all sequences of indices that always appear together in the same order inside parentheses
    /// 3. Renumber the int indices sequentially based on when they first appear, inputs first then outputs
    /// ```
    /// # use rust_circuit::{sv, rearrange_spec::{OpSize, RearrangeSpec}};
    /// let spec = RearrangeSpec::new(
    ///     sv![sv![0], sv![1, 2], sv![3, 4, 5]],
    ///     sv![sv![1, 2], sv![5], sv![3, 4], sv![0]],
    ///     sv![
    ///         OpSize(2),
    ///         OpSize(2),
    ///         OpSize(2),
    ///         OpSize(2),
    ///         OpSize(2),
    ///         OpSize(2),
    ///     ],
    /// );
    /// let canonicalized_spec = RearrangeSpec::new(
    ///     sv![sv![0], sv![1], sv![2, 3]],
    ///     sv![sv![1], sv![3], sv![2], sv![0]],
    ///     sv![OpSize(2), OpSize(4), OpSize(4), OpSize(2)],
    /// );
    /// assert_eq!(spec.canonicalize(true), canonicalized_spec);
    /// ```
    #[args(special_case_ones = true)]
    pub fn canonicalize(&self, special_case_ones: bool) -> Self {
        // Remove all indices of size 1
        let int_sizes: Vec<u64> = self.get_unwrapped_sizes();
        let mut input_ints = self.input_ints.clone();
        let mut output_ints = self.output_ints.clone();
        if special_case_ones {
            let drop_einints = |ints_list: RInts| {
                ints_list
                    .iter()
                    .map(|ints| {
                        ints.iter()
                            .filter(|i| int_sizes[**i as usize] != 1)
                            .copied()
                            .collect()
                    })
                    .collect()
            };
            input_ints = drop_einints(input_ints);
            output_ints = drop_einints(output_ints);
        }

        // Find sequences of indices that always appear together by storing the idx ints that
        // appear before and after this idx int
        #[derive(Copy, Clone, PartialEq, Debug)]
        enum SeqPos {
            First,
            Last,
            Middle(EinInt),
        }
        use SeqPos::*;
        let mut prev_idx = vec![None; int_sizes.len()];
        let mut next_idx = vec![None; int_sizes.len()];
        for lst in input_ints.iter().chain(output_ints.iter()) {
            if let (Some(&first), Some(&last)) = (lst.first(), lst.last()) {
                prev_idx[first as usize] = Some(First);
                next_idx[last as usize] = Some(Last);
            }

            for (&prev, &curr) in lst.iter().tuple_windows() {
                let prev_i = prev as usize;
                let curr_i = curr as usize;
                if prev_idx[curr_i].is_none() {
                    prev_idx[curr_i] = Some(Middle(prev));
                }
                if next_idx[prev_i].is_none() {
                    next_idx[prev_i] = Some(Middle(curr));
                }
                if prev_idx[curr_i] != Some(Middle(prev)) || next_idx[prev_i] != Some(Middle(curr))
                {
                    prev_idx[curr_i] = Some(First);
                    next_idx[prev_i] = Some(Last);
                }
            }
        }

        // find the first index in a sequence of repeated indices
        // similar to union find - caches results to make future lookups faster
        fn find(i: EinInt, prev_idx: &mut [Option<SeqPos>]) -> EinInt {
            let mut pos = i;
            while let Some(Middle(prev_pos)) = prev_idx[pos as usize] {
                pos = prev_pos;
            }
            assert!(prev_idx[pos as usize] == Some(First));

            let first_pos = pos;
            pos = i;
            while let Some(Middle(prev_pos)) = prev_idx[pos as usize] {
                prev_idx[pos as usize] = Some(Middle(first_pos));
                pos = prev_pos;
            }
            first_pos
        }

        let mut map: HashMap<EinInt, EinInt> = HashMap::new();
        let mut new_int_sizes: Vec<u64> = Vec::new();
        let mut already_accounted_shape = vec![false; int_sizes.len()];

        let mut merge_tuples_and_renumber_fn = |ints: RInts| {
            ints.iter()
                .map(|single_dim| {
                    let mut new_dim = sv![];
                    for &i in single_dim.iter() {
                        if let Some(&new_i) = map.get(&i) {
                            new_dim.push(new_i);
                        } else if prev_idx[i as usize] == Some(First) {
                            let new_i: u8 = new_int_sizes.len().try_into().unwrap();
                            map.insert(i, new_i);
                            new_dim.push(new_i);
                            new_int_sizes.push(int_sizes[i as usize]);
                        } else if !already_accounted_shape[i as usize] {
                            new_int_sizes[*map.get(&find(i, &mut prev_idx)).unwrap() as usize] *=
                                int_sizes[i as usize];
                            already_accounted_shape[i as usize] = true;
                        }
                    }
                    new_dim
                })
                .collect()
        };

        let input_ints: RInts = merge_tuples_and_renumber_fn(input_ints);
        let output_ints: RInts = merge_tuples_and_renumber_fn(output_ints);

        RearrangeSpec {
            input_ints,
            output_ints,
            int_sizes: new_int_sizes
                .iter()
                .map(|&x| OpSize::from(Some(x as usize)))
                .collect(),
        }
    }

    pub fn fill_empty_ints(
        &self,
        allow_rust_invalid: bool,
    ) -> Result<RearrangeSpec, TensorInvariantError> {
        let mut next_int = self.all_ints().max().map(|i| i + 1).unwrap_or(0);
        let first_int_to_add = next_int;
        let input_ints = self
            .input_ints
            .iter()
            .map(|ints| {
                if ints.is_empty() {
                    next_int += 1;
                    sv![next_int - 1]
                } else {
                    ints.clone()
                }
            })
            .collect();
        let int_after_input = next_int;
        let mut output_ints: RInts = self
            .output_ints
            .iter()
            .map(|ints| {
                if ints.is_empty() {
                    next_int += 1;
                    sv![next_int - 1]
                } else {
                    ints.clone()
                }
            })
            .collect();
        if int_after_input > first_int_to_add {
            if !output_ints.is_empty() {
                output_ints[0].extend(first_int_to_add..int_after_input);
            } else if !allow_rust_invalid {
                return Err(TensorInvariantError::RearrangeNotConvertable { spec: self.clone() });
            }
        }
        let result = RearrangeSpec {
            input_ints,
            output_ints,
            int_sizes: self
                .int_sizes
                .iter()
                .cloned()
                .chain(vec![OpSize(1); (next_int - first_int_to_add) as usize])
                .collect(),
        };
        if !allow_rust_invalid && !result.is_valid() {
            println!("{:?}", result);
            panic!();
        }
        Ok(result)
    }

    #[staticmethod]
    #[pyo3(name = "fuse")]
    pub fn fuse_py(inner: Self, outer: Self) -> PyResult<Self> {
        RearrangeSpec::fuse(&inner, &outer).map_err(Into::into)
    }
    #[pyo3(name = "conform_to_input_shape")]
    fn conform_to_input_shape_py(
        &self,
        shape: Shape,
        coerce: bool,
    ) -> Result<RearrangeSpec, TensorInvariantError> {
        self.conform_to_input_shape(&shape, coerce)
    }
}

impl RearrangeSpec {
    pub fn ints_in_inp_it(&self) -> impl Iterator<Item = EinInt> + '_ {
        self.input_ints.iter().flatten().copied()
    }
    pub fn ints_in_out_it(&self) -> impl Iterator<Item = EinInt> + '_ {
        self.output_ints.iter().flatten().copied()
    }
    /// All integers must occur in the output, so this is valid
    pub fn all_ints(&self) -> impl Iterator<Item = EinInt> + '_ {
        self.ints_in_out_it()
    }

    pub fn new_canon(input_ints: RInts, output_ints: RInts, int_sizes: OpShape) -> Self {
        let result = RearrangeSpec {
            input_ints,
            output_ints,
            int_sizes,
        }
        .canonicalize(true);
        assert!(result.is_valid(), "{:?}", result);
        result
    }

    pub fn conform_to_input_shape(
        &self,
        shape: &Shape,
        coerce: bool, /* if false, only change None sizes, if true, change others if unique solution */
    ) -> Result<RearrangeSpec, TensorInvariantError> {
        if shape.len() != self.input_ints.len() {
            return Err(TensorInvariantError::RearrangeInputNotConformable {
                spec: self.clone(),
                shape: shape.clone(),
            });
        }
        let mut int_sizes = self.int_sizes.clone();
        for (ints, l) in zip(&self.input_ints, shape) {
            let none_indices: Vec<usize> = ints
                .iter()
                .enumerate()
                .filter(|(_i, x)| self.int_sizes[**x as usize].is_none())
                .map(|(i, _x)| i)
                .collect();
            let non_wildcard_size: u64 = ints
                .iter()
                .map(|x| {
                    let size_here = self.int_sizes[*x as usize];
                    if size_here.is_none() {
                        1
                    } else {
                        size_here.0
                    }
                })
                .product();
            if non_wildcard_size != *l as u64 || !none_indices.is_empty() {
                if (none_indices.len() == 1 || none_indices.is_empty() && ints.len() == 1 && coerce)
                    && *l as u64 % non_wildcard_size == 0
                {
                    let mut cur_int = ints[0];
                    if none_indices.len() == 1 {
                        cur_int = ints[none_indices[0]]
                    }
                    let wildcard_size = *l as u64 / non_wildcard_size;
                    int_sizes[cur_int as usize] = OpSize(wildcard_size);
                } else {
                    return Err(TensorInvariantError::RearrangeInputNotConformable {
                        spec: self.clone(),
                        shape: shape.clone(),
                    });
                }
            }
        }
        Ok(Self {
            input_ints: self.input_ints.clone(),
            output_ints: self.output_ints.clone(),
            int_sizes,
        })
    }

    /// use at your own risk, this doesn't check whether resulting rearrange is valid
    pub fn filter_out_axes_unsafe(&self, out_axes_to_skip: &HashSet<usize>) -> RearrangeSpec {
        RearrangeSpec {
            input_ints: self.input_ints.clone(),
            output_ints: filter_out_idx(&self.output_ints, out_axes_to_skip)
                .into_iter()
                .collect(),
            int_sizes: self.int_sizes.clone(),
        }
    }
    /// use at your own risk, this doesn't check whether resulting rearrange is valid
    pub fn filter_all_tuples(&self, tuples_to_skip: &HashSet<Box<[EinInt]>>) -> RearrangeSpec {
        RearrangeSpec {
            input_ints: self
                .input_ints
                .iter()
                .filter(|x| !tuples_to_skip.contains(&x[..]))
                .cloned()
                .collect(),
            output_ints: self
                .output_ints
                .iter()
                .filter(|x| !tuples_to_skip.contains(&x[..]))
                .cloned()
                .collect(),
            int_sizes: self.int_sizes.clone(),
        }
    }

    /// input_ints and output_ints cant contain repeats!
    pub fn unremove_axes(removed_axes: &HashSet<usize>, output_shape: &Shape) -> RearrangeSpec {
        RearrangeSpec {
            input_ints: (0..output_shape.len())
                .filter(|i| !removed_axes.contains(i))
                .map(|i| sv![i as u8])
                .collect(),
            output_ints: (0..output_shape.len()).map(|i| sv![i as u8]).collect(),
            int_sizes: shape_to_op_shape(output_shape),
        }
    }

    pub fn expand(
        input_ints: &EinsumAxes,
        output_ints: &EinsumAxes,
        int_sizes: &HashMap<u8, usize>,
    ) -> RearrangeSpec {
        let int_sizes_usize: HashMap<usize, usize> =
            int_sizes.iter().map(|(k, v)| (*k as usize, *v)).collect();
        RearrangeSpec {
            input_ints: input_ints.iter().map(|i| sv![*i]).collect(),
            output_ints: output_ints.iter().map(|i| sv![*i]).collect(),
            int_sizes: shape_to_op_shape(
                &dict_to_list(&int_sizes_usize, None).into_iter().collect(),
            ),
        }
    }

    pub fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        for axis in self.input_ints.iter() {
            hasher.update(&uuid!("8718e8a1-bf0a-46fe-be66-be8894bc41bd").into_bytes()); // delimit with uuid
            hasher.update(axis);
        }
        for axis in self.output_ints.iter() {
            hasher.update(&uuid!("ebd66768-bb20-43a4-8f5a-fd51e76a0333").into_bytes()); // delimit with uuid
            hasher.update(axis);
        }
        hasher.update(&uuid!("ebd66768-bb20-43a4-8f5a-fd51e76a0333").into_bytes()); // delimit with uuid
        for size in self.int_sizes.iter() {
            hasher.update(&uuid!("ebd66768-bb20-43a4-8f5a-fd51e76a0333").into_bytes()); // delimit with uuid
            hasher.update(&size.0.to_le_bytes());
        }
        hasher.finalize().into()
    }

    fn get_unwrapped_sizes(&self) -> Vec<u64> {
        self.int_sizes.iter().map(|x| x.unwrap()).collect()
    }

    // TODO: Clean up the code examples once we implement RearrangeSpec.from_string
    /// Composes two rearrange specs
    ///
    /// # Examples
    /// ```
    /// # use rust_circuit::{sv, rearrange_spec::{OpSize, RearrangeSpec}};
    /// let inner = RearrangeSpec::new(
    ///     sv![sv![0], sv![1]],
    ///     sv![sv![0, 1]],
    ///     sv![OpSize(2), OpSize(3)],
    /// );
    /// let outer = RearrangeSpec::new(sv![sv![0]], sv![sv![0], sv![1]], sv![OpSize(6), OpSize(4)]);
    /// let fused = RearrangeSpec::new(
    ///     sv![sv![0], sv![1]],
    ///     sv![sv![0, 1], sv![2]],
    ///     sv![OpSize(2), OpSize(3), OpSize(4)],
    /// );
    /// assert_eq!(RearrangeSpec::fuse(&inner, &outer).unwrap(), fused);
    /// ```
    pub fn fuse(inner: &Self, outer: &Self) -> Result<Self, RewriteError> {
        let mut inner_sizes: Vec<u64> = inner.get_unwrapped_sizes();
        let mut outer_sizes: Vec<u64> = outer.get_unwrapped_sizes();
        let mut inner_replaces: HashMap<EinInt, Vec<EinInt>> = HashMap::new();
        let mut outer_replaces: HashMap<EinInt, Vec<EinInt>> = HashMap::new();
        let mut in_to_out: HashMap<EinInt, EinInt> = HashMap::new();

        // if possible, split up inner.outer_ints and outer.inner_ints until they have the same size for each subdimension (if not possible, raise error)
        for (outer_ints, inner_ints) in izip!(&outer.input_ints, &inner.output_ints) {
            let mut new_inner_ints = inner_ints.clone();
            let mut new_outer_ints = outer_ints.clone();
            let mut inner_iter = inner_ints.iter().peekable();
            let mut outer_iter = outer_ints.iter().peekable();
            while let Some(&&in_i) = inner_iter.peek() && let Some(&&out_i) = outer_iter.peek() {
                let in_s = inner_sizes[in_i as usize];
                let out_s = outer_sizes[out_i as usize];
                if in_s == out_s {
                    inner_iter.next();
                    outer_iter.next();
                    in_to_out.insert(in_i, out_i);
                    vec_map_insert(&mut inner_replaces, in_i, in_i);
                    vec_map_insert(&mut outer_replaces, out_i, out_i);
                } else {
                    let (
                        old_i,
                        new_i,
                        small_i,
                        small_s,
                        small_iter,
                        small_replaces,
                        big_s,
                        big_ints,
                        big_sizes,
                        big_replaces,
                    ) = if in_s > out_s {
                        (
                            in_i,
                            inner_sizes.len().try_into().unwrap(),
                            out_i,
                            out_s,
                            &mut outer_iter,
                            &mut outer_replaces,
                            in_s,
                            &mut new_inner_ints,
                            &mut inner_sizes,
                            &mut inner_replaces,
                        )
                    } else {
                        (
                            out_i,
                            outer_sizes.len().try_into().unwrap(),
                            in_i,
                            in_s,
                            &mut inner_iter,
                            &mut inner_replaces,
                            out_s,
                            &mut new_outer_ints,
                            &mut outer_sizes,
                            &mut outer_replaces,
                        )
                    };

                    if big_s % small_s != 0 {
                        return Err(RewriteError::RearrangeNotFusable { inner:inner.clone(), outer:outer.clone() });
                    }
                    if in_s > out_s {
                        in_to_out.insert(new_i, out_i);
                    } else {
                        in_to_out.insert(in_i, new_i);
                    }
                    small_iter.next();
                    big_ints.push(new_i);
                    big_sizes[old_i as usize] /= small_s;
                    big_sizes.push(small_s);
                    vec_map_insert(small_replaces, small_i, small_i);
                    vec_map_insert(big_replaces, old_i, new_i);
                }
            }

            if inner_iter.any(|&i| inner_sizes[i as usize] != 1)
                || outer_iter.any(|&i| outer_sizes[i as usize] != 1)
            {
                return Err(RewriteError::RearrangeNotFusable {
                    inner: inner.clone(),
                    outer: outer.clone(),
                });
            }
        }

        // update inner.inner_ints and outer.inner_ints using the splits we generated above
        fn expand_dims(
            all_dim_ints: &[RInnerInts],
            replaces: &mut HashMap<EinInt, Vec<EinInt>>,
        ) -> RInts {
            all_dim_ints
                .iter()
                .map(|dim_ints| {
                    dim_ints
                        .iter()
                        .flat_map(|dim_int| {
                            replaces.remove(dim_int).unwrap_or_else(|| vec![*dim_int])
                        })
                        .collect()
                })
                .collect()
        }
        let input_ints: RInts = expand_dims(&inner.input_ints, &mut inner_replaces);
        let output_ints: RInts = expand_dims(&outer.output_ints, &mut outer_replaces);

        // change inputs to use output labels and drop input terms that don't have a mapping
        // (this should only happen if those indices have size 1)
        let input_ints: RInts = input_ints
            .iter()
            .map(|dim_ints| {
                dim_ints
                    .iter()
                    .filter_map(|dim_int| in_to_out.get(dim_int).copied())
                    .collect()
            })
            .collect();

        Ok(Self {
            input_ints,
            output_ints,
            int_sizes: outer_sizes
                .iter()
                .map(|&x| OpSize::from(Some(x as usize)))
                .collect(),
        }
        .canonicalize(true))
    }
}

#[derive(Debug, Error)]
pub enum RewriteError {
    #[error("Rearranges can't be fused, {inner:?}\n{outer:?}")]
    RearrangeNotFusable {
        inner: RearrangeSpec,
        outer: RearrangeSpec,
    },
}

impl From<RewriteError> for PyErr {
    fn from(err: RewriteError) -> Self {
        PyErr::new::<exceptions::PyValueError, _>(format!("error {}", err))
    }
}
