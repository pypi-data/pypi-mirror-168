use crate::hashmaps::FxHashMap as HashMap;

pub struct UnionFind(Vec<usize>);

impl UnionFind {
    pub fn new(size: usize) -> Self {
        UnionFind((0..size).collect())
    }

    pub fn find(&self, x: usize) -> usize {
        if self.0[x] == x {
            return x;
        }
        self.find(self.0[x])
    }

    pub fn union(&mut self, a: usize, b: usize) {
        let bf = self.find(b);
        if self.0[a] == a {
            self.0[bf] = a;
        } else {
            self.union(self.0[a], bf);
        }
    }

    pub fn to_vec_vec(&self) -> Vec<Vec<usize>> {
        let mut dict: HashMap<usize, Vec<usize>> = HashMap::new();
        for (i, x) in self.0.iter().enumerate() {
            dict.entry(self.find(*x)).or_insert(Vec::new()).push(i);
        }
        dict.values().cloned().collect()
    }
}
