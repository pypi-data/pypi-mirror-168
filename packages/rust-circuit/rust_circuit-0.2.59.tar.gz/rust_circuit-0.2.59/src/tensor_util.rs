use crate::hashmaps::FxHashMap as HashMap;
use crate::py_types::PY_UTILS;
use crate::smallvec::Sv;
use crate::{
    circuit::{CircuitConstructionError, HashBytes},
    filter_by_variant,
    py_types::Tensor,
    pycall,
    rearrange_spec::RearrangeSpec,
};
use crate::{pyo3_prelude::*, sv};
use pyo3::types::IntoPyDict;
use pyo3::{
    exceptions, ffi, pyclass, pymethods,
    types::{PySlice, PyTuple},
    AsPyPointer, FromPyObject, IntoPy, PyAny, PyErr, PyObject, PyResult, Python, ToPyObject,
};
use std::{
    cmp::{max, min},
    fmt::{self, Display},
    iter::zip,
};

use thiserror::Error;
use uuid::uuid;

use super::py_types::ExtraPySelfOps;

// make me small vec for perf
pub type Shape = Sv<[usize; 6]>; // TODO: maybe this should be struct which preserves invariant that dim shapes >= 0?

#[derive(Error, Debug, Clone)]
pub enum TensorInvariantError {
    #[error("Shapes aren't broadcastable, {shapes:?}")]
    NotBroadcastable { shapes: Vec<Shape> },
    #[error("RearrangeSpec not conformable, {spec:?} {shape:?}")]
    RearrangeInputNotConformable { spec: RearrangeSpec, shape: Shape },

    #[error("RearrangeSpec has wildcard sizes, {spec:?}=")]
    RearrangeHasWildcardSizes { spec: RearrangeSpec },

    #[error("RearrangeSpec cannot be converted to no-(), no-squeeze format, {spec:?}=")]
    RearrangeNotConvertable { spec: RearrangeSpec },
}

impl From<TensorInvariantError> for PyErr {
    fn from(err: TensorInvariantError) -> Self {
        PyErr::new::<exceptions::PyValueError, _>(format!("error (TODO: better) {}", err))
    }
}
pub fn broadcast_shapes(shapes: &Vec<Shape>) -> Result<Shape, TensorInvariantError> {
    if shapes.is_empty() {
        return Ok(sv![]);
    }
    let ranks: Vec<usize> = shapes.iter().map(|x| x.len()).collect();
    let out_rank = *ranks.iter().max().unwrap();
    let mut result: Shape = sv![1; out_rank];
    for axis_from_end in 1..out_rank + 1 {
        for (i, shape) in shapes.iter().enumerate() {
            let axis_for_shape = ranks[i].checked_sub(axis_from_end);
            match axis_for_shape {
                None => {}
                Some(j) => {
                    let axis_len = shape[j];
                    if axis_len == 0
                        || axis_len != 1
                            && result[out_rank - axis_from_end] != 1
                            && result[out_rank - axis_from_end] != axis_len
                    {
                        return Err(TensorInvariantError::NotBroadcastable {
                            shapes: shapes.to_owned(),
                        });
                    }
                    result[out_rank - axis_from_end] =
                        max(axis_len, result[out_rank - axis_from_end]);
                }
            }
        }
    }
    Ok(result)
}

// we could bit pack if we wanted...
#[derive(Debug, Clone, Copy)]
pub struct Slice {
    pub start: Option<i64>,
    pub stop: Option<i64>,
}

impl Slice {
    pub fn to_unsigned_loc(x: i64, l: usize) -> usize {
        if x < 0 {
            l.saturating_sub((-x) as usize)
        } else {
            l.min(x as usize)
        }
    }

    fn start_u(self, l: usize) -> usize {
        self.start.map(|x| Self::to_unsigned_loc(x, l)).unwrap_or(0)
    }

    fn stop_u(self, l: usize) -> usize {
        self.stop.map(|x| Self::to_unsigned_loc(x, l)).unwrap_or(l)
    }

    fn size(self, l: usize) -> usize {
        self.stop_u(l).saturating_sub(self.start_u(l))
    }

    fn canonicalize(self, l: usize) -> Self {
        Self {
            start: Some(self.start_u(l) as i64),
            stop: Some(self.stop_u(l) as i64),
        }
    }

    fn update_hash(self, hasher: &mut blake3::Hasher) {
        for op in [self.start, self.stop] {
            match op {
                Some(i) => {
                    hasher.update(&i.to_le_bytes());
                    hasher.update(&[0]);
                }
                None => {
                    hasher.update(&0_i64.to_le_bytes());
                    hasher.update(&[1]);
                }
            }
        }
    }

    fn is_identity(self, l: usize) -> bool {
        self.start_u(l) == 0 && self.stop_u(l) == l
    }
}

impl<'source> FromPyObject<'source> for Slice {
    fn extract(slice_in: &'source PyAny) -> PyResult<Self> {
        let py_slice: &PySlice = slice_in.extract()?;

        // could also use never type if that was supported : /
        let step: Option<isize> = py_slice.getattr("step").unwrap().extract()?;
        if step != None {
            return Err(PyErr::new::<exceptions::PyValueError, _>(
                "step must be None!",
            ));
        }

        Ok(Slice {
            start: py_slice.getattr("start").unwrap().extract()?,
            stop: py_slice.getattr("stop").unwrap().extract()?,
        })
    }
}

impl IntoPy<PyObject> for Slice {
    fn into_py(self, py: Python<'_>) -> PyObject {
        unsafe {
            // we use unsafe + ffi because pyo3 slice doesn't support None
            let ptr = ffi::PySlice_New(
                self.start.into_py(py).as_ptr(),
                self.stop.into_py(py).as_ptr(),
                None::<i64>.into_py(py).as_ptr(),
            );
            let slice: &PySlice = py.from_owned_ptr(ptr);
            slice.into()
        }
    }
}

#[derive(PartialEq, Eq, Hash, Clone, Debug, Copy)]
pub struct USlice {
    pub start: usize,
    pub stop: usize,
}
impl USlice {
    pub fn intersection(&self, other: &USlice) -> USlice {
        let start = max(self.start, other.start);
        USlice {
            start,
            stop: max(min(self.stop, other.stop), start),
        }
    }
    pub fn union(&self, other: &USlice) -> USlice {
        USlice {
            start: min(self.start, other.start),
            stop: max(self.stop, other.stop),
        }
    }

    pub fn shrink_base(&self, new_base: &USlice) -> USlice {
        assert!(new_base.stop >= self.stop);
        assert!(self.start >= new_base.start);
        USlice {
            start: self.start - new_base.start,
            stop: self.stop - new_base.start,
        }
    }

    pub fn containing_uslice(x: &TensorAxisIndex) -> Option<USlice> {
        match x {
            TensorAxisIndex::Single(single) => Some(USlice {
                start: *single as usize,
                stop: (*single + 1) as usize,
            }),
            TensorAxisIndex::Slice(slice) => (*slice).into(),
            TensorAxisIndex::Tensor(_) => None,
        }
    }
    pub fn length(&self) -> usize {
        self.stop - self.start
    }
}

pub fn uslices_shrink_base(x: &Vec<USlice>, new_base: &Vec<USlice>) -> Vec<USlice> {
    zip(x, new_base).map(|(x, b)| x.shrink_base(b)).collect()
}

pub fn uslices_to_index(x: &Vec<USlice>) -> TensorIndex {
    TensorIndex(
        x.iter()
            .map(|x| TensorAxisIndex::Slice((*x).into()))
            .collect(),
    )
}

impl From<USlice> for Slice {
    fn from(x: USlice) -> Self {
        Slice {
            start: Some(x.start as i64),
            stop: Some(x.stop as i64),
        }
    }
}

impl From<Slice> for Option<USlice> {
    fn from(slice: Slice) -> Self {
        if let Slice {
            start: Some(start),
            stop: Some(stop),
        } = slice
        {
            if start < 0 || stop < 0 {
                return None;
            }
            Some(USlice {
                start: start as usize,
                stop: stop as usize,
            })
        } else {
            None
        }
    }
}

impl From<USlice> for TensorAxisIndex {
    fn from(x: USlice) -> Self {
        TensorAxisIndex::Slice(Slice {
            start: Some(x.start as i64),
            stop: Some(x.stop as i64),
        })
    }
}

/// for now, doesn't support tensors with negatives
#[derive(Debug, Clone, FromPyObject)]
pub enum TensorAxisIndex {
    Tensor(Tensor), // tensor needs to come first so len 1 tensors go to tensor not single
    Single(i64),
    Slice(Slice),
}

impl TensorAxisIndex {
    pub const IDENT: TensorAxisIndex = TensorAxisIndex::Slice(Slice {
        start: None,
        stop: None,
    });
    /// untested
    pub fn shrink_base_uslice(&self, uslice: &USlice) -> Self {
        match self {
            TensorAxisIndex::Single(single) => {
                assert!(*single >= 0);
                assert!((single + uslice.start as i64) < uslice.stop as i64);
                TensorAxisIndex::Single(single - uslice.start as i64)
            }
            TensorAxisIndex::Slice(slice) => {
                assert!(
                    slice.stop.is_some()
                        && slice.stop.unwrap() >= 0
                        && slice.start.unwrap_or(0) >= 0
                );
                let start = Some(slice.start.unwrap_or(0) - uslice.start as i64);
                let stop = Some(slice.stop.unwrap() - uslice.start as i64);
                TensorAxisIndex::Slice(Slice { start, stop })
            }
            TensorAxisIndex::Tensor(_tensor) => {
                unimplemented!();
            }
        }
    }
    pub fn new_plain_slice(start: usize, stop: usize) -> Self {
        TensorAxisIndex::Slice(Slice {
            start: Some(start as i64),
            stop: Some(stop as i64),
        })
    }

    pub fn is_identity(&self, l: usize) -> bool {
        if let TensorAxisIndex::Slice(slice) = self {
            return slice.size(l) == l;
        }
        false
    }

    pub fn new_tensor_randint_seeded(
        length: usize,
        base_length: usize,
        device_dtype: TorchDeviceDtypeOp,
        seed: usize,
    ) -> Self {
        TensorAxisIndex::Tensor(pyo3::Python::with_gil(|py| {
            PY_UTILS
                .torch
                .getattr(py, "manual_seed")
                .unwrap()
                .call(py, (seed,), None)
                .unwrap();
            let mut kwargs = HashMap::new();
            if let Some(dtype) = device_dtype.dtype {
                kwargs.insert("dtype", PY_UTILS.torch.getattr(py, dtype).unwrap());
            }
            if let Some(device) = device_dtype.device {
                kwargs.insert("device", device.into_py(py));
            }
            PY_UTILS
                .torch
                .getattr(py, "randint")
                .unwrap()
                .call(
                    py,
                    (0, base_length, pyo3::types::PyTuple::new(py, vec![length])),
                    Some(kwargs.into_py_dict(py)),
                )
                .unwrap()
                .extract(py)
                .unwrap()
        }))
    }
}

impl IntoPy<PyObject> for TensorAxisIndex {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            Self::Single(x) => x.into_py(py),
            Self::Tensor(x) => x.into_py(py),
            Self::Slice(x) => x.into_py(py),
        }
    }
}

// https://github.com/PyO3/pyo3/issues/1595 for why needed
impl ToPyObject for TensorAxisIndex {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

#[derive(Debug, Clone, FromPyObject)]
pub struct TensorIndex(pub Vec<TensorAxisIndex>);

impl Display for TensorIndex {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut result = "(".to_owned();
        for (i, idx) in self.0.iter().enumerate() {
            result.push_str(&match idx {
                TensorAxisIndex::Single(i) => i.to_string(),
                TensorAxisIndex::Slice(slice) => {
                    slice.start.map(|i| i.to_string()).unwrap_or("".to_owned())
                        + ":"
                        + &slice.stop.map(|i| i.to_string()).unwrap_or("".to_owned())
                }
                TensorAxisIndex::Tensor(tensor) => {
                    "[".to_owned() + &tensor.shape()[0].to_string() + "]"
                }
            });
            if i != self.0.len() - 1 {
                result.push(',');
            }
        }
        result.push(')');
        write!(f, "{}", result)
    }
}

#[test]
fn sat_as_expected() {
    assert_eq!(1, 4usize.saturating_sub((-(-3isize)) as usize));
    assert_eq!(0, 4usize.saturating_sub((-(-5isize)) as usize));
}

impl TensorIndex {
    pub fn apply_to_shape(&self, shape: &Shape) -> Shape {
        zip(&self.0, shape)
            .filter_map(|(idx, &l)| match idx {
                TensorAxisIndex::Single(_i) => None,
                TensorAxisIndex::Tensor(t) => {
                    if t.shape().is_empty() {
                        None
                    } else {
                        Some(t.shape()[0])
                    }
                }
                TensorAxisIndex::Slice(sl) => Some(sl.size(l)),
            })
            .collect()
    }
    pub fn is_identity(&self, shape: &Shape) -> bool {
        zip(&self.0, shape).all(|(idx, &l)| match idx {
            TensorAxisIndex::Single(_i) => false,
            TensorAxisIndex::Tensor(_t) => false, // dont bother to check tensor, if you want that canon first
            TensorAxisIndex::Slice(sl) => sl.is_identity(l),
        })
    }

    pub fn validate(&self, shape: &Shape) -> Result<(), CircuitConstructionError> {
        let get_err = |at| {
            Err(CircuitConstructionError::IndexOutOfBounds {
                index: self.clone(),
                shape: shape.clone(),
                at,
                axis: self.0[at].clone(),
                l: shape[at],
            })
        };

        let check = |at: usize, i: Option<i64>, l: usize, is_slice: bool| {
            if let Some(i) = i {
                let end_b = if is_slice { l + 1 } else { l };
                if i >= end_b as i64 || i < -(l as i64) {
                    return get_err(at);
                }
            }
            Ok(())
        };

        for (at, (idx, &l)) in zip(&self.0, shape).enumerate() {
            match idx {
                &TensorAxisIndex::Single(i) => check(at, Some(i), l, false)?,
                &TensorAxisIndex::Slice(Slice { start, stop }) => {
                    check(at, start, l, true)?;
                    check(at, stop, l, true)?;

                    let mod_l_idx = |x| if x < 0 { l as i64 + x } else { x };
                    let start_u: i64 = start.map_or(0, mod_l_idx);
                    let stop_u: i64 = stop.map_or(l as i64, mod_l_idx);
                    if start_u > stop_u {
                        get_err(at)?;
                    }
                }
                _ => (),
            }
        }

        Ok(())
    }

    pub fn canonicalize(&self, shape: &Shape) -> TensorIndex {
        self.validate(shape).expect("invalid tensor index");
        TensorIndex(
            zip(&self.0, shape)
                .map(|(idx, &l)| match idx {
                    TensorAxisIndex::Single(i) => TensorAxisIndex::Single((*i + l as i64) % l as i64),
                    TensorAxisIndex::Tensor(t) => TensorAxisIndex::Tensor(t.clone()), // not bothering to canon tensor for now
                    TensorAxisIndex::Slice(sl) => TensorAxisIndex::Slice(sl.canonicalize(l)),
                })
                .collect(),
        )
    }

    pub fn all_slices(&self) -> Option<Vec<Slice>> {
        let filtered = filter_by_variant!(&self.0, TensorAxisIndex, Slice, Slice).0;
        if filtered.len() == self.0.len() {
            Some(filtered)
        } else {
            None
        }
    }

    pub fn all_uslices(&self) -> Option<Vec<USlice>> {
        self.all_slices().and_then(|x| {
            let result: Vec<USlice> = x.iter().filter_map(|x| (*x).into()).collect();
            if result.len() == x.len() {
                Some(result)
            } else {
                None
            }
        })
    }

    pub fn new_single(idx: TensorAxisIndex, pos: usize, rank: usize) -> Self {
        TensorIndex(
            (0..rank)
                .map(|i| {
                    if i == pos {
                        idx.clone()
                    } else {
                        TensorAxisIndex::IDENT
                    }
                })
                .collect(),
        )
    }

    pub fn ident(rank: usize) -> Self {
        Self(vec![TensorAxisIndex::IDENT; rank])
    }

    pub fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        for axis in self.0.iter() {
            hasher.update(&uuid!("3d14636b-a1ed-4235-91cd-5fc9e818c93d").into_bytes()); // delimit with uuid
            match axis {
                TensorAxisIndex::Single(i) => {
                    hasher.update(&i.to_le_bytes());
                }
                TensorAxisIndex::Tensor(t) => {
                    hasher.update(t.hashed().hash().unwrap());
                } // dont bother to check tensor, if you want that canon first
                TensorAxisIndex::Slice(sl) => sl.update_hash(&mut hasher),
            }
        }
        hasher.finalize().into()
    }
}

impl IntoPy<PyObject> for TensorIndex {
    fn into_py(self, py: Python<'_>) -> PyObject {
        PyTuple::new(py, self.0).into_py(py)
    }
}

pub fn compose(top: &TensorIndex, bottom: &TensorIndex) -> TensorIndex {
    let mut result: Vec<TensorAxisIndex> = vec![];
    let mut top_idx: usize = 0;
    for bottom_idx in bottom.0.iter() {
        match bottom_idx {
            TensorAxisIndex::Single(_i) => result.push(bottom_idx.clone()),
            TensorAxisIndex::Tensor(t) => {
                let top_here = top.0[top_idx].clone();
                top_idx += 1;
                Python::with_gil(|py| {
                    let indexed_tensor = t.clone().py_getitem(py, top_here).unwrap();
                    if indexed_tensor.shape().is_empty() {
                        result.push(TensorAxisIndex::Single(pycall!(
                            PY_UTILS.cast_int,
                            (indexed_tensor,)
                        )));
                    } else {
                        result.push(TensorAxisIndex::Tensor(indexed_tensor));
                    }
                })
            }
            TensorAxisIndex::Slice(slice) => {
                let start = slice.start.unwrap_or(0);
                let stop = slice.stop;
                let top_here = top.0[top_idx].clone();
                match top_here {
                    TensorAxisIndex::Single(i) => result.push(TensorAxisIndex::Single(start + i)),
                    TensorAxisIndex::Tensor(t) => Python::with_gil(|py| {
                        result.push(TensorAxisIndex::Tensor(t.py_add(py, start).unwrap()))
                    }),
                    TensorAxisIndex::Slice(top_slice) => {
                        let top_start = top_slice.start.unwrap_or(0);
                        let top_stop = top_slice.stop;
                        let (mut new_start, mut new_stop) =
                            (Some(start + top_start), Some(start + top_stop.unwrap_or(0)));
                        if top_start < 0 {
                            new_start = Some(stop.unwrap_or(0) + top_start);
                        }
                        if top_stop.unwrap_or(-1) < 0 {
                            if top_stop.is_none() && stop.is_none() {
                                new_stop = None;
                            } else {
                                new_stop = Some(stop.unwrap_or(0) + top_stop.unwrap_or(0));
                            }
                        }
                        result.push(TensorAxisIndex::Slice(Slice {
                            start: new_start,
                            stop: new_stop,
                        }))
                    }
                }
                top_idx += 1;
            }
        }
    }
    TensorIndex(result)
}

pub fn cuda_to_first_cuda(string: &str) -> String {
    if string == "cuda" {
        let number = match std::env::var("CUDA_VISIBLE_DEVICES") {
            Err(_e) => 0,
            Ok(s) => s
                .split(",")
                .map(|s| s.parse::<usize>())
                .nth(0)
                .unwrap_or(Ok(0))
                .unwrap_or(0),
        };
        format!("cuda:{}", number)
    } else {
        string.to_owned()
    }
}

#[test]
fn test_cvd() {
    dbg!(cuda_to_first_cuda("cuda"));
}

/// use string so you can compare fast when constructing and have full range (weird types like uint or bfloat16)
/// as opposed to PyObject torch.dtype or enum (could switch to enum)
#[pyclass]
#[derive(Debug, Clone, PartialEq, Eq, Default, PyClassDeriv)]
pub struct TorchDeviceDtypeOp {
    #[pyo3(get)]
    pub device: Option<String>,
    #[pyo3(get)]
    pub dtype: Option<String>,
}

#[pymethods]
impl TorchDeviceDtypeOp {
    #[staticmethod]
    #[pyo3(name = "default")]
    fn default_py() -> Self {
        Self::default()
    }

    #[new]
    #[args(device = "None", dtype = "None")]
    fn new(device: Option<String>, dtype: Option<String>) -> Self {
        Self {
            device: device.map(|x| cuda_to_first_cuda(&x)),
            dtype,
        }
    }
}

#[pyclass]
#[derive(Debug, Clone, PartialEq, Eq, PyClassDeriv)]
pub struct TorchDeviceDtype {
    #[pyo3(get)]
    pub device: String,
    #[pyo3(get)]
    pub dtype: String,
}

#[pymethods]
impl TorchDeviceDtype {
    #[new]
    fn new(device: String, dtype: String) -> Self {
        Self {
            device: cuda_to_first_cuda(&device),
            dtype,
        }
    }
    #[staticmethod]
    #[pyo3(name = "from_tensor")]
    pub fn from_tensor_py(tensor: Tensor) -> Self {
        Self::from_tensor(&tensor)
    }

    pub fn cast_tensor(&self, tensor: Tensor) -> Tensor {
        Python::with_gil(|py| {
            PY_UTILS
                .cast_tensor
                .call(py, (tensor, self.clone()), None)
                .unwrap()
                .extract(py)
                .unwrap()
        })
    }
}

impl TorchDeviceDtype {
    pub fn from_tensor(tensor: &Tensor) -> Self {
        Python::with_gil(|py| Self {
            device: tensor
                .tensor()
                .getattr(py, "device")
                .unwrap()
                .getattr(py, "__str__")
                .unwrap()
                .call0(py)
                .unwrap()
                .extract(py)
                .unwrap(),
            dtype: tensor
                .tensor()
                .getattr(py, "dtype")
                .unwrap()
                .getattr(py, "__str__")
                .unwrap()
                .call0(py)
                .unwrap()
                .extract::<String>(py)
                .unwrap()[6..]
                .to_owned(),
        })
    }
    pub fn size(&self) -> usize {
        let map = HashMap::from([
            ("float32".to_owned(), 4),
            ("float64".to_owned(), 8),
            ("float16".to_owned(), 2),
            ("int64".to_owned(), 8),
            ("int32".to_owned(), 4),
            ("int16".to_owned(), 2),
            ("int8".to_owned(), 1),
        ]);
        map[&self.dtype]
    }
}

impl From<TorchDeviceDtype> for TorchDeviceDtypeOp {
    fn from(x: TorchDeviceDtype) -> Self {
        Self {
            device: Some(x.device),
            dtype: Some(x.dtype),
        }
    }
}

impl TorchDeviceDtypeOp {
    pub const NONE: Self = TorchDeviceDtypeOp {
        device: None,
        dtype: None,
    };

    pub fn combine(self, other: Self) -> Result<Self, CircuitConstructionError> {
        let out = Self {
            device: match (&self.device, &other.device) {
                (Some(l), Some(r)) if l != r => {
                    return Err(CircuitConstructionError::ChildrenMultipleDevices {
                        a: self.device.clone(),
                        b: other.device.clone(),
                    });
                }
                (l, r) => l.as_ref().or(r.as_ref()).cloned(),
            },
            dtype: match (&self.dtype, &other.dtype) {
                (Some(l), Some(r)) if l != r => {
                    return Err(CircuitConstructionError::ChildrenMultipleDtypes {
                        a: self.dtype.clone(),
                        b: other.dtype.clone(),
                    });
                }
                (l, r) => l.as_ref().or(r.as_ref()).cloned(),
            },
        };
        Ok(out)
    }

    pub fn unwrap_or_defaults(self) -> TorchDeviceDtype {
        TorchDeviceDtype {
            dtype: self.dtype.unwrap_or_else(|| "float32".to_owned()),
            device: self.device.unwrap_or_else(|| "cpu".to_owned()),
        }
    }

    pub fn size(&self) -> usize {
        self.clone().unwrap_or_defaults().size()
    }
}
