// file copy pasted from crate ahash but with IntoPy implemented because we can't implement on their newtype
use crate::pyo3_prelude::*;
use rustc_hash::FxHasher;
use std::borrow::Borrow;
use std::collections::{hash_map, hash_set, HashMap, HashSet};
use std::fmt::{self, Debug};
use std::hash::{BuildHasher, BuildHasherDefault, Hash};
use std::iter::FromIterator;
use std::ops::{BitAnd, BitOr, BitXor, Deref, DerefMut, Index, Sub};
use std::panic::UnwindSafe;
// use rustc_hash::FxHashMap;
type RandomState = BuildHasherDefault<FxHasher>;

/// A [`HashMap`](std::collections::HashMap) using [`RandomState`](FxHasher) to hash the items.
/// (Requires the `std` feature to be enabled.)
#[derive(Clone)]
pub struct FxHashMap<K, V, S = RandomState>(HashMap<K, V, S>);

impl<K, V> From<HashMap<K, V, RandomState>> for FxHashMap<K, V> {
    fn from(item: HashMap<K, V, RandomState>) -> Self {
        FxHashMap(item)
    }
}

impl<K, V, const N: usize> From<[(K, V); N]> for FxHashMap<K, V>
where
    K: Eq + Hash,
{
    /// # Examples
    ///
    /// ```
    /// use rust_circuit::hashmaps::FxHashMap;
    ///
    /// let map1 = FxHashMap::from([(1, 2), (3, 4)]);
    /// let map2: FxHashMap<_, _> = [(1, 2), (3, 4)].into();
    /// assert_eq!(map1, map2);
    /// ```
    fn from(arr: [(K, V); N]) -> Self {
        Self::from_iter(arr)
    }
}

impl<K, V> Into<HashMap<K, V, RandomState>> for FxHashMap<K, V> {
    fn into(self) -> HashMap<K, V, RandomState> {
        self.0
    }
}

impl<K, V> FxHashMap<K, V, RandomState> {
    pub fn new() -> Self {
        FxHashMap(HashMap::with_hasher(RandomState::default()))
    }

    pub fn with_capacity(capacity: usize) -> Self {
        FxHashMap(HashMap::with_capacity_and_hasher(
            capacity,
            RandomState::default(),
        ))
    }
}

impl<K, V, S> FxHashMap<K, V, S>
where
    S: BuildHasher,
{
    pub fn with_hasher(hash_builder: S) -> Self {
        FxHashMap(HashMap::with_hasher(hash_builder))
    }

    pub fn with_capacity_and_hasher(capacity: usize, hash_builder: S) -> Self {
        FxHashMap(HashMap::with_capacity_and_hasher(capacity, hash_builder))
    }
}

impl<K, V, S> FxHashMap<K, V, S>
where
    K: Hash + Eq,
    S: BuildHasher,
{
    /// Returns a reference to the value corresponding to the key.
    ///
    /// The key may be any borrowed form of the map's key type, but
    /// [`Hash`] and [`Eq`] on the borrowed form *must* match those for
    /// the key type.
    ///
    /// # Examples
    ///
    /// ```
    /// use std::collections::HashMap;
    ///
    /// let mut map = HashMap::new();
    /// map.insert(1, "a");
    /// assert_eq!(map.get(&1), Some(&"a"));
    /// assert_eq!(map.get(&2), None);
    /// ```
    #[inline]
    pub fn get<Q: ?Sized>(&self, k: &Q) -> Option<&V>
    where
        K: Borrow<Q>,
        Q: Hash + Eq,
    {
        self.0.get(k)
    }

    /// Returns the key-value pair corresponding to the supplied key.
    ///
    /// The supplied key may be any borrowed form of the map's key type, but
    /// [`Hash`] and [`Eq`] on the borrowed form *must* match those for
    /// the key type.
    ///
    /// # Examples
    ///
    /// ```
    /// use std::collections::HashMap;
    ///
    /// let mut map = HashMap::new();
    /// map.insert(1, "a");
    /// assert_eq!(map.get_key_value(&1), Some((&1, &"a")));
    /// assert_eq!(map.get_key_value(&2), None);
    /// ```
    #[inline]
    pub fn get_key_value<Q: ?Sized>(&self, k: &Q) -> Option<(&K, &V)>
    where
        K: Borrow<Q>,
        Q: Hash + Eq,
    {
        self.0.get_key_value(k)
    }

    /// Returns a mutable reference to the value corresponding to the key.
    ///
    /// The key may be any borrowed form of the map's key type, but
    /// [`Hash`] and [`Eq`] on the borrowed form *must* match those for
    /// the key type.
    ///
    /// # Examples
    ///
    /// ```
    /// use std::collections::HashMap;
    ///
    /// let mut map = HashMap::new();
    /// map.insert(1, "a");
    /// if let Some(x) = map.get_mut(&1) {
    ///     *x = "b";
    /// }
    /// assert_eq!(map[&1], "b");
    /// ```
    #[inline]
    pub fn get_mut<Q: ?Sized>(&mut self, k: &Q) -> Option<&mut V>
    where
        K: Borrow<Q>,
        Q: Hash + Eq,
    {
        self.0.get_mut(k)
    }

    /// Inserts a key-value pair into the map.
    ///
    /// If the map did not have this key present, [`None`] is returned.
    ///
    /// If the map did have this key present, the value is updated, and the old
    /// value is returned. The key is not updated, though; this matters for
    /// types that can be `==` without being identical. See the [module-level
    /// documentation] for more.
    ///
    /// # Examples
    ///
    /// ```
    /// use std::collections::HashMap;
    ///
    /// let mut map = HashMap::new();
    /// assert_eq!(map.insert(37, "a"), None);
    /// assert_eq!(map.is_empty(), false);
    ///
    /// map.insert(37, "b");
    /// assert_eq!(map.insert(37, "c"), Some("b"));
    /// assert_eq!(map[&37], "c");
    /// ```
    #[inline]
    pub fn insert(&mut self, k: K, v: V) -> Option<V> {
        self.0.insert(k, v)
    }

    /// Removes a key from the map, returning the value at the key if the key
    /// was previously in the map.
    ///
    /// The key may be any borrowed form of the map's key type, but
    /// [`Hash`] and [`Eq`] on the borrowed form *must* match those for
    /// the key type.
    ///
    /// # Examples
    ///
    /// ```
    /// use std::collections::HashMap;
    ///
    /// let mut map = HashMap::new();
    /// map.insert(1, "a");
    /// assert_eq!(map.remove(&1), Some("a"));
    /// assert_eq!(map.remove(&1), None);
    /// ```
    #[inline]
    pub fn remove<Q: ?Sized>(&mut self, k: &Q) -> Option<V>
    where
        K: Borrow<Q>,
        Q: Hash + Eq,
    {
        self.0.remove(k)
    }
}

impl<K, V, S> Deref for FxHashMap<K, V, S> {
    type Target = HashMap<K, V, S>;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<K, V, S> DerefMut for FxHashMap<K, V, S> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl<K, V, S> UnwindSafe for FxHashMap<K, V, S>
where
    K: UnwindSafe,
    V: UnwindSafe,
{
}

impl<K, V, S> PartialEq for FxHashMap<K, V, S>
where
    K: Eq + Hash,
    V: PartialEq,
    S: BuildHasher,
{
    fn eq(&self, other: &FxHashMap<K, V, S>) -> bool {
        self.0.eq(&other.0)
    }
}

impl<K, V, S> Eq for FxHashMap<K, V, S>
where
    K: Eq + Hash,
    V: Eq,
    S: BuildHasher,
{
}

impl<K, Q: ?Sized, V, S> Index<&Q> for FxHashMap<K, V, S>
where
    K: Eq + Hash + Borrow<Q>,
    Q: Eq + Hash,
    S: BuildHasher,
{
    type Output = V;

    /// Returns a reference to the value corresponding to the supplied key.
    ///
    /// # Panics
    ///
    /// Panics if the key is not present in the `HashMap`.
    #[inline]
    fn index(&self, key: &Q) -> &V {
        self.0.index(key)
    }
}

impl<K, V, S> Debug for FxHashMap<K, V, S>
where
    K: Debug,
    V: Debug,
    S: BuildHasher,
{
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        self.0.fmt(fmt)
    }
}

impl<K, V, S> FromIterator<(K, V)> for FxHashMap<K, V, S>
where
    K: Eq + Hash,
    S: BuildHasher + Default,
{
    fn from_iter<T: IntoIterator<Item = (K, V)>>(iter: T) -> Self {
        FxHashMap(HashMap::from_iter(iter))
    }
}

impl<'a, K, V, S> IntoIterator for &'a FxHashMap<K, V, S> {
    type Item = (&'a K, &'a V);
    type IntoIter = hash_map::Iter<'a, K, V>;
    fn into_iter(self) -> Self::IntoIter {
        self.0.iter()
    }
}

impl<'a, K, V, S> IntoIterator for &'a mut FxHashMap<K, V, S> {
    type Item = (&'a K, &'a mut V);
    type IntoIter = hash_map::IterMut<'a, K, V>;
    fn into_iter(self) -> Self::IntoIter {
        self.0.iter_mut()
    }
}

impl<K, V, S> IntoIterator for FxHashMap<K, V, S> {
    type Item = (K, V);
    type IntoIter = hash_map::IntoIter<K, V>;
    fn into_iter(self) -> Self::IntoIter {
        self.0.into_iter()
    }
}

impl<K, V, S> Extend<(K, V)> for FxHashMap<K, V, S>
where
    K: Eq + Hash,
    S: BuildHasher,
{
    #[inline]
    fn extend<T: IntoIterator<Item = (K, V)>>(&mut self, iter: T) {
        self.0.extend(iter)
    }
}

impl<'a, K, V, S> Extend<(&'a K, &'a V)> for FxHashMap<K, V, S>
where
    K: Eq + Hash + Copy + 'a,
    V: Copy + 'a,
    S: BuildHasher,
{
    #[inline]
    fn extend<T: IntoIterator<Item = (&'a K, &'a V)>>(&mut self, iter: T) {
        self.0.extend(iter)
    }
}

impl<K, V> Default for FxHashMap<K, V, RandomState> {
    #[inline]
    fn default() -> FxHashMap<K, V, RandomState> {
        FxHashMap::new()
    }
}

impl<K: Eq + Hash, V> IntoPy<PyObject> for FxHashMap<K, V>
where
    HashMap<K, V>: pyo3::IntoPy<PyObject>,
{
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.0.into_iter().collect::<HashMap<K, V>>().into_py(py)
    }
}

impl<'source, K: Eq + Hash, V> FromPyObject<'source> for FxHashMap<K, V>
where
    HashMap<K, V>: pyo3::FromPyObject<'source>,
{
    fn extract(obj: &'source PyAny) -> PyResult<Self> {
        let default_version: HashMap<K, V> = obj.extract()?;
        Ok(Self(default_version.into_iter().collect()))
    }
}

#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn test_borrow() {
        let mut map: FxHashMap<String, String> = FxHashMap::new();
        map.insert("foo".to_string(), "Bar".to_string());
        map.insert("Bar".to_string(), map.get("foo").unwrap().to_owned());
    }
}

/// A [`HashSet`](std::collections::HashSet) using [`RandomState`](RandomState) to hash the items.
/// (Requires the `std` feature to be enabled.)
#[derive(Clone)]
pub struct AHashSet<T, S = RandomState>(HashSet<T, S>);

impl<T> From<HashSet<T, RandomState>> for AHashSet<T> {
    fn from(item: HashSet<T, RandomState>) -> Self {
        AHashSet(item)
    }
}

impl<T, const N: usize> From<[T; N]> for AHashSet<T>
where
    T: Eq + Hash,
{
    /// # Examples
    ///
    /// ```
    /// use rust_circuit::hashmaps::AHashSet;
    ///
    /// let set1 = AHashSet::from([1, 2, 3, 4]);
    /// let set2: AHashSet<_> = [1, 2, 3, 4].into();
    /// assert_eq!(set1, set2);
    /// ```
    fn from(arr: [T; N]) -> Self {
        Self::from_iter(arr)
    }
}

impl<T> Into<HashSet<T, RandomState>> for AHashSet<T> {
    fn into(self) -> HashSet<T, RandomState> {
        self.0
    }
}

impl<T> AHashSet<T, RandomState> {
    pub fn new() -> Self {
        AHashSet(HashSet::with_hasher(RandomState::default()))
    }

    pub fn with_capacity(capacity: usize) -> Self {
        AHashSet(HashSet::with_capacity_and_hasher(
            capacity,
            RandomState::default(),
        ))
    }
}

impl<T, S> AHashSet<T, S>
where
    S: BuildHasher,
{
    pub fn with_hasher(hash_builder: S) -> Self {
        AHashSet(HashSet::with_hasher(hash_builder))
    }

    pub fn with_capacity_and_hasher(capacity: usize, hash_builder: S) -> Self {
        AHashSet(HashSet::with_capacity_and_hasher(capacity, hash_builder))
    }
}

impl<T, S> Deref for AHashSet<T, S> {
    type Target = HashSet<T, S>;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<T, S> DerefMut for AHashSet<T, S> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl<T, S> PartialEq for AHashSet<T, S>
where
    T: Eq + Hash,
    S: BuildHasher,
{
    fn eq(&self, other: &AHashSet<T, S>) -> bool {
        self.0.eq(&other.0)
    }
}

impl<T, S> Eq for AHashSet<T, S>
where
    T: Eq + Hash,
    S: BuildHasher,
{
}

impl<T, S> BitOr<&AHashSet<T, S>> for &AHashSet<T, S>
where
    T: Eq + Hash + Clone,
    S: BuildHasher + Default,
{
    type Output = AHashSet<T, S>;

    /// Returns the union of `self` and `rhs` as a new `AHashSet<T, S>`.
    ///
    /// # Examples
    ///
    /// ```
    /// use rust_circuit::hashmaps::AHashSet;
    ///
    /// let a: AHashSet<_> = vec![1, 2, 3].into_iter().collect();
    /// let b: AHashSet<_> = vec![3, 4, 5].into_iter().collect();
    ///
    /// let set = &a | &b;
    ///
    /// let mut i = 0;
    /// let expected = [1, 2, 3, 4, 5];
    /// for x in &set {
    ///     assert!(expected.contains(x));
    ///     i += 1;
    /// }
    /// assert_eq!(i, expected.len());
    /// ```
    fn bitor(self, rhs: &AHashSet<T, S>) -> AHashSet<T, S> {
        AHashSet(self.0.bitor(&rhs.0))
    }
}

impl<T, S> BitAnd<&AHashSet<T, S>> for &AHashSet<T, S>
where
    T: Eq + Hash + Clone,
    S: BuildHasher + Default,
{
    type Output = AHashSet<T, S>;

    /// Returns the intersection of `self` and `rhs` as a new `AHashSet<T, S>`.
    ///
    /// # Examples
    ///
    /// ```
    /// use rust_circuit::hashmaps::AHashSet;
    ///
    /// let a: AHashSet<_> = vec![1, 2, 3].into_iter().collect();
    /// let b: AHashSet<_> = vec![2, 3, 4].into_iter().collect();
    ///
    /// let set = &a & &b;
    ///
    /// let mut i = 0;
    /// let expected = [2, 3];
    /// for x in &set {
    ///     assert!(expected.contains(x));
    ///     i += 1;
    /// }
    /// assert_eq!(i, expected.len());
    /// ```
    fn bitand(self, rhs: &AHashSet<T, S>) -> AHashSet<T, S> {
        AHashSet(self.0.bitand(&rhs.0))
    }
}

impl<T, S> BitXor<&AHashSet<T, S>> for &AHashSet<T, S>
where
    T: Eq + Hash + Clone,
    S: BuildHasher + Default,
{
    type Output = AHashSet<T, S>;

    /// Returns the symmetric difference of `self` and `rhs` as a new `AHashSet<T, S>`.
    ///
    /// # Examples
    ///
    /// ```
    /// use rust_circuit::hashmaps::AHashSet;
    ///
    /// let a: AHashSet<_> = vec![1, 2, 3].into_iter().collect();
    /// let b: AHashSet<_> = vec![3, 4, 5].into_iter().collect();
    ///
    /// let set = &a ^ &b;
    ///
    /// let mut i = 0;
    /// let expected = [1, 2, 4, 5];
    /// for x in &set {
    ///     assert!(expected.contains(x));
    ///     i += 1;
    /// }
    /// assert_eq!(i, expected.len());
    /// ```
    fn bitxor(self, rhs: &AHashSet<T, S>) -> AHashSet<T, S> {
        AHashSet(self.0.bitxor(&rhs.0))
    }
}

impl<T, S> Sub<&AHashSet<T, S>> for &AHashSet<T, S>
where
    T: Eq + Hash + Clone,
    S: BuildHasher + Default,
{
    type Output = AHashSet<T, S>;

    /// Returns the difference of `self` and `rhs` as a new `AHashSet<T, S>`.
    ///
    /// # Examples
    ///
    /// ```
    /// use rust_circuit::hashmaps::AHashSet;
    ///
    /// let a: AHashSet<_> = vec![1, 2, 3].into_iter().collect();
    /// let b: AHashSet<_> = vec![3, 4, 5].into_iter().collect();
    ///
    /// let set = &a - &b;
    ///
    /// let mut i = 0;
    /// let expected = [1, 2];
    /// for x in &set {
    ///     assert!(expected.contains(x));
    ///     i += 1;
    /// }
    /// assert_eq!(i, expected.len());
    /// ```
    fn sub(self, rhs: &AHashSet<T, S>) -> AHashSet<T, S> {
        AHashSet(self.0.sub(&rhs.0))
    }
}

impl<T, S> Debug for AHashSet<T, S>
where
    T: Debug,
    S: BuildHasher,
{
    fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(fmt)
    }
}

impl<T, S> FromIterator<T> for AHashSet<T, S>
where
    T: Eq + Hash,
    S: BuildHasher + Default,
{
    #[inline]
    fn from_iter<I: IntoIterator<Item = T>>(iter: I) -> AHashSet<T, S> {
        AHashSet(HashSet::from_iter(iter))
    }
}

impl<'a, T, S> IntoIterator for &'a AHashSet<T, S> {
    type Item = &'a T;
    type IntoIter = hash_set::Iter<'a, T>;
    fn into_iter(self) -> Self::IntoIter {
        self.0.iter()
    }
}

impl<T, S> IntoIterator for AHashSet<T, S> {
    type Item = T;
    type IntoIter = hash_set::IntoIter<T>;
    fn into_iter(self) -> Self::IntoIter {
        self.0.into_iter()
    }
}

impl<T, S> Extend<T> for AHashSet<T, S>
where
    T: Eq + Hash,
    S: BuildHasher,
{
    #[inline]
    fn extend<I: IntoIterator<Item = T>>(&mut self, iter: I) {
        self.0.extend(iter)
    }
}

impl<'a, T, S> Extend<&'a T> for AHashSet<T, S>
where
    T: 'a + Eq + Hash + Copy,
    S: BuildHasher,
{
    #[inline]
    fn extend<I: IntoIterator<Item = &'a T>>(&mut self, iter: I) {
        self.0.extend(iter)
    }
}

impl<T> Default for AHashSet<T, RandomState> {
    /// Creates an empty `AHashSet<T, S>` with the `Default` value for the hasher.
    #[inline]
    fn default() -> AHashSet<T, RandomState> {
        AHashSet(HashSet::default())
    }
}
impl<V: Eq + Hash> IntoPy<PyObject> for AHashSet<V>
where
    HashSet<V>: pyo3::IntoPy<PyObject>,
{
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.0.into_iter().collect::<HashSet<V>>().into_py(py)
    }
}

impl<'source, V: Eq + Hash> FromPyObject<'source> for AHashSet<V>
where
    HashSet<V>: pyo3::FromPyObject<'source>,
{
    fn extract(obj: &'source PyAny) -> PyResult<Self> {
        let default_version: HashSet<V> = obj.extract()?;
        Ok(Self(default_version.into_iter().collect()))
    }
}
