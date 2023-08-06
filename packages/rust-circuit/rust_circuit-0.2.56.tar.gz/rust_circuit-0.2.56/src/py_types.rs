use crate::{all_imports::TorchDeviceDtype, pyo3_prelude::*};
use macro_rules_attribute::apply;
use pyo3::types::IntoPyDict;
use pyo3::{
    exceptions,
    types::{PyBytes, PyTuple},
};
use uuid::Uuid;

use crate::{
    circuit::{EinsumAxes, HashBytes},
    lazy::GILLazyPy,
    tensor_util::Shape,
};

pub struct PyUtils {
    pub torch: PyObject,
    get_tensor_shape: PyObject,
    get_uuid_bytes: PyObject,
    construct_uuid_bytes: PyObject,
    id: PyObject,
    pub cast_int: PyObject,
    scalar_to_tensor: PyObject,
    pub cast_tensor: PyObject,
    un_flat_concat: PyObject,
    tensor_scale: PyObject,
    pub generalfunctions: std::collections::HashMap<String, PyObject>,
    pub none: PyObject,
    einsum: PyObject,
    make_diagonal: PyObject,
    make_bytes: PyObject,
}

/// misc python utilities
pub static PY_UTILS: GILLazyPy<PyUtils> = GILLazyPy::new_py(|py| {
    let utils = PyModule::from_code(
        py,
        include_str!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/rust_circuit_type_utils.py"
        )),
        concat!(env!("CARGO_MANIFEST_DIR"), "/rust_circuit_type_utils.py"),
        "rust_circuit_type_utils",
    )
    .unwrap();

    let get = |s: &str| utils.getattr(s).unwrap().into();

    PyUtils {
        torch: get("torch"),
        get_tensor_shape: get("get_tensor_shape"),
        get_uuid_bytes: get("get_uuid_bytes"),
        construct_uuid_bytes: get("construct_uuid_bytes"),
        id: get("get_id"),
        cast_int: get("cast_int"),
        scalar_to_tensor: get("scalar_to_tensor"),
        cast_tensor: get("cast_tensor"),
        un_flat_concat: get("un_flat_concat"),
        tensor_scale: get("tensor_scale"),
        generalfunctions: utils
            .getattr("generalfunctions")
            .unwrap()
            .extract()
            .unwrap(),
        none: get("none"),
        einsum: get("einsum"),
        make_diagonal: get("make_diagonal"),
        make_bytes: get("make_bytes"),
    }
});

pub fn py_address(x: &PyObject) -> usize {
    Python::with_gil(|py| {
        PY_UTILS
            .id
            .call(py, (x,), None)
            .unwrap()
            .extract(py)
            .unwrap()
    })
}

#[macro_export]
macro_rules! make_py_func {
    {
        #[py_ident($py:ident)]
        $( #[$m:meta] )*
        $vi:vis fn $name:ident($($arg_name:ident : $arg_ty:ty),* $(,)?) -> $ret_ty:ty
        { $($tt:tt)* }
    } => {
        paste::paste!{
            $(#[$m])*
            $vi fn [<$name _py>]<'py>($py : Python<'py>, $($arg_name : $arg_ty,)*) -> $ret_ty {
                $($tt)*
            }
            $(#[$m])* // TODO: maybe shouldn't apply to both??
            $vi fn $name($($arg_name : $arg_ty,)*) -> $ret_ty {
                Python::with_gil(|py| [<$name _py>](py, $($arg_name,)*))
            }
        }

    };
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn scalar_to_tensor(v: f64, shape: Shape, device_dtype: TorchDeviceDtype) -> PyResult<Tensor> {
    PY_UTILS
        .scalar_to_tensor
        .call(py, (v, shape, device_dtype), None)?
        .extract::<Tensor>(py)
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn einsum(items: Vec<(Tensor, EinsumAxes)>, out_axes: EinsumAxes) -> PyResult<Tensor> {
    PY_UTILS
        .einsum
        .call(py, (items, out_axes), None)?
        .extract(py)
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn make_diagonal(
    non_diag: &Tensor,
    out_axes_deduped: EinsumAxes,
    out_axes: EinsumAxes,
) -> PyResult<Tensor> {
    PY_UTILS
        .make_diagonal
        .call(py, (non_diag, out_axes_deduped, out_axes), None)?
        .extract(py)
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn einops_repeat(
    tensor: &Tensor,
    op: String,
    sizes: impl IntoIterator<Item = (String, u64)>,
) -> PyResult<Tensor> {
    PY_EINOPS
        .repeat
        .call(py, (tensor, op), Some(sizes.into_py_dict(py)))?
        .extract(py)
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn make_bytes(bytes: &[u8]) -> PyResult<PyObject> {
    PY_UTILS.make_bytes.call(py, (bytes,), None)
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn un_flat_concat(tensor: &Tensor, split_shapes: Vec<Shape>) -> PyResult<Vec<Tensor>> {
    PY_UTILS
        .un_flat_concat
        .call(py, (tensor, split_shapes), None)?
        .extract(py)
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn tensor_scale(tensor: &Tensor) -> PyResult<f64> {
    PY_UTILS.tensor_scale.call(py, (tensor,), None)?.extract(py)
}

pub struct PyEinops {
    pub einops: Py<PyModule>,
    pub repeat: PyObject,
}

pub static PY_EINOPS: GILLazyPy<PyEinops> = GILLazyPy::new_py(|py| {
    let einops = PyModule::import(py, "einops").unwrap();
    let get = |s: &str| einops.getattr(s).unwrap().into();

    PyEinops {
        einops: einops.into(),
        repeat: get("repeat"),
    }
});

pub static HASH_TENSOR: GILLazyPy<PyObject> = GILLazyPy::new_py(|py| {
    let module = PyModule::from_code(
        py,
        include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/tensor_hash.py")),
        concat!(env!("CARGO_MANIFEST_DIR"), "/tensor_hash.py"),
        "tensor_hash",
    )
    .unwrap();
    module.getattr("hash_tensor").unwrap().into()
});

#[macro_export]
macro_rules! pycall {
    ($f:expr,$args:expr) => {
        Python::with_gil(|py| $f.call(py, $args, None).unwrap().extract(py).unwrap())
    };
    ($f:expr,$args:expr,$err_type:ty) => {
        Python::with_gil(|py| {
            $f.call(py, $args, None)
                .map_err(|z| <$err_type>::from(z))?
                .extract(py)
                .map_err(|z| <$err_type>::from(z))
        })
    };
}

macro_rules! generate_extra_py_ops {
    [$($op:ident),*] => {
        paste::paste! {
            struct PyOperators {
                $($op: PyObject,)*
            }

            static PY_OPERATORS: GILLazyPy<PyOperators> = GILLazyPy::new_py(|py| {
                let operator = PyModule::import(py, "operator").unwrap();

                PyOperators {
                    $( $op : operator.getattr(stringify!($op)).unwrap().into(),)*
                }
            });


            /// Trait for python operator methods when they return the same type.
            /// Used for tensors.
            ///
            /// Not useful when an operator returns a different type: this will
            /// always raise an error (e.g. dict).
            ///
            /// # Example
            ///
            /// ```
            /// # use pyo3::prelude::*;
            /// # use rust_circuit::py_types::ExtraPySelfOps;
            ///
            /// #[derive(Clone, Debug, FromPyObject)]
            /// struct WrapInt(i64);
            ///
            /// impl IntoPy<PyObject> for WrapInt {
            ///     fn into_py(self, py: Python<'_>) -> PyObject {
            ///         self.0.into_py(py)
            ///     }
            /// }
            ///
            /// impl ExtraPySelfOps for WrapInt {}
            ///
            /// pyo3::prepare_freethreaded_python();
            ///
            /// assert_eq!(
            ///     Python::with_gil(|py| WrapInt(8).py_add(py, 7)).unwrap().0,
            ///     7 + 8
            /// );
            /// assert_eq!(
            ///     Python::with_gil(|py| WrapInt(2).py_mul(py, 3)).unwrap().0,
            ///     2 * 3
            /// );
            /// ```
            pub trait ExtraPySelfOps
            where
                Self: IntoPy<PyObject>,
                for<'a> Self: FromPyObject<'a>,
            {
                $(
                    fn [<py_ $op>]<'a>(self, py: Python<'a>, x: impl IntoPy<PyObject>) -> PyResult<Self> {
                        PY_OPERATORS.$op.call1(py, (self, x))?.extract(py)
                    }

                    // not sure if this method should exist
                    fn [<py_ $op _acquire>]<'a>(self, x: impl IntoPy<PyObject>) -> PyResult<Self> {
                        Python::with_gil(|py| self.[<py_ $op>](py, x))
                    }
                )*
            }
        }
    }
}

// add more as needed
generate_extra_py_ops!(add, getitem, mul);

pub struct PyUuid(pub Uuid);

impl<'source> FromPyObject<'source> for PyUuid {
    fn extract(uuid_obj: &'source PyAny) -> PyResult<Self> {
        let uuid_bytes: Vec<u8> =
            Python::with_gil(|py| PY_UTILS.get_uuid_bytes.call1(py, (uuid_obj,))?.extract(py))?;

        let num_bytes = uuid_bytes.len();
        let bytes_arr: [u8; 16] = uuid_bytes.try_into().map_err(|_| {
            PyErr::new::<exceptions::PyTypeError, _>(format!(
                "expected 16 bytes for uuid, found {}",
                num_bytes
            ))
        })?;

        Ok(PyUuid(Uuid::from_bytes(bytes_arr)))
    }
}

impl IntoPy<PyObject> for PyUuid {
    fn into_py(self, py: Python<'_>) -> PyObject {
        PY_UTILS
            .construct_uuid_bytes
            .call1(py, (PyBytes::new(py, &self.0.into_bytes()),))
            .unwrap()
    }
}

#[derive(Debug, Clone)]
pub struct Tensor {
    tensor: PyObject,
    shape: Shape, /* cache shape so doesn't have to be recomputed on reconstruct etc (not uber efficient I think) */
    hash: Option<HashBytes>,
}

impl<'source> FromPyObject<'source> for Tensor {
    fn extract(tensor: &'source PyAny) -> PyResult<Self> {
        let shape =
            Python::with_gil(|py| PY_UTILS.get_tensor_shape.call1(py, (tensor,))?.extract(py))?;

        Ok(Self {
            tensor: tensor.into(),
            shape,
            hash: None,
        })
    }
}

impl IntoPy<PyObject> for &Tensor {
    fn into_py(self, _py: Python<'_>) -> PyObject {
        self.tensor.clone()
    }
}
impl IntoPy<PyObject> for Tensor {
    fn into_py(self, _py: Python<'_>) -> PyObject {
        self.tensor
    }
}

impl ExtraPySelfOps for Tensor {}

impl Tensor {
    pub fn tensor(&self) -> &PyObject {
        &self.tensor
    }

    pub fn shape(&self) -> &Shape {
        &self.shape
    }

    pub fn hash(&self) -> Option<&HashBytes> {
        self.hash.as_ref()
    }

    pub fn hash_usize(&self) -> Option<usize> {
        self.hash.as_ref().map(|x| {
            let mut hash_prefix: [u8; 8] = Default::default();
            hash_prefix.copy_from_slice(&x[..8]);
            usize::from_le_bytes(hash_prefix)
        })
    }

    pub fn hashed(&self) -> Tensor {
        if self.hash.is_some() {
            self.clone()
        } else {
            Self {
                tensor: self.tensor.clone(),
                shape: self.shape.clone(),
                hash: Python::with_gil(|py| {
                    HASH_TENSOR
                        .call(py, (self.tensor.clone(),), None)
                        .unwrap()
                        .extract(py)
                        .unwrap()
                }),
            }
        }
    }
}

#[derive(FromPyObject)]
pub struct PyShape(pub Shape);

impl IntoPy<PyObject> for PyShape {
    fn into_py(self, py: Python<'_>) -> PyObject {
        PyTuple::new(py, self.0).into_py(py)
    }
}

#[derive(FromPyObject)]
pub struct PyEinsumAxes(pub EinsumAxes);

impl IntoPy<PyObject> for PyEinsumAxes {
    fn into_py(self, py: Python<'_>) -> PyObject {
        PyTuple::new(py, self.0).into_py(py)
    }
}
