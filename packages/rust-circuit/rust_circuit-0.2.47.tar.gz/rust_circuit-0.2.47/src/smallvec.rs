use crate::pyo3_prelude::*;
use smallvec::{Array, SmallVec};
use std::{
    fmt::Debug,
    hash::{Hash, Hasher},
    ops::{Deref, DerefMut},
    slice::{self, SliceIndex},
};

/// defining newtype of SmallVec so it can be converted to and from python
pub struct Sv<A: Array>(pub SmallVec<A>);

impl<A: Array> Hash for Sv<A>
where
    A::Item: Hash,
{
    fn hash<H: Hasher>(&self, state: &mut H) {
        (***self).hash(state)
    }
}

impl<A: Array> Debug for Sv<A>
where
    A::Item: Debug,
{
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.0.fmt(f)
    }
}

impl<A: Array> Default for Sv<A> {
    #[inline]
    fn default() -> Sv<A> {
        Sv(SmallVec::new())
    }
}

impl<A: Array, B: Array> PartialEq<Sv<B>> for Sv<A>
where
    A::Item: PartialEq<B::Item>,
{
    #[inline]
    fn eq(&self, other: &Sv<B>) -> bool {
        self.0[..] == other.0[..]
    }
}

impl<A: Array> Eq for Sv<A> where A::Item: Eq {}

impl<A: Array> Clone for Sv<A>
where
    A::Item: Clone,
{
    #[inline]
    fn clone(&self) -> Sv<A> {
        Sv(SmallVec::from(self.as_slice()))
    }

    fn clone_from(&mut self, source: &Self) {
        self.0.clone_from(&source.0);
    }
}

impl<A: Array> IntoPy<PyObject> for Sv<A>
where
    Vec<<A as smallvec::Array>::Item>: pyo3::IntoPy<PyObject>,
{
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.0.into_iter().collect::<Vec<_>>().into_py(py)
    }
}

impl<'source, A: Array> FromPyObject<'source> for Sv<A>
where
    Vec<<A as smallvec::Array>::Item>: pyo3::FromPyObject<'source>,
{
    fn extract(obj: &'source PyAny) -> PyResult<Self> {
        let vec_version: Vec<A::Item> = obj.extract()?;
        Ok(Self(vec_version.into()))
    }
}
impl<A: Array> FromIterator<A::Item> for Sv<A> {
    #[inline]
    fn from_iter<I: IntoIterator<Item = A::Item>>(iterable: I) -> Sv<A> {
        let mut v = Sv(SmallVec::new());
        v.0.extend(iterable);
        v
    }
}

impl<A: Array> Deref for Sv<A> {
    type Target = SmallVec<A>;

    #[inline]
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<A: Array> DerefMut for Sv<A> {
    #[inline]
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl<A: Array> From<SmallVec<A>> for Sv<A> {
    fn from(x: SmallVec<A>) -> Self {
        Self(x)
    }
}

#[macro_export]
macro_rules! sv {
    [$($tt:tt)*] => {
        $crate::smallvec::Sv(smallvec::smallvec!($($tt)*))
    };
}

type SVIntoIter<A> = <SmallVec<A> as IntoIterator>::IntoIter;

impl<A: Array> IntoIterator for Sv<A> {
    type Item = A::Item;
    type IntoIter = SVIntoIter<A>;
    fn into_iter(self) -> SVIntoIter<A> {
        self.0.into_iter()
    }
}

impl<A: Array, I: SliceIndex<[A::Item]>> std::ops::Index<I> for Sv<A> {
    type Output = I::Output;

    fn index(&self, index: I) -> &I::Output {
        &(*self.0)[index]
    }
}

impl<A: Array, I: SliceIndex<[A::Item]>> std::ops::IndexMut<I> for Sv<A> {
    fn index_mut(&mut self, index: I) -> &mut Self::Output {
        &mut (*self.0)[index]
    }
}

impl<'a, A: Array> IntoIterator for &'a Sv<A> {
    type IntoIter = slice::Iter<'a, A::Item>;
    type Item = &'a A::Item;
    fn into_iter(self) -> Self::IntoIter {
        self.iter()
    }
}

impl<'a, A: Array> IntoIterator for &'a mut Sv<A> {
    type IntoIter = slice::IterMut<'a, A::Item>;
    type Item = &'a mut A::Item;
    fn into_iter(self) -> Self::IntoIter {
        self.iter_mut()
    }
}
