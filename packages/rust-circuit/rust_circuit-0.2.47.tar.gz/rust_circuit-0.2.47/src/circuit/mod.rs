#![allow(clippy::borrow_deref_ref)]
use crate::hashmaps::{AHashSet as HashSet, FxHashMap as HashMap};
use crate::py_types::PY_MAKE_BYTES;
use crate::{pycall, pyo3_prelude::*};
use num_bigint::BigUint;
use pyo3::{exceptions, pyclass::CompareOp};
use std::hash::Hash;
use std::{
    iter::zip,
    ops::{Deref, DerefMut},
    rc::Rc,
};

use macro_rules_attribute::apply;
use std::fmt::Debug;
use thiserror::Error;

pub mod algebraic_rewrite;
pub mod batching;
pub mod canonicalize;
pub mod circuit_manipulation;
pub mod circuit_optimizer;
pub mod circuit_utils;
pub mod compiler_heuristics;
pub mod compiler_strip;
mod computational_node;
pub mod concat_rewrite;
mod constant;
pub mod debugging;
pub mod deep_rewrite;
pub mod diag_rewrite;
pub mod generalfunction;
pub mod named_axes;
pub mod nrc;
pub mod print;
mod repr;
pub mod scatter_rewrite;
pub mod scheduled_execution;
pub mod scheduling_z3;

use crate::{
    cached_lambda,
    py_types::{PyShape, Tensor, CIRCUIT_RUST_TO_PY},
    rearrange_spec::{OpSize, RearrangeSpec},
    tensor_util::{Shape, TensorAxisIndex, TensorIndex, TorchDeviceDtype, TorchDeviceDtypeOp},
    util::AsOp,
};
pub use computational_node::{
    flat_concat, Add, Concat, Einsum, EinsumAxes, Index, Rearrange, Scatter,
};
pub use generalfunction::{GeneralFunction, GeneralFunctionSpec, PyGFSpecShapeGetter};

pub use constant::{ArrayConstant, ScalarConstant, Symbol};
use uuid::uuid;

mod circuit_node_private {
    pub trait CircuitNodePrivate {
        fn info_mut(&mut self) -> &mut super::CachedCircuitInfo;
        fn name_mut(&mut self) -> &mut Option<String>;
    }
}
use circuit_node_private::*;

use self::{
    circuit_utils::total_flops,
    print::{print_circuit_stats, repr_circuit_deep_compiler},
};

pub type NamedAxes = Vec<Option<String>>;
pub trait CircuitNode: CircuitNodePrivate {
    // ==== implementable section ===
    //
    // NOTE: ALL FNS IN THIS SECTION *MUST* BE COPIED TO THE CIRCUIT NODE UNION IMPL!
    // If you add something here with a default impl, write a new impl for circuit node union!
    // (up until default section)
    //
    // we could enforce this sort of stuff with some proc macros, but seems like overkill atm.

    fn info(&self) -> &CachedCircuitInfo;
    fn name(&self) -> Option<&str>;

    fn compute_shape(&self) -> Shape;
    fn compute_hash(&self) -> blake3::Hasher; // shouldn't hash name
    fn compute_is_constant(&self) -> bool {
        self.children().all(|c| c.info().is_constant)
    }
    fn compute_is_explicitly_computable(&self) -> bool {
        self.children().all(|c| c.info().is_explicitly_computable)
    }
    fn compute_can_be_sampled(&self) -> bool {
        self.children().all(|c| c.info().can_be_sampled)
    }

    fn device_dtype_extra<'a>(&'a self) -> Box<dyn Iterator<Item = TorchDeviceDtypeOp> + 'a> {
        Box::new(std::iter::empty())
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>>;

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a>;

    fn map_children_enumerate<'a, F, E>(&'a self, f: F) -> Result<Self, CircuitConstructionError>
    where
        Self: Sized,
        CircuitConstructionError: From<E>,
        F: FnMut(usize, &'a Circuit) -> Result<CircuitRc, E>;

    fn node_type_uuid(&self) -> [u8; 16];

    fn self_flops(&self) -> BigUint {
        BigUint::from(0usize)
    }

    fn eval_tensors(
        &self,
        tensors: &[Tensor],
        device_dtype: &TorchDeviceDtype,
    ) -> Result<Tensor, TensorEvalError>;

    /// At most how many elements will evaluating this circuit require allocating
    /// new memory (that we are allowed to free ourselves) for? Used to improve scheduling.
    fn intermediate_cost_bound(&self) -> usize {
        self.info().numel_usize()
    }

    // ==== default section ===
    // FUNCTIONS BELOW HERE *shouldn't* be overridden by implementors!
    // (if you do implement, this won't be picked up on by union types!)

    fn name_cloned(&self) -> Option<String> {
        self.name().map(|x| x.to_owned())
    }

    fn compute_device_dtype(&self) -> Result<TorchDeviceDtypeOp, CircuitConstructionError> {
        self.children()
            .map(|c| c.info().device_dtype.clone())
            .chain(self.device_dtype_extra())
            .fold(Ok(TorchDeviceDtypeOp::NONE), |acc, new| {
                acc.map(|old| TorchDeviceDtypeOp::combine(old, new))?
            })
    }

    fn compute_named_axes(&self) -> NamedAxes {
        let child_axis_map = self.child_axis_map();
        let mut result: Vec<Option<String>> = vec![None; self.info().rank()];
        for (mp, child) in zip(child_axis_map, self.children()) {
            for (out_axis, name) in zip(mp, &child.info().named_axes) {
                if let Some(out_axis)=out_axis && let Some(name)=name{
                    result[out_axis]=Some(name.clone());
                }
            }
        }
        result
    }

    fn map_children<'a, F, E>(&'a self, mut f: F) -> Result<Self, CircuitConstructionError>
    where
        Self: Sized,
        CircuitConstructionError: From<E>,
        F: FnMut(&'a Circuit) -> Result<CircuitRc, E>,
    {
        self.map_children_enumerate(|_i, x| f(x))
    }

    fn map_children_idxs<'a, F, E>(&'a self, mut f: F) -> Result<Self, CircuitConstructionError>
    where
        Self: Sized,
        CircuitConstructionError: From<E>,
        F: FnMut(usize) -> Result<CircuitRc, E>,
    {
        self.map_children_enumerate(|i, _x| f(i))
    }

    fn map_children_unwrap<'a, F>(&'a self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(&'a Circuit) -> CircuitRc,
    {
        self.map_children(|x| Ok::<CircuitRc, CircuitConstructionError>(f(x)))
            .unwrap()
    }

    fn map_children_unwrap_enumerate<'a, F>(&'a self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(usize, &'a Circuit) -> CircuitRc,
    {
        self.map_children_enumerate(|i, x| Ok::<CircuitRc, CircuitConstructionError>(f(i, x)))
            .unwrap()
    }

    fn map_children_unwrap_idxs<'a, F>(&'a self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(usize) -> CircuitRc,
    {
        self.map_children_enumerate(|i, _x| Ok::<CircuitRc, CircuitConstructionError>(f(i)))
            .unwrap()
    }

    /// if any return Some, return child mapped, otherwise None
    fn map_children_op<'a, F>(&'a self, mut f: F) -> Option<Self>
    where
        Self: Sized,
        F: FnMut(&'a Circuit) -> Option<CircuitRc>,
    {
        let mut any_modified = false;
        let out = self.map_children_unwrap(|x| {
            if let Some(new) = f(x) {
                any_modified = true;
                new
            } else {
                x.clone().rc()
            }
        });
        if any_modified {
            Some(out)
        } else {
            None
        }
    }

    fn init_info(mut self) -> Result<Self, CircuitConstructionError>
    where
        Self: Sized,
    {
        let shape = self.compute_shape();
        self.info_mut().shape = shape.clone(); // set shape so methods to compute other info can use it

        let mut hasher = self.compute_hash();
        let named_axes = if self.children().any(|x| !x.info().named_axes.is_empty()) {
            self.compute_named_axes()
        } else {
            vec![None; shape.len()]
        };
        hasher.update(self.name().unwrap_or("").as_bytes());
        hasher.update(&self.node_type_uuid());
        hasher.update(uuid!("025e9af4-1366-4211-aa5f-7c28fc6cdf9f").as_bytes());
        for axis in &named_axes {
            hasher.update(axis.as_ref().unwrap_or(&"".to_owned()).as_bytes());
        }
        *self.info_mut() = CachedCircuitInfo {
            shape,
            is_constant: self.compute_is_constant(),
            is_explicitly_computable: self.compute_is_explicitly_computable(),
            can_be_sampled: self.compute_can_be_sampled(),
            hash: hasher.finalize().into(),
            max_non_input_size: self.max_non_input_size(),
            device_dtype: self.compute_device_dtype()?,
            named_axes,
        };
        Ok(self)
    }

    fn rename(mut self, new_name: Option<String>) -> Self
    where
        Self: Sized,
    {
        *self.name_mut() = new_name;
        self.init_info().unwrap() // we could avoid recomputing some stuff if we wanted
    }

    fn max_non_input_size(&self) -> BigUint {
        self.children()
            .map(|x| x.info().max_non_input_size.clone())
            .chain(std::iter::once(self.info().numel()))
            .max()
            .unwrap_or(0usize.into())
    }

    fn c(self) -> Circuit
    where
        Self: Into<Circuit>,
    {
        self.into()
    }

    fn rc(self) -> CircuitRc
    where
        Self: Into<Circuit>,
    {
        CircuitRc(Rc::new(self.c()))
    }

    fn compiler_repr(&self) -> String
    where
        Self: Into<Circuit> + Clone,
    {
        repr_circuit_deep_compiler(&self.clone().c())
    }

    fn compiler_print(&self)
    where
        Self: Into<Circuit> + Clone,
    {
        println!("{}", self.compiler_repr())
    }

    fn get_hash(&self) -> HashBytes {
        self.info().hash
    }
}

pub trait CircuitNodeAutoName: CircuitNode {
    fn auto_name(&self, name: Option<String>) -> Option<String>;
}

pub trait CircuitNodeUnion {
    fn as_trait_obj(&self) -> &dyn CircuitNode;
    fn as_trait_obj_mut(&mut self) -> &mut dyn CircuitNode;
    fn map_children_enumerate_impl<'a, F, E>(
        &'a self,
        f: F,
    ) -> Result<Self, CircuitConstructionError>
    where
        Self: Sized,
        CircuitConstructionError: From<E>,
        F: FnMut(usize, &'a Circuit) -> Result<CircuitRc, E>;
    fn variant_string(&self) -> String;
    fn node_type_uuid(&self) -> [u8; 16];
}

// not really needed to be so pedantic with ::std::...
#[macro_export]
macro_rules! circuit_node_eq_ord {
    ($type_name:ty) => {
        impl ::std::cmp::PartialEq for $type_name {
            fn eq(&self, other: &Self) -> bool {
                use $crate::circuit::prelude::*;
                self.info().hash == other.info().hash
            }
        }

        impl ::std::cmp::Eq for $type_name {}

        impl ::std::cmp::Ord for $type_name {
            fn cmp(&self, other: &Self) -> ::std::cmp::Ordering {
                use $crate::circuit::prelude::*;
                // name and then
                (self.name(), self.info().hash).cmp(&(other.name(), other.info().hash))
            }
        }

        impl ::std::cmp::PartialOrd for $type_name {
            fn partial_cmp(&self, other: &Self) -> ::std::option::Option<::std::cmp::Ordering> {
                Some(::std::cmp::Ord::cmp(self, other))
            }
        }

        impl ::std::hash::Hash for $type_name {
            fn hash<H: ::std::hash::Hasher>(&self, state: &mut H) {
                state.write(&self.info().hash[..::std::mem::size_of::<u64>()]);
            }
        }
    };
}

pub trait UnwrapToOption {
    type Item;

    fn try_unwrap(self) -> Option<Self::Item>;
}

// this is what peak rust development looks like
#[doc(hidden)]
#[macro_export]
macro_rules! define_circuit_union_impl {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        #[derive(::std::fmt::Debug, ::std::clone::Clone)]
        #[cfg_attr(feature = "real-pyo3", derive($crate::pyo3::FromPyObject))]
        pub enum $name {
            $(
                $x($x),
            )*
        }

        #[cfg(not(feature = "real-pyo3"))]
        impl<'source> $crate::pyo3::FromPyObject<'source> for $name {
            fn extract(_: &'source $crate::pyo3::PyAny) -> $crate::pyo3::PyResult<Self> {
                unimplemented!()
            }
        }


        $crate::circuit_node_eq_ord!($name);

        paste::paste! {
            $(
                impl $name {
                    pub fn [<into_ $x:snake>](self) -> Option<$crate::circuit::$x> {
                        self.into_op()
                    }
                    pub fn [<as_ $x:snake>](&self) -> Option<&$crate::circuit::$x> {
                        self.as_op()
                    }
                    pub fn [<as_mut_ $x:snake>](&mut self) -> Option<&mut $crate::circuit::$x> {
                        self.as_mut_op()
                    }
                }
                // Easy to also add macro to implement AsOp for pairs of enums to downcast.
                impl AsOp<$crate::circuit::$x> for $name {
                    fn into_op(self) -> Option<$crate::circuit::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                    fn as_op(&self) -> Option<&$crate::circuit::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                    fn as_mut_op(&mut self) -> Option<&mut $crate::circuit::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                }
            )*
        }

        impl $crate::circuit::CircuitNodeUnion for $name {
            #[inline] // hopefully inlined away?
            fn as_trait_obj(&self) -> &dyn $crate::circuit::CircuitNode {
                match self {
                    $(
                        Self::$x(node) => node,
                    )*
                }
            }

            #[inline] // hopefully inlined away?
            fn as_trait_obj_mut(&mut self) -> &mut dyn $crate::circuit::CircuitNode {
                match self {
                    $(
                        Self::$x(node) => node,
                    )*
                }
            }

            fn map_children_enumerate_impl<'a, F, E>(&'a self, f: F) -> Result<Self, $crate::circuit::CircuitConstructionError>
            where
                $crate::circuit::CircuitConstructionError: From<E>,
                F: FnMut(usize,&'a $crate::circuit::Circuit) -> Result<$crate::circuit::CircuitRc, E>,
            {
                match self {
                    $(
                        Self::$x(node) => $crate::circuit::CircuitNode::map_children_enumerate(node, f).map(|v| Self::$x(v)),
                    )*
                }
            }

            fn variant_string(&self) -> String {
                match self {
                    $(
                        Self::$x(_) => stringify!($x).to_owned(),
                    )*
                }
            }
            fn node_type_uuid(&self) ->[u8;16]{
                match self {
                    $(
                        Self::$x(node) => node.node_type_uuid(),
                    )*
                }
            }

        }

        $(
            impl From<$x> for $name {
                fn from(item: $x) -> Self {
                    Self::$x(item)
                }
            }
        )*

        impl $crate::pyo3::IntoPy<$crate::pyo3::PyObject> for $name {
            fn into_py(self, py: $crate::pyo3::Python<'_>) -> $crate::pyo3::PyObject {
                #[cfg(feature = "real-pyo3")]
                match self {
                    $(
                        Self::$x(node) => $crate::pyo3::IntoPy::into_py(node, py),
                    )*
                }

                #[cfg(not(feature = "real-pyo3"))]
                unimplemented!()
            }
        }
    }
}

macro_rules! define_circuit {
    [$($x:ident),+ $(,)?] => {
        define_circuit_union_impl!(Circuit {$($x,)*});
    }
}

define_circuit!(
    Einsum,
    ArrayConstant,
    Symbol,
    ScalarConstant,
    Add,
    Rearrange,
    Index,
    GeneralFunction,
    Concat,
    Scatter,
);

/// Define adhoc unions of different circuit types
///
/// # Example
///
/// ```
/// # use rust_circuit::{
/// #     circuit::{ArrayConstant, ScalarConstant, Symbol, CircuitNodeUnion, CircuitNode, Circuit},
/// #     define_circuit_union, util::AsOp, sv
/// # };
/// # use uuid::Uuid;
///
/// define_circuit_union!(SomeConst {
///     ScalarConstant,
///     Symbol,
///     ArrayConstant,
/// });
///
/// let values = [
///     SomeConst::ScalarConstant(ScalarConstant::new(0.2, sv![3], Some("first".to_owned()))),
///     SomeConst::Symbol(Symbol::new(sv![3], Uuid::new_v4(), Some("second".to_owned()))),
/// ];
///
/// assert_eq!(values[0].name(), Some("first"));
/// assert_eq!(values[1].name(), Some("second"));
/// assert_eq!(values[0].variant_string(), "ScalarConstant".to_owned());
/// assert_eq!(values[1].variant_string(), "Symbol".to_owned());
///
/// // we can convert to full circuit also
/// let values_circuit : Vec<Circuit> = values.iter().cloned().map(Into::into).collect();
/// ```
#[macro_export]
macro_rules! define_circuit_union {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        $crate::define_circuit_union_impl!($name {$($x,)*});

        impl ::std::convert::From<$name> for $crate::circuit::Circuit {
            fn from(item: $name) -> Self {
                match item {
                    $(
                        $name::$x(node) => node.into(),
                    )*
                }
            }
        }
    }
}

// work around for fact that we can't implement foreign trait on constrained type
#[macro_export]
macro_rules! circuit_node_extra_impl {
    ($type_name:ident) => {
        $crate::circuit_node_eq_ord!($type_name);

        impl $crate::circuit::CircuitNodePrivate for $type_name {
            fn info_mut(&mut self) -> &mut $crate::circuit::CachedCircuitInfo {
                &mut self.info
            }
            fn name_mut(&mut self) -> &mut Option<String> {
                &mut self.name
            }
        }

        #[cfg(feature = "real-pyo3")]
        impl $type_name {
            fn into_init(self) -> PyClassInitializer<Self> {
                // kinda awkward clone... (but probably basically free)
                (
                    self.clone(),
                    $crate::circuit::PyCircuitBase(::std::rc::Rc::new(self.c())),
                )
                    .into()
            }
        }

        impl IntoPy<PyObject> for $type_name {
            fn into_py(self, py: Python<'_>) -> PyObject {
                // this is slightly gross. I wonder if possible to do better?
                // when does this unwrap fail?
                #[cfg(feature = "real-pyo3")]
                {
                    Py::new(py, self.into_init()).unwrap().into_py(py)
                }

                #[cfg(not(feature = "real-pyo3"))]
                unimplemented!()
            }
        }
    };
}

#[macro_export]
macro_rules! circuit_node_auto_impl {
    ($the_uuid:literal) => {
        fn info(&self) -> &$crate::circuit::CachedCircuitInfo {
            &self.info
        }
        fn name(&self) -> Option<&str> {
            self.name.as_deref()
        }
        fn node_type_uuid(&self) -> [u8; 16] {
            *uuid::uuid!($the_uuid).as_bytes()
        }
    };
}

impl<T: CircuitNodeUnion> CircuitNodePrivate for T {
    fn info_mut(&mut self) -> &mut CachedCircuitInfo {
        self.as_trait_obj_mut().info_mut()
    }
    fn name_mut(&mut self) -> &mut Option<String> {
        self.as_trait_obj_mut().name_mut()
    }
}

// UPDATE ME WHEN YOU CHANGE CircuitNode Trait!!!
impl<T: CircuitNodeUnion> CircuitNode for T {
    fn info(&self) -> &CachedCircuitInfo {
        self.as_trait_obj().info()
    }

    fn name(&self) -> Option<&str> {
        self.as_trait_obj().name()
    }

    fn compute_shape(&self) -> Shape {
        self.as_trait_obj().compute_shape()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let hasher = self.as_trait_obj().compute_hash();
        hasher
    }

    fn compute_is_constant(&self) -> bool {
        self.as_trait_obj().compute_is_constant()
    }

    fn compute_is_explicitly_computable(&self) -> bool {
        self.as_trait_obj().compute_is_explicitly_computable()
    }

    fn compute_can_be_sampled(&self) -> bool {
        self.as_trait_obj().compute_can_be_sampled()
    }

    fn device_dtype_extra<'a>(&'a self) -> Box<dyn Iterator<Item = TorchDeviceDtypeOp> + 'a> {
        self.as_trait_obj().device_dtype_extra()
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.as_trait_obj().child_axis_map()
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        self.as_trait_obj().children()
    }

    fn map_children_enumerate<'a, F, E>(&'a self, f: F) -> Result<Self, CircuitConstructionError>
    where
        CircuitConstructionError: From<E>,
        F: FnMut(usize, &'a Circuit) -> Result<CircuitRc, E>,
    {
        self.map_children_enumerate_impl(f)
    }

    fn node_type_uuid(&self) -> [u8; 16] {
        self.as_trait_obj().node_type_uuid()
    }

    fn self_flops(&self) -> BigUint {
        self.as_trait_obj().self_flops()
    }

    fn eval_tensors(
        &self,
        tensors: &[Tensor],
        device_dtype: &TorchDeviceDtype,
    ) -> Result<Tensor, TensorEvalError> {
        self.as_trait_obj().eval_tensors(tensors, device_dtype)
    }

    fn intermediate_cost_bound(&self) -> usize {
        self.as_trait_obj().intermediate_cost_bound()
    }
}

pub type HashBytes = [u8; 32];
#[derive(Clone, Copy, Hash, PartialEq, Eq)]
pub struct PyHashBytes(pub [u8; 32]);
impl IntoPy<PyObject> for PyHashBytes {
    fn into_py(self, _py: Python<'_>) -> PyObject {
        pycall!(PY_MAKE_BYTES, (self.0,))
    }
}

#[derive(Clone, Default)]
pub struct CachedCircuitInfo {
    pub shape: Shape,
    pub is_constant: bool,
    pub is_explicitly_computable: bool,
    pub can_be_sampled: bool,
    pub hash: HashBytes,
    pub max_non_input_size: BigUint,
    pub device_dtype: TorchDeviceDtypeOp,
    pub named_axes: NamedAxes,
}

/// don't want to print hash with Debug, for now just print shape
impl Debug for CachedCircuitInfo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.shape)
    }
}

impl CachedCircuitInfo {
    pub fn numel(&self) -> BigUint {
        self.shape.iter().map(|x| BigUint::from(*x)).product()
    }
    /// Saturating element count
    pub fn numel_usize(&self) -> usize {
        let numel_digits = self.numel().to_u64_digits();
        if numel_digits.len() == 1 {
            numel_digits[0] as usize
        } else {
            usize::MAX
        }
    }
    pub fn rank(&self) -> usize {
        self.shape.len()
    }
    pub fn hash_usize(&self) -> usize {
        let mut hash_prefix: [u8; 8] = Default::default();
        hash_prefix.copy_from_slice(&self.hash[..8]);
        usize::from_le_bytes(hash_prefix)
    }
}

#[derive(Error, Debug, Clone)]
pub enum CircuitConstructionError {
    #[error("len shape different from len axes (len axes: {len_axes}, len shape: {circuit_len_shape}, circuit name: {circuit_name:?})")]
    EinsumLenShapeDifferentFromAxes {
        circuit_name: Option<String>,
        circuit_len_shape: usize,
        len_axes: usize,
    },
    #[error("shape different for axis (axis: {axis}, shape: {circuit_shape}, existing_shape: {existing_shape} circuit name: {circuit_name:?})")]
    EinsumShapeDifferent {
        circuit_name: Option<String>,
        circuit_shape: usize,
        axis: usize,
        existing_shape: usize,
    },
    #[error("output not subset, TODO error")]
    EinsumOutputNotSubset {
        // TODO: args
    },

    #[error("Sum nodes not broadcastable, {shapes:?}")]
    SumNotBroadcastable { shapes: Vec<Shape> },

    #[error("Rearrange takes different input shape, shape: {shape:?} spec: {spec:?}")]
    RearrangeWrongInputShape { spec: RearrangeSpec, shape: Shape },

    #[error("Invalid rearrange spec {spec:?}")]
    InvalidRearrangeSpec { spec: RearrangeSpec },

    #[error("Wrong input shapes for GeneralFunction {input_shapes:?} {gf_spec:?}")]
    GeneralFunctionWrongInputShape {
        gf_spec: GeneralFunctionSpec,
        input_shapes: Vec<Shape>,
    },

    #[error("Concat requires at least one node")]
    ConcatZeroNodes {},

    #[error("Concat nodes have different shapes {shapes:?}")]
    ConcatShapeDifferent { shapes: Vec<Shape> },

    #[error("index rank too high: {index_rank} vs {node_rank}")]
    IndexRankTooHigh { index_rank: usize, node_rank: usize },

    #[error("Index out of bounds, {index:?} {shape:?}")]
    IndexOutOfBounds { index: TensorIndex, shape: Shape },

    #[error("Scatter shape wrong, index: {index_shape:?} child: {shape:?} {index:?}")]
    ScatterShapeWrong {
        index: TensorIndex,
        shape: Shape,
        index_shape: Shape,
    },

    #[error("Scatter not supported yet, {index:?}")]
    ScatterUnimplemented { index: TensorIndex },

    #[error("Children multiple dtypes {a:?} {b:?}")]
    ChildrenMultipleDtypes {
        a: Option<String>,
        b: Option<String>,
    },

    #[error("Children multiple dtypes {a:?} {b:?}")]
    ChildrenMultipleDevices {
        a: Option<String>,
        b: Option<String>,
    },

    #[error("Unknown GeneralFunction name {spec_name}")]
    UnknownGeneralFunction { spec_name: String },

    #[error("python error {py_err:?}")]
    PythonError { py_err: Rc<PyErr> },
}

impl From<CircuitConstructionError> for PyErr {
    fn from(err: CircuitConstructionError) -> Self {
        PyErr::new::<exceptions::PyValueError, _>(format!("error (TODO: better) {}", err))
    }
}

impl From<PyErr> for CircuitConstructionError {
    fn from(py_err: PyErr) -> Self {
        CircuitConstructionError::PythonError {
            py_err: Rc::new(py_err),
        }
    }
}

#[derive(Error, Debug, Clone)]
pub enum TensorEvalError {
    #[error("not explicitly computable: {circuit:?})")]
    NotExplicitlyComputable { circuit: CircuitRc },
    #[error("python error {py_err:?}")]
    PythonError { py_err: Rc<PyErr> }, // PyErr doesn't have .clone, so Rc-ing
}

impl From<TensorEvalError> for PyErr {
    fn from(err: TensorEvalError) -> Self {
        PyErr::new::<exceptions::PyValueError, _>(format!("{}", err))
    }
}

impl From<PyErr> for TensorEvalError {
    fn from(py_err: PyErr) -> Self {
        TensorEvalError::PythonError {
            py_err: Rc::new(py_err),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct CircuitRc(Rc<Circuit>);

pub fn make_children_zero<T: CircuitNode>(circuit: &T) -> T {
    circuit.map_children_unwrap(&mut |child: &Circuit| {
        ScalarConstant::new(0.0, child.info().shape.clone(), child.name_cloned()).rc()
    })
}

pub fn evaluate_fn(circ: &Circuit) -> Result<Tensor, TensorEvalError> {
    let device_dtype = get_compatible_dtype(circ);
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: Circuit) -> Result<Tensor, TensorEvalError> {
        let child_tensors: Result<Vec<Tensor>, TensorEvalError> =
            circ.children().map(|x| recurse((**x).clone())).collect();
        let child_tensors = child_tensors?;

        circ.eval_tensors(&child_tensors, &device_dtype)
    }

    recurse(circ.clone())
}

pub fn deep_map<F>(circuit: &Circuit, f: F) -> Result<CircuitRc, CircuitConstructionError>
where
    F: Fn(&Circuit) -> Result<CircuitRc, CircuitConstructionError>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: &Circuit) -> Result<CircuitRc, CircuitConstructionError> {
        let inner_mapped = circ.map_children(&mut recurse)?;
        f(&inner_mapped)
    }
    recurse(circuit)
}

pub fn deep_map_preorder<F>(circuit: &Circuit, f: F) -> Result<CircuitRc, CircuitConstructionError>
where
    F: Fn(&Circuit) -> Result<CircuitRc, CircuitConstructionError>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: &Circuit) -> Result<CircuitRc, CircuitConstructionError> {
        f(circ)?.map_children(&mut recurse).map(|z| z.rc())
    }
    recurse(circuit)
}

pub fn deep_map_unwrap<F>(circuit: &Circuit, f: F) -> CircuitRc
where
    F: Fn(&Circuit) -> CircuitRc,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: &Circuit) -> CircuitRc {
        let inner_mapped = circ.map_children_unwrap(&mut recurse);
        f(&inner_mapped)
    }
    recurse(circuit)
}

/// this applies the function to parent before children, as opposed to deep_map_unwrap, which is children first
pub fn deep_map_unwrap_preorder<F>(circuit: &Circuit, f: F) -> CircuitRc
where
    F: Fn(&Circuit) -> CircuitRc,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: &Circuit) -> CircuitRc {
        f(circ).map_children_unwrap(&mut recurse).rc()
    }
    recurse(circuit)
}

/// visits each subcircuit that's in any circuit once! (pre-order traversal if it's a tree)
pub fn visit_circuit<F>(circuit: &Circuit, mut f: F)
where
    F: FnMut(&Circuit),
{
    let mut seen: HashSet<HashBytes> = HashSet::new();

    fn recurse<F>(circ: &Circuit, seen: &mut HashSet<HashBytes>, f: &mut F)
    where
        F: FnMut(&Circuit),
    {
        if !seen.contains(&circ.info().hash) {
            seen.insert(circ.info().hash);
            f(circ);
            for child in circ.children() {
                recurse(&child, seen, f)
            }
        }
    }
    recurse(circuit, &mut seen, &mut f);
}

pub fn visit_circuit_fallable<F, E>(circuit: &Circuit, mut f: F) -> Result<(), E>
where
    F: FnMut(&Circuit) -> Result<(), E>,
{
    let mut seen: HashSet<HashBytes> = HashSet::new();

    fn recurse<F, E>(circ: &Circuit, seen: &mut HashSet<HashBytes>, f: &mut F) -> Result<(), E>
    where
        F: FnMut(&Circuit) -> Result<(), E>,
    {
        if !seen.contains(&circ.info().hash) {
            seen.insert(circ.info().hash);
            f(circ)?;
            for child in circ.children() {
                recurse(&child, seen, f)?
            }
        }
        Ok(())
    }
    recurse(circuit, &mut seen, &mut f)
}

pub fn visit_circuit_postorder<F>(circuit: &Circuit, mut f: F)
where
    F: FnMut(&Circuit),
{
    let mut seen: HashSet<HashBytes> = HashSet::new();

    fn recurse<F>(circ: &Circuit, seen: &mut HashSet<HashBytes>, f: &mut F)
    where
        F: FnMut(&Circuit),
    {
        if !seen.contains(&circ.info().hash) {
            seen.insert(circ.info().hash);
            for child in circ.children() {
                recurse(&child, seen, f)
            }
            f(circ);
        }
    }
    recurse(circuit, &mut seen, &mut f);
}

pub fn deep_map_op<F>(circuit: &Circuit, f: F) -> Option<CircuitRc>
where
    F: Fn(&Circuit) -> Option<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: &Circuit) -> Option<CircuitRc> {
        let inner_mapped = circ.map_children_op(&mut recurse);
        inner_mapped
            .map(|x| x.and_then_or_clone(&f))
            .or_else(|| f(circ))
    }
    recurse(circuit)
}

pub fn deep_map_pre_new_children<F>(circuit: &Circuit, f: F) -> CircuitRc
where
    F: Fn(&Circuit, &Vec<CircuitRc>) -> CircuitRc,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: &Circuit) -> CircuitRc {
        let old_children: Vec<CircuitRc> = circ.children().collect();
        let new_children = old_children.iter().map(|x| &***x).map(recurse).collect();
        f(circ, &new_children)
    }
    recurse(circuit)
}

pub fn deep_map_op_pre_new_children<F>(circuit: &Circuit, f: F) -> Option<CircuitRc>
where
    F: Fn(&Circuit, &Vec<CircuitRc>) -> Option<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: &Circuit) -> Option<CircuitRc> {
        let old_children: Vec<CircuitRc> = circ.children().collect();
        let new_children: Vec<Option<CircuitRc>> =
            old_children.iter().map(|x| &***x).map(recurse).collect();
        if new_children.iter().all(|x| x.is_none()) {
            f(circ, &old_children)
        } else {
            let new_real_children = zip(old_children, new_children)
                .map(|(old, new)| new.unwrap_or(old))
                .collect();
            Some(f(circ, &new_real_children).unwrap_or_else(|| {
                circ.map_children_unwrap_idxs(|i| new_real_children[i].clone())
                    .rc()
            }))
        }
    }
    recurse(circuit)
}

pub fn apply_fn_cache<I, K, O, F, FK>(i: &I, f: F, c: &mut HashMap<K, O>, fk: FK) -> O
where
    F: Fn(&I) -> O,
    FK: Fn(&I) -> K,
    O: Clone,
    K: Eq + Hash,
{
    let k = fk(i);
    match c.get(&k) {
        Some(r) => r.clone(),
        None => {
            let r = f(i);
            c.insert(k, r.clone());
            r
        }
    }
}

pub fn deep_map_op_context<F, C>(
    circuit: &Circuit,
    f: &F,
    context: &mut C,
    self_cache: &mut HashMap<HashBytes, Option<CircuitRc>>,
) -> Option<CircuitRc>
where
    F: Fn(&Circuit, &mut C) -> Option<CircuitRc>,
{
    if let Some(z) = self_cache.get(&circuit.info().hash) {
        return z.clone();
    }
    let inner_mapped = circuit.map_children_op(|x| deep_map_op_context(x, f, context, self_cache));
    let result = match inner_mapped {
        Some(z) => f(&z, context).or(Some(z.rc())),
        None => f(circuit, context),
    };
    self_cache.insert(circuit.info().hash, result.clone());
    result
}

pub fn evaluate_fn_uncached(
    circ: &Circuit,
    device_dtype: &TorchDeviceDtype,
) -> Result<Tensor, TensorEvalError> {
    let child_tensors: Result<Vec<Tensor>, TensorEvalError> = circ
        .children()
        .map(|x| evaluate_fn_uncached(&x, device_dtype))
        .collect();
    let child_tensors = child_tensors?;

    circ.eval_tensors(&child_tensors, device_dtype)
}

impl IntoPy<PyObject> for CircuitRc {
    fn into_py(self, py: Python<'_>) -> PyObject {
        #[cfg(feature = "real-pyo3")]
        {
            (*self.0).clone().into_py(py)
        }

        #[cfg(not(feature = "real-pyo3"))]
        unimplemented!()
    }
}

impl<'source> FromPyObject<'source> for CircuitRc {
    fn extract(circuit_obj: &'source PyAny) -> PyResult<Self> {
        #[cfg(feature = "real-pyo3")]
        {
            let circ: Circuit = circuit_obj.extract()?;
            Ok(circ.rc())
        }

        #[cfg(not(feature = "real-pyo3"))]
        unimplemented!()
    }
}

impl<T: CircuitNode + Into<Circuit>> From<T> for CircuitRc {
    fn from(x: T) -> Self {
        x.rc()
    }
}

impl From<Rc<Circuit>> for CircuitRc {
    fn from(x: Rc<Circuit>) -> Self {
        CircuitRc(x)
    }
}

impl Deref for CircuitRc {
    type Target = Rc<Circuit>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for CircuitRc {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[pyclass(unsendable, subclass, name = "Circuit")]
#[derive(Clone, Debug)]
pub struct PyCircuitBase(Rc<Circuit>);

impl Deref for PyCircuitBase {
    type Target = Rc<Circuit>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for PyCircuitBase {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

fn use_rust_comp<T: PartialOrd>(l: &T, r: &T, comp_op: CompareOp) -> bool {
    match comp_op {
        CompareOp::Lt => l < r,
        CompareOp::Gt => l > r,
        CompareOp::Le => l <= r,
        CompareOp::Ge => l >= r,
        CompareOp::Eq => l == r,
        CompareOp::Ne => l != r,
    }
}

fn python_apply_fn_to_sub<N: CircuitNode>(
    node: &N,
    f: PyObject,
) -> Result<N, CircuitConstructionError> {
    node.map_children(|c| {
        Python::with_gil(|py| -> Result<_, CircuitConstructionError> {
            let out = f.call1(py, (c.clone(),))?.extract::<CircuitRc>(py)?;
            Ok(out)
        })
    })
}

pub fn circuit_rust_to_py(circ: CircuitRc) -> PyObject {
    Python::with_gil(|py| CIRCUIT_RUST_TO_PY.call(py, (circ,), None).unwrap())
}

#[pymethods]
impl PyCircuitBase {
    #[getter]
    fn shape(&self) -> PyShape {
        PyShape(self.info().shape.clone())
    }

    #[getter]
    fn is_constant(&self) -> bool {
        self.info().is_constant
    }

    #[getter]
    fn is_explicitly_computable(&self) -> bool {
        self.info().is_explicitly_computable
    }

    #[getter]
    fn can_be_sampled(&self) -> bool {
        self.info().can_be_sampled
    }

    #[getter]
    fn name(&self) -> &str {
        self.0.name().unwrap_or("")
    }

    #[getter]
    fn intermediate_cost_bound(&self) -> usize {
        self.0.intermediate_cost_bound()
    }

    // TODO: probably could be more efficient...
    fn children(&self) -> Vec<CircuitRc> {
        self.0.children().collect()
    }

    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self.0, &object.0, comp_op)
    }

    #[getter]
    fn hash(&self) -> PyHashBytes {
        PyHashBytes(self.info().hash)
    }

    fn __hash__(&self) -> u64 {
        u64::from_le_bytes(
            self.info().hash[..std::mem::size_of::<u64>()]
                .try_into()
                .unwrap(),
        )
    }

    pub fn self_flops(&self) -> BigUint {
        self.0.self_flops()
    }

    pub fn total_flops(&self) -> BigUint {
        total_flops((*self.0).clone().rc())
    }

    pub fn max_non_input_size(&self) -> BigUint {
        (*self.0).info().max_non_input_size.clone()
    }

    pub fn print_stats(&self) {
        print_circuit_stats(&self.0)
    }
    // TODO: rename for rust consistency?
    pub fn apply_fn_to_sub(&self, f: PyObject) -> PyResult<Circuit> {
        let out = python_apply_fn_to_sub(&*self.0, f)?;
        Ok(out)
    }

    fn compiler_repr(&self) -> String {
        repr_circuit_deep_compiler(self)
    }

    fn compiler_print(&self) {
        println!("{}", self.compiler_repr())
    }

    fn numel(&self) -> BigUint {
        self.0.info().numel()
    }

    fn rank(&self) -> usize {
        self.0.info().rank()
    }

    fn to_py(&self) -> PyObject {
        circuit_rust_to_py(CircuitRc(self.0.clone()))
    }

    fn evaluate(&self) -> Result<Tensor, TensorEvalError> {
        evaluate_fn(self)
    }
}

// TODO: prelude!
pub fn get_compatible_dtype(circ: &Circuit) -> TorchDeviceDtype {
    circ.info().device_dtype.clone().unwrap_or_defaults()
}

pub mod prelude {
    pub use super::{
        Circuit, CircuitConstructionError, CircuitNode, CircuitNodeAutoName, CircuitNodeUnion,
        CircuitRc,
    };
}
