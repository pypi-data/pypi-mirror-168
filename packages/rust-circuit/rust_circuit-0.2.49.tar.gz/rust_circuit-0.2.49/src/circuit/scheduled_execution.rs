use crate::{
    hashmaps::{AHashSet as HashSet, FxHashMap as HashMap},
    py_types::{scalar_to_tensor, tensor_scale, un_flat_concat},
};
use std::fmt::{self, Display};

use crate::{
    cached_lambda,
    py_types::{ExtraPySelfOps, Tensor},
    pycall,
    tensor_util::{Shape, TorchDeviceDtype},
    timed,
};

use super::{
    circuit_optimizer::OptimizationSettings,
    circuit_utils::{hash_to_node, toposort_circuit},
    get_compatible_dtype,
    prelude::*,
    print::oom_fmt,
    scheduling_z3::schedule_dag_strategy_ints,
    visit_circuit, ArrayConstant, HashBytes, PyHashBytes, ScalarConstant,
};
use crate::pyo3_prelude::*;
use crate::util::filter_to_idx;
use itertools::Itertools;
use macro_rules_attribute::apply;
use num_bigint::BigUint;
use pyo3::{create_exception, exceptions::PyException};
use thiserror::Error;

#[derive(Clone, Debug)]
pub enum Instruction {
    Drop(HashBytes),
    Compute(CircuitRc),
}

impl IntoPy<PyObject> for Instruction {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            Instruction::Drop(hb) => PyHashBytes(hb).into_py(py),
            Instruction::Compute(c) => c.into_py(py),
        }
    }
}

#[pyclass(unsendable)]
#[derive(Clone, Debug, PyClassDeriv)]
pub struct Schedule {
    #[pyo3(get)]
    pub instructions: Vec<Instruction>,
    pub constants: HashMap<HashBytes, Tensor>,
    // keep scalar constants seperate so adjust numerical scale can work without losing precision
    // before when these were in tensors, they had to be right dtype and therefore overflowed when
    // adjustment needed
    pub scalar_constants: HashMap<HashBytes, ScalarConstant>,
    #[pyo3(get)]
    pub device_dtype: TorchDeviceDtype,
    pub output_circuit: Option<CircuitRc>,
    pub split_shapes: Option<Vec<Shape>>,
}
#[pymethods]
impl Schedule {
    pub fn replace_tensors(&self, map: HashMap<HashBytes, Tensor>) -> PyResult<Self> {
        let mut result = self.clone();
        for (k, v) in map {
            if !result.constants.contains_key(&k) {
                return Err(PyErr::new::<pyo3::exceptions::PyKeyError, _>(
                    "key circuit wasn't present in original",
                ));
            }
            result.constants.insert(k, v);
        }
        Ok(result)
    }

    #[pyo3(name = "map_tensors")]
    pub fn map_tensors_py(&self, f: PyObject) -> PyResult<Self> {
        let mut result = self.clone();
        result.constants = result
            .constants
            .into_iter()
            .map(|(hash, tensor)| (hash, pycall!(f, (PyHashBytes(hash), tensor))))
            .collect();
        Ok(result)
    }

    #[getter]
    #[pyo3(name = "constants")]
    pub fn constants_py(&self) -> HashMap<PyHashBytes, Tensor> {
        self.constants
            .iter()
            .map(|(k, v)| (PyHashBytes(*k), v.clone()))
            .collect()
    }

    pub fn evaluate(&self, settings: OptimizationSettings) -> Tensor {
        let eval = || {
            if settings.adjust_numerical_scale {
                evaluate_schedule_adjust_numerical_scale(self, settings)
                    [&self.output_circuit.as_ref().unwrap().info().hash]
                    .clone()
            } else {
                evaluate_schedule(self)[&self.output_circuit.as_ref().unwrap().info().hash].clone()
            }
        };
        timed!(eval(), 10, settings.verbose >= 1)
    }

    pub fn evaluate_many(&self, settings: OptimizationSettings) -> Vec<Tensor> {
        let single = self.evaluate(settings);
        self.split(single)
    }

    pub fn split(&self, tensor: Tensor) -> Vec<Tensor> {
        un_flat_concat(&tensor, self.split_shapes.clone().unwrap()).unwrap()
    }

    pub fn get_stats(&self) -> ScheduleStats {
        let mut mem: BigUint = BigUint::from(0usize);
        let mut max_mem: BigUint = BigUint::from(0usize);
        let mut biggest: HashMap<HashBytes, CircuitRc> = HashMap::new();
        let mut current: HashMap<HashBytes, CircuitRc> = HashMap::new();
        for instruction in self.instructions.clone() {
            match instruction {
                Instruction::Drop(drop) => {
                    let dropped = current.remove(&drop).unwrap();
                    mem -= dropped.info().numel();
                }
                Instruction::Compute(c) => {
                    current.insert(c.info().hash, c.clone());
                    mem += c.info().numel();
                    if mem > max_mem {
                        max_mem = mem.clone();
                        biggest = current.clone();
                    }
                }
            }
        }
        ScheduleStats {
            max_mem,
            constant_mem: self
                .constants
                .iter()
                .map(|(_h, t)| t.shape().iter().product::<usize>())
                .sum(),
            max_circuit_set: biggest.values().cloned().collect(),
        }
    }
}

#[pyclass(unsendable)]
#[derive(Clone, Debug, PyClassDeriv)]
pub struct ScheduleStats {
    #[pyo3(get)]
    max_mem: BigUint,
    #[pyo3(get)]
    constant_mem: BigUint, // this has already been allocated so it can't be over 2^64
    // #[pyo3(get)]
    max_circuit_set: HashSet<CircuitRc>,
}

#[derive(Error, Debug)]
pub enum SchedulingError {
    #[error("{string}")]
    CannotFitInMemory {
        max_memory: usize,
        memory_chunks: usize,
        node_memories: Vec<usize>,
        string: String,
    },
}

create_exception!(
    rust_circuit,
    PyOOMError,
    PyException,
    "OOM error from compiler"
);

impl From<SchedulingError> for PyErr {
    fn from(err: SchedulingError) -> Self {
        PyErr::new::<PyOOMError, _>(format!("error (TODO: better) {}", err))
    }
}

impl Display for ScheduleStats {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut shapes = self
            .max_circuit_set
            .iter()
            .map(|x| x.info().shape.clone())
            .collect::<Vec<Shape>>();
        shapes.sort_by_key(|x| std::cmp::Reverse(x.iter().product::<usize>()));
        let shapes_and_percents: String = shapes
            .iter()
            .map(|x| {
                format!(
                    "{:?} {}%",
                    x,
                    // biguint doesn't have cast f64? that would be less lossy than truncate
                    (x.iter().product::<usize>() as f64 / self.max_mem.to_u64_digits()[0] as f64
                        * 100.0) as i64
                )
            })
            .collect::<Vec<String>>()
            .join(", ");
        let result = format!(
            "ScheduleStats: max: {} const: {} shapes: {}",
            oom_fmt(self.max_mem.clone()),
            oom_fmt(self.constant_mem.clone()),
            shapes_and_percents
        );
        write!(f, "{}", result)
    }
}

pub fn evaluate_schedule(schedule: &Schedule) -> HashMap<HashBytes, Tensor> {
    let mut live: HashMap<HashBytes, Tensor> = schedule.constants.clone();
    live.extend(
        schedule
            .scalar_constants
            .iter()
            .map(|x| (*x.0, x.1.eval_tensors(&[], &schedule.device_dtype).unwrap())),
    );
    for s in &schedule.instructions {
        match s {
            Instruction::Compute(circ) => {
                circ.children().for_each(|x: CircuitRc| {
                    if !live.contains_key(&x.info().hash) {
                        println!("FAIL");
                        dbg!(schedule
                            .instructions
                            .iter()
                            .filter_map(|ins| {
                                match ins {
                                    Instruction::Drop(d) => {
                                        if *d == x.info().hash {
                                            Some(ins)
                                        } else {
                                            None
                                        }
                                    }
                                    Instruction::Compute(c) => {
                                        if c == &x {
                                            Some(ins)
                                        } else {
                                            None
                                        }
                                    }
                                }
                            })
                            .collect::<Vec<&Instruction>>());
                        circ.compiler_print();
                        x.compiler_print();
                        panic!();
                    }
                });
                let tensors: Vec<Tensor> = circ
                    .children()
                    .map(|x| live[&x.info().hash].clone())
                    .collect();
                let result_err = circ.eval_tensors(&tensors, &schedule.device_dtype);
                if result_err.is_err() {
                    println!("errored evaluate");
                    circ.compiler_print()
                }
                let result = result_err.unwrap();
                assert!(result.shape()[..] == circ.info().shape[..]);
                live.insert(circ.info().hash, result);
            }
            Instruction::Drop(hash) => {
                live.remove(hash);
            }
        }
    }
    live
}

pub fn evaluate_schedule_adjust_numerical_scale(
    schedule: &Schedule,
    settings: OptimizationSettings,
) -> HashMap<HashBytes, Tensor> {
    // we store (tensor, scale) where scale is a number the tensor's been multiplied by
    // so (tensor(1e10),1.0) evaluates to same as (tensor(1),1e-10)
    let mul = |tup: &(Tensor, f64), m: f64| -> (Tensor, f64) {
        Python::with_gil(|py| (tup.0.clone().py_mul(py, m).unwrap(), tup.1 * m))
    };
    let set_scale = |tup: &(Tensor, f64), new_scale: f64| -> (Tensor, f64) {
        Python::with_gil(|py| {
            (
                tup.0.clone().py_mul(py, new_scale / tup.1).unwrap(),
                new_scale,
            )
        })
    };
    let clamp = |tup: &(Tensor, f64)| -> (Tensor, f64) {
        let scale = tensor_scale(&tup.0).unwrap();
        if scale > settings.numerical_scale_max || scale < settings.numerical_scale_min {
            mul(tup, 1.0 / scale)
        } else {
            tup.clone()
        }
    };
    let uniformize = |tups: &Vec<(Tensor, f64)>| -> Vec<(Tensor, f64)> {
        if tups.is_empty() || tups.iter().all(|x| x.1 == tups[0].1) {
            tups.clone()
        } else {
            let new_scale: f64 = tups
                .iter()
                .map(|x| x.1)
                .reduce(|a, b| if a > b { a } else { b })
                .unwrap();
            tups.iter().map(|x| set_scale(x, new_scale)).collect()
        }
    };

    let mut live: HashMap<HashBytes, (Tensor, f64)> = schedule
        .constants
        .iter()
        .map(|x| (*x.0, clamp(&(x.1.clone(), 1.0))))
        .collect();
    live.extend(schedule.scalar_constants.iter().map(|(h, s)| {
        (*h, {
            let value_scale = s.value.abs();
            if value_scale > settings.numerical_scale_max
                || value_scale < settings.numerical_scale_min && value_scale != 0.0
            {
                (
                    scalar_to_tensor(
                        s.value.signum(),
                        s.info().shape.clone(),
                        schedule.device_dtype.clone(),
                    )
                    .unwrap(),
                    1.0 / value_scale,
                )
            } else {
                (
                    scalar_to_tensor(
                        s.value,
                        s.info().shape.clone(),
                        schedule.device_dtype.clone(),
                    )
                    .unwrap(),
                    1.0,
                )
            }
        })
    }));
    for s in &schedule.instructions {
        match s {
            Instruction::Compute(circ) => {
                circ.children().for_each(|x: CircuitRc| {
                    if !live.contains_key(&x.info().hash) {
                        println!("FAIL");
                        dbg!(schedule
                            .instructions
                            .iter()
                            .filter_map(|ins| {
                                match ins {
                                    Instruction::Drop(d) => {
                                        if *d == x.info().hash {
                                            Some(ins)
                                        } else {
                                            None
                                        }
                                    }
                                    Instruction::Compute(c) => {
                                        if c == &x {
                                            Some(ins)
                                        } else {
                                            None
                                        }
                                    }
                                }
                            })
                            .collect::<Vec<&Instruction>>());
                        circ.compiler_print();
                        x.compiler_print();
                        panic!();
                    }
                });
                let tensors_and_scales: Vec<(Tensor, f64)> = circ
                    .children()
                    .map(|x| live[&x.info().hash].clone())
                    .collect();
                let tensors: Vec<Tensor> = tensors_and_scales.iter().map(|x| x.0.clone()).collect();
                let result = match &***circ {
                    Circuit::Einsum(_) => {
                        let new_scale = tensors_and_scales.iter().map(|x| x.1).product();
                        clamp(&(
                            circ.eval_tensors(&tensors, &schedule.device_dtype).unwrap(),
                            new_scale,
                        ))
                    }
                    Circuit::Add(_) | Circuit::Concat(_) => {
                        let new_ts = uniformize(&tensors_and_scales);
                        (
                            circ.eval_tensors(
                                &new_ts.iter().map(|x| x.0.clone()).collect::<Vec<_>>(),
                                &schedule.device_dtype,
                            )
                            .unwrap(),
                            new_ts[0].1,
                        )
                    }
                    Circuit::GeneralFunction(_) => {
                        let new_ts: Vec<(Tensor, f64)> = tensors_and_scales
                            .iter()
                            .map(|x| set_scale(x, 1.0))
                            .collect();
                        clamp(&(
                            circ.eval_tensors(
                                &new_ts.iter().map(|x| x.0.clone()).collect::<Vec<_>>(),
                                &schedule.device_dtype,
                            )
                            .unwrap(),
                            1.0,
                        ))
                    }
                    Circuit::Index(_) | Circuit::Rearrange(_) | Circuit::Scatter(_) => (
                        circ.eval_tensors(
                            &tensors_and_scales
                                .iter()
                                .map(|x| x.0.clone())
                                .collect::<Vec<_>>(),
                            &schedule.device_dtype,
                        )
                        .unwrap(),
                        tensors_and_scales[0].1,
                    ),
                    Circuit::ScalarConstant(_) | Circuit::ArrayConstant(_) | Circuit::Symbol(_) => {
                        panic!("constant found as schedule instruction, not supposed to happen")
                    }
                };
                assert!(result.0.shape()[..] == circ.info().shape[..]);
                live.insert(circ.info().hash, result);
            }
            Instruction::Drop(hash) => {
                live.remove(hash);
            }
        }
    }
    live.iter()
        .map(|(k, v)| (*k, set_scale(v, 1.0).0))
        .collect()
}

/// this supports dropping and recomputing. if you have an Evaluate(CircuitRc) of something you already evaluated
/// it's assumed you dropped this and are recomputing it
pub fn order_to_schedule(
    order: &Vec<CircuitRc>,
    constants: &Vec<ArrayConstant>,
    scalar_constants: &Vec<ScalarConstant>,
    to_keep: HashSet<HashBytes>,
    device_dtype: TorchDeviceDtype,
) -> Schedule {
    let mut result: Schedule = Schedule {
        instructions: vec![],
        constants: constants
            .iter()
            .map(|x| (x.info().hash, x.value.clone()))
            .collect(),
        scalar_constants: scalar_constants
            .iter()
            .map(|x| (x.info().hash, x.clone()))
            .collect(),
        device_dtype,
        split_shapes: None,
        output_circuit: None,
    };

    let mut seen_dependencies: HashSet<HashBytes> = HashSet::new();
    for ex in order.iter().rev() {
        for child in ex.children() {
            let dep = child.info().hash;
            if !matches!(
                &**child,
                Circuit::ArrayConstant(_) | Circuit::ScalarConstant(_)
            ) && seen_dependencies.insert(dep)
                && !to_keep.contains(&dep)
            {
                result.instructions.push(Instruction::Drop(dep));
            }
        }
        result.instructions.push(Instruction::Compute(ex.clone()));
        // seen_dependencies.remove(&ex.info().hash);
    }
    result.instructions.reverse();
    result
}

#[pyclass]
#[derive(Default, Clone, Debug)]
pub struct Dag {
    pub children: Vec<Vec<usize>>,
    pub parents: Vec<Vec<usize>>,
    /// the cost is the number of new elements computing the node entails allocating.
    /// some nodes compute views into existing memory, such as some indexes and all ArrayConstants
    /// (as they're already allocated), so they have cost 0
    /// if a node computes a new tensor, the cost is the product of the shape.
    pub node_costs: Vec<usize>,
    pub node_hashes: Vec<HashBytes>,
    pub hash_to_node: HashMap<HashBytes, usize>,
}
impl Dag {
    pub fn get_outputs(&self) -> Vec<usize> {
        filter_to_idx(&self.parents.iter().collect(), &mut |y| y.is_empty())
    }
    /// Create a new dag with a subset of the nodes. Edges to ignored
    /// nodes are replaced with edges that pass through to nodes we're keeping
    pub fn sub_dag(&self, nodes_to_keep: &Vec<usize>) -> Dag {
        // map indices from nodes_to_keep -> arange
        let old_to_new: HashMap<usize, usize> = nodes_to_keep
            .iter()
            .enumerate()
            .map(|x| (*x.1, x.0))
            .collect();
        // fill out everything except the parents and children
        // assumes the costs stay the same
        let mut result = Dag {
            node_hashes: nodes_to_keep.iter().map(|x| self.node_hashes[*x]).collect(),
            hash_to_node: nodes_to_keep
                .iter()
                .enumerate()
                .map(|(i, x)| (self.node_hashes[*x], i))
                .collect(),
            node_costs: nodes_to_keep.iter().map(|x| self.node_costs[*x]).collect(),
            children: vec![vec![]; nodes_to_keep.len()],
            parents: vec![vec![]; nodes_to_keep.len()],
        };
        // new children = (old children we're keeping) + (new children of old children we're not keeping)
        #[apply(cached_lambda)]
        fn new_children(old_i: usize) -> Vec<usize> {
            let old_children = &self.children[old_i];
            old_children
                .iter()
                .flat_map(|old_child| {
                    if let Some(n) = old_to_new.get(old_child) {
                        vec![*n]
                    } else {
                        new_children(*old_child)
                    }
                })
                .collect()
        }
        // fill out parents and children
        for (new_i, old_i) in nodes_to_keep.iter().enumerate() {
            let children = new_children(*old_i);
            result.children[new_i] = children.clone();
            for child in children {
                result.parents[child].push(new_i);
            }
        }
        result
    }

    /// Find all of the nontrivial chains within the dag which are internally not connected
    /// to other nodes, and return the top / parent indices
    /// This corresponds to all the size >=2 subcircuits in a circuit which involve serial computation
    /// (Technically these are the nontrivial maximal chain induced subgraphs)
    pub fn chains(&self) -> Vec<usize> {
        #[apply(cached_lambda)]
        fn top_of_chain(node: usize) -> usize {
            if self.parents[node].len() == 1 && self.children[self.parents[node][0]].len() == 1 {
                top_of_chain(self.parents[node][0])
            } else {
                node
            }
        }
        let node_to_top: Vec<usize> = (0..self.node_costs.len()).map(top_of_chain).collect();
        node_to_top
            .into_iter()
            .enumerate()
            // filter out length 1 chains
            .filter_map(|(node, top)| if node == top { None } else { Some(top) })
            // return each parent of a nontrivial chain once
            .unique()
            .collect()
    }
}

pub fn circuits_to_dag(circuits: &[&Circuit]) -> Dag {
    let mut result: Dag = Default::default();
    // append the circuit to the dag if it's not already there, and return its index
    let number_node = |c: &Circuit, result: &mut Dag| -> usize {
        if let Some(idx) = result.hash_to_node.get(&c.info().hash) {
            return *idx;
        }
        result.node_costs.push(c.intermediate_cost_bound());
        result.node_hashes.push(c.info().hash);
        result
            .hash_to_node
            .insert(c.info().hash, result.node_hashes.len() - 1);
        result.children.push(vec![]);
        result.parents.push(vec![]);
        result.node_hashes.len() - 1
    };
    for circuit in circuits {
        visit_circuit(circuit, &mut |c: &Circuit| {
            // ArrayConstants are never added to the dag to begin with because they're always 0 cost
            if !matches!(c, Circuit::ArrayConstant(_) | Circuit::ScalarConstant(_)) {
                let my_number = number_node(c, &mut result);
                let children_to_consider: Vec<CircuitRc> = c
                    .children()
                    .filter(|child| {
                        !matches!(
                            &***child,
                            Circuit::ArrayConstant(_) | Circuit::ScalarConstant(_)
                        )
                    })
                    .collect();
                result.children[my_number] = children_to_consider
                    .iter()
                    .map(|child| number_node(child, &mut result))
                    .collect();
                for child in children_to_consider {
                    let new_num = number_node(&child, &mut result);
                    result.parents[new_num].push(my_number);
                }
            }
        });
    }
    result
}

fn simplify_dag_for_scheduling_and_kept_nodes(dag: &Dag, chunk_size: usize) -> (Dag, Vec<usize>) {
    // filter out nodes that are too small to be worth scheduling (such as cost 0 indexes)
    let nodes_to_keep: Vec<usize> = (0..dag.node_costs.len())
        .filter(|i| dag.node_costs[*i] >= chunk_size)
        .collect();
    let dag = dag.sub_dag(&nodes_to_keep);
    // now we filter out some parts in chains of serial computation
    // if we have a chain of nodes `start -> node_1 -> ... -> end`,
    // we can simplify the dag to only include the node with the smallest cost,
    // and the highest cost nodes on either side.
    // we need the smallest cost node as after computing this is the best time to compute
    // other nodes from other places in parallel
    // and we need the maximum nodes on either side so the scheduler has the right bound
    // on intermediate memory consumption along the serial chain
    let chain_ends = dag.chains();
    let mut nodes_to_prune: HashSet<usize> = HashSet::new();
    for chain_end in chain_ends {
        // iterate backwards down the chain and accumulate the min and max on either side
        let c = &dag.node_costs;
        let mut current = (chain_end, c[chain_end]);
        let mut min_node = current;
        let mut max_before = current;
        let mut max_after = current;
        while dag.children[current.0].len() == 1 {
            current = {
                let child = dag.children[current.0][0];
                (child, c[child])
            };
            if current.1 < min_node.1 {
                max_before = *vec![max_before, min_node, max_after, current]
                    .iter()
                    .max_by_key(|(_node, cost)| cost)
                    .unwrap();
                min_node = current;
                max_after = current;
            } else if current.1 > max_after.1 {
                max_after = current;
            }
        }
        // and drop all the other nodes
        let mut current = chain_end;
        while dag.children[current].len() == 1 {
            current = dag.children[current][0];
            if current != min_node.0 && current != max_before.0 && current != max_after.0 {
                nodes_to_prune.insert(current);
            }
        }
    }
    let nodes_to_keep = (0..dag.node_costs.len())
        .filter(|i| !nodes_to_prune.contains(i))
        .collect();
    let dag = dag.sub_dag(&nodes_to_keep);
    (dag, nodes_to_keep)
}

fn subset_order_to_full_order(
    order: &Vec<usize>,
    kept_nodes: &Vec<usize>,
    dag: &Dag,
) -> Vec<usize> {
    let mut result: Vec<usize> = vec![];
    let mut result_set: HashSet<usize> = HashSet::new();

    fn recurse(orig_i: usize, result: &mut Vec<usize>, result_set: &mut HashSet<usize>, dag: &Dag) {
        if !result_set.contains(&orig_i) {
            for child in &dag.children[orig_i] {
                if !result_set.contains(child) {
                    recurse(*child, result, result_set, dag);
                }
            }
            result.push(orig_i);
            result_set.insert(orig_i);
        }
    }

    for sub_i in order {
        let orig_i = kept_nodes[*sub_i];
        recurse(orig_i, &mut result, &mut result_set, dag)
    }
    for output in dag.get_outputs() {
        recurse(output, &mut result, &mut result_set, dag);
    }

    result
}

pub fn circuit_to_schedule(
    circuit: CircuitRc,
    settings: OptimizationSettings,
) -> Result<Schedule, SchedulingError> {
    let max_elements_in_memory = settings.max_memory / get_compatible_dtype(&circuit).size();
    let chunk_size = max_elements_in_memory / settings.scheduling_num_mem_chunks;
    let dag = circuits_to_dag(&[&**circuit]);

    let order_result = {
        // currently dag simplifications increase achievable memory usage unfortunately
        // todo make better simplifications
        if settings.scheduling_simplify {
            // operate on subset dag
            let (sub_dag, kept_nodes) =
                simplify_dag_for_scheduling_and_kept_nodes(&dag, chunk_size);
            if settings.verbose >= 2 {
                println!(
                    "dag sizes: orig: {} pruned: {}",
                    dag.node_costs.len(),
                    sub_dag.node_costs.len()
                );
            }
            schedule_dag_strategy_ints(
                &sub_dag,
                settings.verbose,
                max_elements_in_memory,
                settings.scheduling_num_mem_chunks,
            )
            .map(|sub_order| subset_order_to_full_order(&sub_order, &kept_nodes, &dag))
        } else {
            schedule_dag_strategy_ints(
                &dag,
                settings.verbose,
                max_elements_in_memory,
                settings.scheduling_num_mem_chunks,
            )
        }
    };
    if order_result.is_err() {
        circuit.compiler_print();
    }

    let order = order_result?;

    let to_node = hash_to_node(&circuit);
    let circuit_order: Vec<CircuitRc> = order
        .iter()
        .map(|x| to_node[&dag.node_hashes[*x]].clone())
        .collect();
    let mut out = order_to_schedule(
        &circuit_order,
        &to_node
            .iter()
            .filter_map(|x| x.1.as_array_constant().cloned())
            .collect(),
        &to_node
            .iter()
            .filter_map(|x| x.1.as_scalar_constant().cloned())
            .collect(),
        dag.get_outputs()
            .iter()
            .map(|x| dag.node_hashes[*x])
            .collect(),
        get_compatible_dtype(&circuit),
    );
    out.output_circuit = Some(circuit);

    Ok(out)
}

pub fn circuit_to_schedule_naive_toposort(circuit: CircuitRc) -> Schedule {
    let toposorted = toposort_circuit(circuit.clone());
    let mut result = order_to_schedule(
        &toposorted,
        &vec![],
        &vec![],
        HashSet::from([circuit.info().hash]),
        get_compatible_dtype(&circuit),
    );
    result.output_circuit = Some(circuit);
    result
}

#[pyfunction]
pub fn scheduled_evaluate(
    circuit: CircuitRc,
    settings: OptimizationSettings,
) -> Result<Tensor, SchedulingError> {
    let schedule = circuit_to_schedule(circuit.clone(), settings)?;
    Ok(evaluate_schedule(&schedule)[&circuit.info().hash].clone())
}
