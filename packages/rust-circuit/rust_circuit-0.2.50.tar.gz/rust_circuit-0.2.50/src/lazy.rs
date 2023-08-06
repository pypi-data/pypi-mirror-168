use pyo3::{once_cell::GILOnceCell, Python};
use std::{
    cell::Cell,
    ops::{Deref, DerefMut},
    panic::RefUnwindSafe,
};

/// A value which is initialized on the first access based on
/// [`once_cell::sync::Lazy`](https://docs.rs/once_cell/1.14.0/once_cell/sync/struct.Lazy.html).
///
/// This type is thread-safe and can be used in statics.
///
/// # Example
///
/// ```
/// use std::collections::HashMap;
///
/// use rust_circuit::lazy::GILLazy;
///
/// pyo3::prepare_freethreaded_python();
///
/// static HASHMAP: GILLazy<HashMap<i32, String>> = GILLazy::new(|| {
///     println!("initializing");
///     let mut m = HashMap::new();
///     m.insert(13, "Spica".to_string());
///     m.insert(74, "Hoyten".to_string());
///     m
/// });
///
/// fn main() {
///     println!("ready");
///     std::thread::spawn(|| {
///         println!("{:?}", HASHMAP.get(&13));
///     })
///     .join()
///     .unwrap();
///     println!("{:?}", HASHMAP.get(&74));
///
///     // Prints:
///     //   ready
///     //   initializing
///     //   Some("Spica")
///     //   Some("Hoyten")
/// }
/// ```
///
/// TODO: contribute to pyo3!
pub struct GILLazyPy<T, F = for<'py> fn(Python<'py>) -> T> {
    cell: GILOnceCell<T>,
    init: Cell<Option<F>>,
}

pub struct PyCallWrap<F>(F);

pub type GILLazy<T, S = PyCallWrap<fn() -> T>> = GILLazyPy<T, S>;

// We never create a `&F` from a `&GILLazyPy<T, F>` so it is fine to not impl
// `Sync` for `F`. We do create a `&mut Option<F>` in `force`, but this is
// properly synchronized, so it only happens once so it also does not
// contribute to this impl.
// TODO: is this ok with GILOnceCell????
unsafe impl<T, F: Send> Sync for GILLazyPy<T, F> where GILOnceCell<T>: Sync {}
// auto-derived `Send` impl is OK.

impl<T, F: RefUnwindSafe> RefUnwindSafe for GILLazyPy<T, F> where GILOnceCell<T>: RefUnwindSafe {}

impl<T, F> GILLazyPy<T, PyCallWrap<F>> {
    /// Creates a new lazy value with the given initializing
    /// function.
    pub const fn new(f: F) -> GILLazyPy<T, PyCallWrap<F>> {
        GILLazyPy {
            cell: GILOnceCell::new(),
            init: Cell::new(Some(PyCallWrap(f))),
        }
    }
}

impl<T, F> GILLazyPy<T, F> {
    pub const fn new_py(f: F) -> GILLazyPy<T, F> {
        GILLazyPy {
            cell: GILOnceCell::new(),
            init: Cell::new(Some(f)),
        }
    }
}

pub trait MaybePyCallable<T> {
    fn call<'py>(self, py: Python<'py>) -> T;
}

impl<T, F: for<'py> FnOnce(Python<'py>) -> T> MaybePyCallable<T> for F {
    fn call<'py>(self, py: Python<'py>) -> T {
        self(py)
    }
}

impl<T, F: FnOnce() -> T> MaybePyCallable<T> for PyCallWrap<F> {
    fn call<'py>(self, _: Python<'py>) -> T {
        self.0()
    }
}

impl<T, F: MaybePyCallable<T>> GILLazyPy<T, F> {
    /// Forces the evaluation of this lazy value and
    /// returns a reference to the result. This is equivalent
    /// to the `Deref` impl, but is explicit.
    ///
    /// # Example
    /// ```
    /// use rust_circuit::lazy::GILLazyPy;
    ///
    /// pyo3::prepare_freethreaded_python();
    ///
    /// let lazy = GILLazyPy::new(|| 92);
    ///
    /// assert_eq!(GILLazyPy::force(&lazy), &92);
    /// assert_eq!(&*lazy, &92);
    /// ```
    pub fn force(this: &GILLazyPy<T, F>) -> &T {
        Python::with_gil(|py| {
            this.cell.get_or_init(py, || match this.init.take() {
                Some(f) => f.call(py),
                None => panic!("GILLazyPy instance has previously been poisoned"),
            })
        })
    }

    /// Forces the evaluation of this lazy value and
    /// returns a mutable reference to the result. This is equivalent
    /// to the `Deref` impl, but is explicit.
    ///
    /// # Example
    /// ```
    /// use rust_circuit::lazy::GILLazyPy;
    ///
    /// pyo3::prepare_freethreaded_python();
    ///
    /// let mut lazy = GILLazyPy::new(|| 92);
    ///
    /// assert_eq!(GILLazyPy::force_mut(&mut lazy), &mut 92);
    /// ```
    pub fn force_mut(this: &mut GILLazyPy<T, F>) -> &mut T {
        Self::force(this);
        Self::get_mut(this).unwrap_or_else(|| unreachable!())
    }

    /// Gets the reference to the result of this lazy value if
    /// it was initialized, otherwise returns `None`.
    ///
    /// # Example
    /// ```
    /// use rust_circuit::lazy::GILLazyPy;
    ///
    /// pyo3::prepare_freethreaded_python();
    ///
    /// let lazy = GILLazyPy::new(|| 92);
    ///
    /// assert_eq!(GILLazyPy::get(&lazy), None);
    /// assert_eq!(&*lazy, &92);
    /// assert_eq!(GILLazyPy::get(&lazy), Some(&92));
    /// ```
    pub fn get(this: &GILLazyPy<T, F>) -> Option<&T> {
        Python::with_gil(|py| this.cell.get(py))
    }

    /// Gets the reference to the result of this lazy value if
    /// it was initialized, otherwise returns `None`.
    ///
    /// # Example
    /// ```
    /// use rust_circuit::lazy::GILLazyPy;
    ///
    /// pyo3::prepare_freethreaded_python();
    ///
    /// let mut lazy = GILLazyPy::new(|| 92);
    ///
    /// assert_eq!(GILLazyPy::get_mut(&mut lazy), None);
    /// assert_eq!(&*lazy, &92);
    /// assert_eq!(GILLazyPy::get_mut(&mut lazy), Some(&mut 92));
    /// ```
    pub fn get_mut(this: &mut GILLazyPy<T, F>) -> Option<&mut T> {
        this.cell.get_mut()
    }
}

impl<T, F: MaybePyCallable<T>> Deref for GILLazyPy<T, F> {
    type Target = T;
    fn deref(&self) -> &T {
        GILLazyPy::force(self)
    }
}

impl<T, F: MaybePyCallable<T>> DerefMut for GILLazyPy<T, F> {
    fn deref_mut(&mut self) -> &mut T {
        GILLazyPy::force(self);
        self.cell.get_mut().unwrap_or_else(|| unreachable!())
    }
}

impl<T: Default> Default for GILLazy<T> {
    /// Creates a new lazy value using `Default` as the initializing function.
    fn default() -> GILLazy<T> {
        GILLazyPy::new(T::default)
    }
}

/// use via [macro_rules_attribute::apply](https://docs.rs/macro_rules_attribute/latest/macro_rules_attribute/)
#[macro_export]
macro_rules! make_lazy {
    {
        $( #[doc = $d:literal] )*
        $( #[lazy_ty($($which_lazy:tt)*)] )?
        $( #[lazy_name($lazy_name:ident)] )?
        $vi:vis fn $name:ident () -> $ret_ty:ty
        { $($tt:tt)* }
    } => {
        $(#[doc = $d])*
        $vi fn $name() -> $ret_ty {
            $($tt)*
        }


        $crate::make_lazy!(@lazy_impl $( #[doc = $d] )* $( #[lazy_ty($($which_lazy)*)] )* $( #[lazy_name($lazy_name)] )* {$vi $name; $ret_ty});
    };
    {
        @lazy_impl
        $( #[doc = $d:literal] )*
        #[lazy_ty($($which_lazy:tt)*)]
        #[lazy_name($lazy_name:ident)]
        {$vis:vis $name:ident; $ret_ty:ty}
    } => {
        $(#[doc = $d])*
        $vis static $lazy_name: $($which_lazy)*<$ret_ty> = $($which_lazy)*::new($name);
    };
    {
        @lazy_impl
        $( #[doc = $d:literal] )*
        #[lazy_ty($($which_lazy:tt)*)]
        {$vis:vis $name:ident; $ret_ty:ty}
    } => {
        paste::paste! {
            $crate::make_lazy!(@lazy_impl $(#[doc = $d])* #[lazy_ty($($which_lazy)*)] #[lazy_name([<$name:upper>])] {$vis $name; $ret_ty});
        }
    };
    {
        @lazy_impl
        $( #[doc = $d:literal] )*
        $( #[lazy_name($lazy_name:ident)] )?
        {$($t:tt)*}
    } => {
        $crate::make_lazy!(@lazy_impl $(#[doc = $d])* #[lazy_ty($crate::GILLazyPy)] $( #[lazy_name($lazy_name)] )* {$($t)*});
    };
}
