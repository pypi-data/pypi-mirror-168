extern crate proc_macro;

use proc_macro::TokenStream;

/// consumes pyo3
/// TODO: maybe this should implement into py and from py
/// (easy, see https://github.com/imbolc/rust-derive-macro-guide)
#[proc_macro_derive(FakePyClassDeriv, attributes(pyo3))]
pub fn fake_py_class_deriv(_: TokenStream) -> TokenStream {
    TokenStream::new()
}

#[proc_macro_derive(NoopPyClassDeriv)]
pub fn noop_py_class_deriv(_: TokenStream) -> TokenStream {
    TokenStream::new()
}

#[proc_macro_attribute]
pub fn noop(_: proc_macro::TokenStream, body: proc_macro::TokenStream) -> proc_macro::TokenStream {
    body
}
