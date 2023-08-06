use smallvec::Array;
use uuid::Uuid;

use super::{OpSize, RearrangeSpec, TensorAxisIndex, TensorIndex};
use crate::{all_imports::TorchDeviceDtypeOp, smallvec::Sv, tensor_util::Shape};

pub trait RustRepr {
    /// Serialize objects to Rust expression source code
    fn repr(&self) -> String;
}

impl RustRepr for u8 {
    fn repr(&self) -> String {
        format!("{}", self)
    }
}
impl RustRepr for usize {
    fn repr(&self) -> String {
        format!("{}", self)
    }
}
impl RustRepr for i64 {
    fn repr(&self) -> String {
        format!("{}", self)
    }
}
impl RustRepr for f64 {
    fn repr(&self) -> String {
        format!("{}_f64", self)
    }
}
impl RustRepr for OpSize {
    fn repr(&self) -> String {
        format!("OpSize::from({})", Option::<usize>::from(*self).repr())
    }
}
impl RustRepr for String {
    fn repr(&self) -> String {
        format!("\"{}\".to_owned()", self)
    }
}
impl RustRepr for Uuid {
    fn repr(&self) -> String {
        format!("uuid!(\"{}\")", self)
    }
}

impl<T: RustRepr> RustRepr for Option<T> {
    fn repr(&self) -> String {
        match self {
            Some(x) => format!("Some({})", x.repr()),
            None => "None".to_owned(),
        }
    }
}

impl<T: RustRepr> RustRepr for Vec<T> {
    fn repr(&self) -> String {
        let strings: Vec<String> = self.iter().map(|s| s.repr()).collect();
        format!("vec![{}]", strings.join(","))
    }
}

impl<T: Array> RustRepr for Sv<T>
where
    T::Item: RustRepr,
{
    fn repr(&self) -> String {
        let strings: Vec<String> = self.iter().map(|s| s.repr()).collect();
        format!("sv![{}]", strings.join(","))
    }
}

impl RustRepr for RearrangeSpec {
    fn repr(&self) -> String {
        format!(
            "RearrangeSpec::new({}, {}, {})",
            self.input_ints.repr(),
            self.output_ints.repr(),
            self.int_sizes.repr()
        )
    }
}

impl RustRepr for TorchDeviceDtypeOp {
    fn repr(&self) -> String {
        if let (None, None) = (&self.device, &self.dtype) {
            "TorchDeviceDtypeOp::default()".to_owned()
        } else {
            format!(
                "TorchDeviceDtypeOp {{ device: {}, dtype: {} }}",
                self.device.repr(),
                self.dtype.repr(),
            )
        }
    }
}

pub struct ReprWrapper(pub String);

impl RustRepr for ReprWrapper {
    fn repr(&self) -> String {
        self.0.clone()
    }
}

impl TensorAxisIndex {
    pub fn repr(&self, bound: usize, device_dtype: &TorchDeviceDtypeOp) -> String {
        match self {
            TensorAxisIndex::Single(i) => format!("TensorAxisIndex::Single({})", i),
            TensorAxisIndex::Tensor(t) => {
                format!(
                    "TensorAxisIndex::new_tensor_randint_seeded({}, {}, {}, {})",
                    t.shape()[0].repr(),
                    bound.repr(),
                    device_dtype.repr(),
                    t.hash_usize().unwrap(),
                )
            }
            TensorAxisIndex::Slice(s) => format!(
                "TensorAxisIndex::Slice(Slice {{ start:{}, stop:{} }})",
                s.start.repr(),
                s.stop.repr()
            ),
        }
    }
}

impl TensorIndex {
    pub fn repr(&self, shape: Shape, device_dtype: &TorchDeviceDtypeOp) -> String {
        // shape: shape of the tensor we're indexing into
        format!(
            "TensorIndex ( vec![{}] )",
            self.0
                .iter()
                .enumerate()
                .map(|(i, tensor_axis_index)| tensor_axis_index.repr(shape[i], device_dtype))
                .collect::<Vec<String>>()
                .join(", ")
        )
    }
}
