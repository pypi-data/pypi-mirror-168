use rand::Rng;

use rust_circuit::circuit::diag_rewrite::{diags_intersection, diags_union};
use rust_circuit::circuit::{CircuitNode, GeneralFunction};
use rust_circuit::opt_einsum::{
    get_disconnected_sugraphs, get_int_to_tensor_appearance, EinsumSpec,
};
use rust_circuit::sv;
use rust_circuit::tensor_util::{broadcast_shapes, TorchDeviceDtypeOp};

// real tests are in python calling rust, these are for debugging
#[test]
fn test_basic() {
    let examples = [
        // EinsumSpec {
        //     input_ints: vec![vec![0, 1, 2], vec![0, 1], vec![2, 3], vec![0], vec![3, 4]],
        //     output_ints: vec![4],
        //     int_sizes: vec![2, 3, 4, 5, 6, 7],
        // },
        // EinsumSpec {
        //     input_ints: vec![vec![0, 1, 2], vec![0, 1, 3, 2], vec![3]],
        //     output_ints: vec![0, 1, 3],
        //     int_sizes: vec![30000, 8, 32, 35],
        // },
        // EinsumSpec {
        //     input_ints: vec![vec![0, 1, 2], vec![0, 1, 3, 2], vec![3]],
        //     output_ints: vec![0, 1, 3],
        //     int_sizes: vec![30000, 8, 32, 35],
        // },
        // EinsumSpec {
        //     input_ints: vec![vec![0, 0, 0], vec![],vec![1, 0, 2, 0]],
        //     output_ints: vec![0,],
        //     int_sizes: vec![4,2,2],
        // },
        EinsumSpec {
            input_ints: vec![vec![0], vec![1], vec![], vec![2], vec![1, 1], vec![3]],
            output_ints: vec![1],
            int_sizes: vec![2, 4, 1, 5],
        },
    ];
    // (((0,), (1,), (), (2,), (1, 1), (3,)), (1,), (torch.Size([2]), torch.Size([4]), (), torch.Size([1]), torch.Size([4, 4]), (5,)))
    // (((0, 0, 0), (), (1, 0, 2, 0)), (0,), (torch.Size([4, 4, 4]), torch.Size([]), (2, 4, 2, 4)))
    // ('abc,abdc,d->abd', {0: 32768, 1: 8, 2: 32, 3: 35})
    for example in examples.iter() {
        let opted = example.optimize_dp(None, None, None);

        println!("result {:?}", opted);
    }
}

#[test]
#[ignore] // test is slow
fn test_worst_case() {
    // the test is that this halts
    assert!(core::mem::size_of::<usize>() == 8);
    let n_operands = 40;
    let operand_width = 40;
    let n_ints = 40;
    let example = EinsumSpec {
        input_ints: (0..n_operands)
            .map(|_i| {
                (0..operand_width)
                    .map(|_j| rand::thread_rng().gen_range(0..n_ints))
                    .collect()
            })
            .collect(),
        output_ints: vec![0, 1, 1, 2, 3, 4],
        int_sizes: (0..n_ints).collect(),
    };
    println!("have einspec {:?}", example);
    // ('abc,abdc,d->abd', {0: 32768, 1: 8, 2: 32, 3: 35})
    let opted = example.optimize_dp(None, None, Some(500));

    println!("result {:?}", opted);
}

#[test]
fn test_subgraph() {
    let example: Vec<Vec<usize>> = vec![
        vec![0],
        vec![],
        vec![0],
        vec![0, 1, 2],
        vec![0, 3, 4],
        vec![5],
        vec![6],
        vec![],
        vec![6, 1],
        vec![7],
        vec![2, 8],
        vec![8],
        vec![9, 10, 8],
        vec![9, 10],
        vec![11],
        vec![],
        vec![11, 3],
        vec![12],
        vec![4, 13],
        vec![13],
        vec![9, 14, 13],
    ];
    let appear = get_int_to_tensor_appearance(&example);
    println!("appear {:?}", appear);
    let sg = get_disconnected_sugraphs(&example, &appear);
    println!("sg {:?}", sg);
}

#[test]
fn test_broadcast_shapes() {
    let examples = [
        vec![],
        vec![sv![], sv![]],
        vec![sv![1, 2], sv![3, 2, 1]],
        vec![sv![3, 2], sv![3]],
        vec![sv![1, 2, 2], sv![1, 2], sv![3, 2, 2, 2, 172112]],
    ];
    for example in examples {
        println!("{:?}", broadcast_shapes(&example));
    }
}

#[test]
fn test_generalfuction() {
    use rust_circuit::circuit::circuit_optimizer::optimize_and_evaluate;
    use rust_circuit::circuit::{Add, ArrayConstant, Einsum};

    pyo3::prepare_freethreaded_python();
    let circuit = Einsum::nrc(
        vec![(
            Add::nrc(
                vec![
                    ArrayConstant::randn_named(sv![2, 3, 4], None, TorchDeviceDtypeOp::default())
                        .rc(),
                    GeneralFunction::new_by_name(
                        vec![ArrayConstant::randn_named(
                            sv![2, 3, 4],
                            None,
                            TorchDeviceDtypeOp::default(),
                        )
                        .rc()],
                        "sigmoid".to_owned(),
                        None,
                    )
                    .unwrap()
                    .rc(),
                ],
                None,
            ),
            sv![0, 1, 2],
        )],
        sv![0, 1],
        None,
    );
    optimize_and_evaluate(circuit, Default::default()).unwrap();
}

#[test]
fn test_diags_intersection_union() {
    let ex = vec![sv![0, 1, 0, 0], sv![0, 1, 0, 1]];
    let inter = diags_intersection(&ex);
    dbg!(&inter);
    let union = diags_union(&ex);
    dbg!(&union);
}
