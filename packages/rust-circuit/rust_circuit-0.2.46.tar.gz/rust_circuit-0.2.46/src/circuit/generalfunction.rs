use crate::hashmaps::FxHashMap as HashMap;
use crate::pyo3_prelude::*;
use std::iter::zip;

use super::{prelude::*, CachedCircuitInfo, HashBytes};
use crate::py_types::{GENERALFUNCTIONS, PY_NONE};
use crate::{
    circuit::PyCircuitBase,
    circuit_node_auto_impl, circuit_node_extra_impl, new_rc_unwrap,
    py_types::py_address,
    tensor_util::{Shape, TorchDeviceDtype},
};

use lazy_static::lazy_static;
use macro_rules_attribute::apply;
use pyo3::types::PyDict;
use pyo3::types::PyTuple;
use uuid::uuid;

#[pyo3::prelude::pyclass] // this needs to be sent to python all the time
pub struct PyGFSpecShapeGetter {
    pub num_non_batchable: usize,
}
#[pyo3::prelude::pymethods]
impl PyGFSpecShapeGetter {
    pub fn __call__(
        &mut self,
        _py: Python<'_>,
        args: &PyAny,
        _kwargs: Option<&PyDict>,
    ) -> Py<PyAny> {
        Python::with_gil(|py| {
            // println!("{}", args.getattr("__repr__").unwrap().call0().unwrap());
            let shapes: Vec<Vec<usize>> = args.extract().unwrap();
            if shapes.len() != 1 {
                return PY_NONE.clone();
            }
            if shapes[0].len() < self.num_non_batchable {
                return PY_NONE.clone();
            }
            return PyTuple::new(py, shapes[0].clone()).into();
        })
    }

    #[new]
    pub fn new(num_non_batchable: usize) -> Self {
        Self { num_non_batchable }
    }
}

macro_rules! gfspecs_wrap {
    ($py:expr,$name:literal,$non_batchable:literal) => {
        (
            $name.to_owned(),
            GeneralFunctionSpec {
                function: GENERALFUNCTIONS[$name].clone(),
                get_shape: PyGFSpecShapeGetter {
                    num_non_batchable: $non_batchable,
                }
                .into_py($py),
                get_jacobians: None,
                num_non_batchable_output_dims: $non_batchable,
                input_batchability: vec![true],
                name: $name.to_owned(),
                is_official: true,
            },
        )
    };
}

lazy_static! {
    static ref GENERAL_FUNCTIONS_SPECS: HashMap<String, GeneralFunctionSpec> =
        Python::with_gil(|py| {
            HashMap::from([
                gfspecs_wrap!(py, "sigmoid", 0),
                gfspecs_wrap!(py, "tanh", 0),
                gfspecs_wrap!(py, "rsqrt", 0),
                gfspecs_wrap!(py, "gelu", 0),
                gfspecs_wrap!(py, "relu", 0),
                gfspecs_wrap!(py, "reciprocal", 0),
                gfspecs_wrap!(py, "log_exp_p_1", 0),
                gfspecs_wrap!(py, "gaussian_pdf", 0),
                gfspecs_wrap!(py, "gaussian_cdf", 0),
                gfspecs_wrap!(py, "softmax", 1),
                gfspecs_wrap!(py, "log_softmax", 1),
                gfspecs_wrap!(py, "q_from_qr", 2),
            ])
        });
}
/// GeneralFunctionSpec contains all needed info about function, and is the same on all instances with the same function
/// how batchability works: input_batchability is a mask indicating which inputs support batching. if none do, there is no batching.
/// the number of non batchable dims in output, starting from end, is num_non_batchable_output_dims.
#[pyclass]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct GeneralFunctionSpec {
    #[pyo3(get)]
    pub function: PyObject, // python function ([torch.Tensor])->torch.Tensor
    #[pyo3(get)]
    pub get_shape: PyObject, // python function ([Shape])->Optional[Shape]
    #[pyo3(get)]
    pub get_jacobians: Option<PyObject>, /* python function (GeneralFunction)->List[Circuit], one circuit per input */
    #[pyo3(get)]
    pub num_non_batchable_output_dims: usize,
    #[pyo3(get)]
    pub input_batchability: Vec<bool>,
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub is_official: bool,
}

impl GeneralFunctionSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&py_address(&self.function).to_le_bytes());
        hasher.update(&py_address(&self.get_shape).to_le_bytes());
        hasher.update(
            &self
                .get_jacobians
                .as_ref()
                .map(|x| py_address(x).to_le_bytes())
                .unwrap_or([0; 8]),
        );
        hasher.update(&self.num_non_batchable_output_dims.to_le_bytes());
        hasher.update(
            &self
                .input_batchability
                .iter()
                .map(|x| if *x { 1 } else { 0 })
                .collect::<Vec<u8>>(),
        );
        hasher.update(&uuid!("b9075dd8-cfbe-4dae-a65b-691ec1b38bf6").into_bytes()); // delimit with uuid
        hasher.update(self.name.as_bytes());
        *hasher.finalize().as_bytes()
    }
}

#[pymethods]
impl GeneralFunctionSpec {
    #[new]
    fn new(
        function: PyObject,
        get_shape: PyObject,
        get_jacobians: Option<PyObject>,
        num_non_batchable_output_dims: usize,
        input_batchability: Vec<bool>,
        name: String,
    ) -> Self {
        Self {
            function,
            get_shape,
            get_jacobians,
            num_non_batchable_output_dims,
            input_batchability,
            name,
            is_official: false,
        }
    }
    pub fn is_batchable(&self) -> bool {
        self.input_batchability.iter().any(|x| *x)
    }
}

#[pyclass(unsendable, extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct GeneralFunction {
    #[pyo3(get)]
    pub nodes: Vec<CircuitRc>,
    #[pyo3(get)]
    pub spec: GeneralFunctionSpec,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl GeneralFunction {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        nodes: Vec<CircuitRc>,
        spec: GeneralFunctionSpec,
        name: Option<String>,
    ) -> (Result<Self, CircuitConstructionError>) {
        let mut out = Self {
            nodes,
            spec,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        if out.try_compute_shape().is_none() {
            return Err(CircuitConstructionError::GeneralFunctionWrongInputShape {
                gf_spec: out.spec,
                input_shapes: out.nodes.iter().map(|x| x.info().shape.clone()).collect(),
            });
        }
        // todo check not too many axes / oob
        out.init_info()
    }

    fn try_compute_shape(&self) -> Option<Shape> {
        Python::with_gil(|py| {
            self.spec
                .get_shape
                .call(
                    py,
                    (self
                        .nodes
                        .iter()
                        .map(|x| x.info().shape.clone())
                        .collect::<Vec<Shape>>(),),
                    None,
                )
                .unwrap()
                .extract(py)
                .unwrap()
        })
    }
}

circuit_node_extra_impl!(GeneralFunction);

impl CircuitNode for GeneralFunction {
    circuit_node_auto_impl!("3c655670-b352-4a5f-891c-0d7160609341");

    fn compute_shape(&self) -> Shape {
        self.try_compute_shape().unwrap()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        for node in &self.nodes {
            hasher.update(&node.info().hash);
        }
        if self.spec.is_official {
            hasher.update(uuid!("2b355376-2e18-479e-8a52-1903ba3fd145").as_bytes());
            hasher.update(self.spec.name.as_bytes());
        } else {
            hasher.update(uuid!("2f45e4d7-8019-43df-be98-23425312691b").as_bytes());
            hasher.update(&self.spec.compute_hash());
        }
        hasher
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<'a, F, E>(
        &'a self,
        mut f: F,
    ) -> Result<Self, CircuitConstructionError>
    where
        CircuitConstructionError: From<E>,
        F: FnMut(usize, &'a Circuit) -> Result<CircuitRc, E>,
    {
        Self::try_new(
            self.nodes
                .iter()
                .enumerate()
                .map(move |(i, circ)| f(i, circ))
                .collect::<Result<Vec<_>, _>>()?,
            self.spec.clone(),
            self.name.clone(),
        )
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let num_batchable_axes = self.info().rank() - self.spec.num_non_batchable_output_dims;
        zip(&self.nodes, &self.spec.input_batchability)
            .map(|(child, batchable)| {
                if !batchable {
                    vec![None; child.info().rank()]
                } else {
                    (0..child.info().rank())
                        .map(|i| match i < num_batchable_axes {
                            true => Some(i),
                            false => None,
                        })
                        .collect()
                }
            })
            .collect()
    }

    fn eval_tensors(
        &self,
        tensors: &[crate::py_types::Tensor],
        _device_dtype: &TorchDeviceDtype,
    ) -> Result<crate::py_types::Tensor, super::TensorEvalError> {
        Python::with_gil(|py| {
            self.spec
                .function
                .call(
                    py,
                    PyTuple::new(py, tensors.iter().map(|x| x.clone().into_py(py))),
                    None,
                )
                .map_err(|err| err.into())
                .map(|r| r.extract(py).unwrap())
        })
    }
}

impl CircuitNodeAutoName for GeneralFunction {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.children().all(|x| x.name().is_none()) {
                None
            } else {
                Some(
                    self.spec.name.clone()
                        + " "
                        + &self
                            .children()
                            .filter_map(|x| x.name().map(|y| y.to_owned()))
                            .collect::<Vec<String>>()
                            .join(" , "),
                )
            }
        })
    }
}

#[pymethods]
impl GeneralFunction {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn new(
        nodes: Vec<CircuitRc>,
        spec: GeneralFunctionSpec,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<GeneralFunction>> {
        let out = GeneralFunction::try_new(nodes, spec, name)?;

        Ok(out.into_init())
    }

    #[staticmethod]
    pub fn new_by_name(
        nodes: Vec<CircuitRc>,
        spec_name: String,
        name: Option<String>,
    ) -> Result<Self, CircuitConstructionError> {
        let spec = GENERAL_FUNCTIONS_SPECS.get(&spec_name);
        let spec = spec.ok_or(CircuitConstructionError::UnknownGeneralFunction { spec_name })?;
        GeneralFunction::try_new(nodes, spec.clone(), name)
    }
}
