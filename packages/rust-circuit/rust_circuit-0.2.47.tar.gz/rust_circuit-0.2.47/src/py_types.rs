use crate::pyo3_prelude::*;
use lazy_static::lazy_static;
use pyo3::{
    exceptions,
    types::{PyBytes, PyTuple},
};
use uuid::Uuid;

use crate::{
    circuit::{EinsumAxes, HashBytes},
    tensor_util::Shape,
};

lazy_static! {
    static ref PYTHON_UTILS: Py<PyModule> = Python::with_gil(|py| {
        PyModule::from_code(
            py,
            include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/rust_circuit_type_utils.py")),
            "rust_circuit_type_utils.py",
            "rust_circuit_type_utils",
        )
        .unwrap() // TODO: fail more gracefully?
        .into()
    });

    pub static ref PY_TORCH: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "torch").unwrap());
    static ref GET_TENSOR_SHAPE: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "get_tensor_shape").unwrap());
    static ref GET_UUID_BYTES: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "get_uuid_bytes").unwrap());
    static ref CONSTRUCT_UUID_BYTES: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "construct_uuid_bytes").unwrap());
    static ref PY_OPERATOR: Py<PyModule> =
        Python::with_gil(|py| PyModule::import(py, "operator").unwrap().into());
    pub static ref PY_ID: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "get_id").unwrap());
    pub static ref PY_CAST_INT: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "cast_int").unwrap());
    pub static ref PY_SCALAR_TO_TENSOR: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "scalar_to_tensor").unwrap());
    pub static ref CAST_TENSOR: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "cast_tensor").unwrap());
    pub static ref UN_FLAT_CONCAT: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "un_flat_concat").unwrap());
    pub static ref TENSOR_SCALE: PyObject =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "tensor_scale").unwrap());
    pub static ref GENERALFUNCTIONS: std::collections::HashMap<String,PyObject> =
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "generalfunctions").unwrap().extract(py).unwrap());
    pub static ref PY_NONE: PyObject=
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "none").unwrap().extract(py).unwrap());
    pub static ref PY_EINSUM: PyObject=
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "einsum").unwrap().extract(py).unwrap());
    pub static ref PY_MAKE_DIAGONAL: PyObject=
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "make_diagonal").unwrap().extract(py).unwrap());
    pub static ref PY_MAKE_BYTES: PyObject=
        Python::with_gil(|py| PYTHON_UTILS.getattr(py, "construct_bytes").unwrap().extract(py).unwrap());
}

lazy_static! {
    static ref PYCIRCUIT_MODULE: Py<PyModule> = Python::with_gil(|py| {
        PyModule::from_code(
            py,
            "from interp.circuit import computational_node, constant; import interp.circuit.interop_rust.interop_rust as interop; import einops; import interp.circuit.circuit_compiler.util as circ_compiler_util",
            "py_circuit_interop.py",
            "py_circuit_interop",
        )
        .unwrap() // TODO: fail more gracefully?
        .into()
    });

    pub static ref PY_COMPUTATIONAL_NODE: PyObject =
        Python::with_gil(|py| PYCIRCUIT_MODULE.getattr(py, "computational_node").unwrap());
    pub static ref PY_CONSTANT: PyObject =
        Python::with_gil(|py| PYCIRCUIT_MODULE.getattr(py, "constant").unwrap());
    pub static ref PY_CIRCUIT_INTEROP: PyObject =
        Python::with_gil(|py| PYCIRCUIT_MODULE.getattr(py, "interop").unwrap());
    pub static ref CIRCUIT_RUST_TO_PY: PyObject =
        Python::with_gil(|py| PY_CIRCUIT_INTEROP.getattr(py, "rust_to_py").unwrap());
    pub static ref PY_EINOPS: PyObject =
        Python::with_gil(|py| PYCIRCUIT_MODULE.getattr(py, "einops").unwrap());
    pub static ref PY_EINOPS_REPEAT: PyObject =
        Python::with_gil(|py| PY_EINOPS.getattr(py, "repeat").unwrap());
    pub static ref PY_CIRC_COMPILER_UTIL: PyObject =
        Python::with_gil(|py| PYCIRCUIT_MODULE.getattr(py, "circ_compiler_util").unwrap());

    static ref PY_TENSOR_HASH_MODULE: Py<PyModule> = Python::with_gil(|py| {
        PyModule::from_code(
            py,
            include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/tensor_hash.py")),
            "tensor_hash.py",
            "tensor_hash",
        )
        .unwrap() // TODO: fail more gracefully?
        .into()
    });


    pub static ref HASH_TENSOR: PyObject =
        Python::with_gil(|py| PY_TENSOR_HASH_MODULE.getattr(py, "hash_tensor").unwrap());
}

#[macro_export]
macro_rules! pycall {
    ($f:ident,$args:expr) => {
        Python::with_gil(|py| $f.call(py, $args, None).unwrap().extract(py).unwrap())
    };
    ($f:ident,$args:expr,$err_type:ty) => {
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
            lazy_static! {
                $(
                    static ref [<PY_ $op:upper>]: PyObject =
                        Python::with_gil(|py| PY_OPERATOR.getattr(py, stringify!($op)).unwrap());
                )*
            }

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
                        [<PY_ $op:upper>].call1(py, (self, x))?.extract(py)
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
            Python::with_gil(|py| GET_UUID_BYTES.call1(py, (uuid_obj,))?.extract(py))?;

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
        CONSTRUCT_UUID_BYTES
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
        let shape = Python::with_gil(|py| GET_TENSOR_SHAPE.call1(py, (tensor,))?.extract(py))?;

        Ok(Self {
            tensor: tensor.into(),
            shape,
            hash: None,
        })
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

pub fn py_address(x: &PyObject) -> usize {
    Python::with_gil(|py| PY_ID.call(py, (x,), None).unwrap().extract(py).unwrap())
}
