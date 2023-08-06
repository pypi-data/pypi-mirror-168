use crate::{
    hashmaps::{AHashSet as HashSet, FxHashMap as HashMap},
    make_lazy,
};
use macro_rules_attribute::apply;
use once_cell::sync::Lazy;

use std::hash::Hash;

pub type EinInt = u8;

/// letters used in einsum and rearrange strings
/// i wanted this to be a constant, but that is annoying in rust bc can't do any computation to produce constants
/// so instead it's cached function
#[apply(make_lazy)]
#[lazy_ty(Lazy)]
pub fn alphabet() -> Vec<String> {
    let alphabet_upper: Vec<String> = (b'A'..=b'Z')
        .map(|x| std::str::from_utf8(&[x]).unwrap().to_owned())
        .collect();
    let alphabet_lower: Vec<String> = (b'a'..=b'z')
        .map(|x| std::str::from_utf8(&[x]).unwrap().to_owned())
        .collect();
    alphabet_lower
        .iter()
        .chain(alphabet_upper.iter())
        .cloned()
        .collect()
}

#[apply(make_lazy)]
#[lazy_ty(Lazy)]
pub fn alphabet_inv() -> HashMap<String, usize> {
    ALPHABET
        .iter()
        .cloned()
        .enumerate()
        .map(|(a, b)| (b, a))
        .collect()
}

pub fn is_unique<T: Eq + Hash>(col: &[T]) -> bool {
    let set: HashSet<&T> = col.iter().collect();
    col.len() == set.len()
}

pub fn unique_to_appearance<T: Eq + Hash + Clone>(vec: &Vec<T>) -> HashMap<T, Vec<usize>> {
    let mut map: HashMap<T, Vec<usize>> = HashMap::new();
    for (i, x) in vec.iter().enumerate() {
        map.entry(x.clone()).or_insert(vec![]).push(i);
    }
    map
}

pub fn filter_to_idx<T>(col: &Vec<T>, f: &dyn Fn(&T) -> bool) -> Vec<usize> {
    col.iter()
        .enumerate()
        .filter(|(_i, x)| f(x))
        .map(|(i, _x)| i)
        .collect()
}

pub fn filter_out_idx<T: Clone>(col: &[T], idxs: &HashSet<usize>) -> Vec<T> {
    col.iter()
        .enumerate()
        .filter(|(i, _x)| !idxs.contains(i))
        .map(|(_i, x)| x)
        .cloned()
        .collect()
}

pub fn intersection_all<T: Eq + Hash + Copy>(sets: &Vec<HashSet<T>>) -> HashSet<T> {
    if sets.is_empty() {
        return HashSet::new();
    }
    let (first, rest) = sets.split_first().unwrap();
    rest.iter().fold(first.clone(), |acc, new| {
        acc.intersection(new).copied().collect()
    })
}

pub fn inverse_permutation(perm: &Vec<usize>) -> Vec<usize> {
    let mut result = vec![0; perm.len()];
    for (i, x) in perm.iter().enumerate() {
        result[*x] = i;
    }
    result
}

/// element at k in vec is v, max
pub fn dict_to_list(dict: &HashMap<usize, usize>, max: Option<usize>) -> Vec<usize> {
    let max = max.unwrap_or(*dict.keys().max().unwrap_or(&0));
    let mut result = vec![0; max + 1];
    for (k, v) in dict.iter() {
        result[*k] = *v;
    }
    result
}

/// Convenience function for managing a hashmap of vecs
pub fn vec_map_insert<T: Eq + Hash>(map: &mut HashMap<T, Vec<T>>, k: T, v: T) {
    map.entry(k).or_insert_with(Vec::new).push(v);
}

// wow this is a badly written macro. I'd really expect something like this to already exist
#[macro_export]
macro_rules! filter_by_variant {
    ($iterator:expr, $enum_name:ident, $variant:ident, $return_type:ty) => {{
        let mut yes: Vec<$return_type> = vec![];
        let mut no = vec![];
        for x in $iterator {
            match &*x {
                $enum_name::$variant(inner) => yes.push(inner.clone()),
                _ => no.push(x),
            }
        }
        (yes, no)
    }};
}

#[macro_export]
macro_rules! unwrap {
    ($target: expr, $pat: path) => {{
        if let $pat(a) = $target {
            // #1
            a
        } else {
            panic!("mismatch variant when cast to {}", stringify!($pat)); // #2
        }
    }};
}

#[macro_export]
macro_rules! timed {
    ($x:expr) => {{
        let timed_macro_now = std::time::Instant::now();

        let result = $x;

        let elapsed = timed_macro_now.elapsed();
        println!("{} took {:.2?}", stringify!($x), elapsed);
        result
    }};
    ($x:expr,$min_to_print_milis:expr,$for_real:expr) => {{
        let timed_macro_now = std::time::Instant::now();

        let result = $x;

        let elapsed = timed_macro_now.elapsed();
        if $for_real && elapsed > std::time::Duration::new(0, $min_to_print_milis * 1_000_000) {
            println!("{} took {:.2?}", stringify!($x), elapsed);
        }
        result
    }};
}
#[macro_export]
macro_rules! timed_value {
    ($x:expr) => {{
        let timed_macro_now = std::time::Instant::now();

        let result = $x;

        let elapsed = timed_macro_now.elapsed();
        (result, elapsed)
    }};
}

pub trait AsOp<T> {
    fn into_op(self) -> Option<T>;
    fn as_op(&self) -> Option<&T>;
    fn as_mut_op(&mut self) -> Option<&mut T>;

    fn map_or_clone<'a, F, O, OF>(&'a self, f: F) -> O
    where
        Self: Into<O>,
        OF: Into<O>,
        T: 'a,
        Self: Clone,
        F: FnOnce(&'a T) -> OF,
    {
        self.and_then_or_clone(|x| Some(f(x)))
    }
    fn and_then_or_clone<'a, F, O, OF>(&'a self, f: F) -> O
    where
        Self: Into<O>,
        OF: Into<O>,
        T: 'a,
        Self: Clone,
        F: FnOnce(&'a T) -> Option<OF>,
    {
        self.as_op()
            .and_then(f)
            .map(Into::into)
            .unwrap_or_else(|| self.clone().into())
    }
}

impl<T> AsOp<T> for T {
    fn into_op(self) -> Option<T> {
        Some(self)
    }
    fn as_op(&self) -> Option<&T> {
        Some(self)
    }
    fn as_mut_op(&mut self) -> Option<&mut T> {
        Some(self)
    }
}

pub fn mapping_until_end<T: Eq + Hash + Clone>(x: &T, mapping: &HashMap<T, T>) -> T {
    let mut result = x.clone();
    for _ in 0..1000 {
        match mapping.get(&result) {
            None => {
                return result;
            }
            Some(next) => {
                result = next.clone();
            }
        }
    }
    panic!("mapping_until_end didnt finish");
}

pub fn apply_fn_until_same<T: Eq + Hash + Clone, F>(x: &T, f: F) -> T
where
    F: FnMut(&T) -> T,
{
    let mut f = f;
    let mut result = x.clone();
    for i in 0..1000 {
        let next = f(&result);
        if next == result {
            return result;
        }
        result = next;
        if i == 1000 - 1 {
            panic!("apply until same didnt finish");
        }
    }
    result
}

// might be fun to make memcpy based optimized outer product where we just copy blocks into place
pub fn outer_product<T: Clone>(cols: &Vec<Vec<T>>) -> Vec<Vec<T>> {
    assert!(!cols.iter().any(|x| x.is_empty()));
    if cols.is_empty() {
        return vec![vec![]];
    }

    let mut result: Vec<Vec<T>> = Vec::with_capacity(cols.iter().map(|x| x.len()).product());
    let mut places: Vec<usize> = vec![0; cols.len()];
    loop {
        result.push(
            places
                .iter()
                .enumerate()
                .map(|(i, place)| cols[i][*place].clone())
                .collect(),
        );

        let mut moving_place = cols.len() - 1;
        loop {
            places[moving_place] += 1;
            if places[moving_place] == cols[moving_place].len() {
                places[moving_place] = 0;
                if moving_place == 0 {
                    return result;
                }
                moving_place -= 1;
            } else {
                break;
            }
        }
    }
}

#[test]
pub fn test_outer_product() {
    let ex = vec![vec![0, 1], vec![2, 3, 4]];
    dbg!(outer_product(&ex));
}

// note this adds an element at the end so you can always look up arr[i+1] to get end
pub fn cumsum<T: std::ops::AddAssign + Default + Copy>(col: &[T]) -> Vec<T> {
    col.iter()
        .chain(std::iter::once(&Default::default()))
        .scan(Default::default(), |state: &mut T, el| {
            let old_state = *state;
            *state += *el;
            Some(old_state)
        })
        .collect()
}

pub fn hashmap_collect_except_duplicates<K: Eq + Hash + Clone, V: Eq + Hash + Clone>(
    it: impl Iterator<Item = (K, V)>,
) -> HashMap<K, V> {
    let mut result = HashMap::new();
    let mut dead: HashSet<K> = HashSet::new();
    for (k, v) in it {
        if !dead.contains(&k) {
            if let Some(old) = result.insert(k.clone(), v.clone()) {
                if old != v {
                    result.remove(&k);
                    dead.insert(k);
                }
            }
        }
    }
    result
}

pub type BitMask64 = usize;
pub type BitMask128 = u128;
