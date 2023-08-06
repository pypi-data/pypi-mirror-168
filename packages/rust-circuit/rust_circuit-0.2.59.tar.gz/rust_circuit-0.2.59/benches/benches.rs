#![feature(test)]

// #[cfg(test)]

use criterion::black_box;
use criterion::criterion_group;
use criterion::criterion_main;
use criterion::Criterion;
use rust_circuit::circuit::algebraic_rewrite::einsum_nest_path;
use rust_circuit::circuit::circuit_optimizer::OptimizationContext;
use rust_circuit::circuit::circuit_optimizer::OptimizationSettings;
use rust_circuit::circuit::deep_rewrite::compiler_simp;
use rust_circuit::circuit::CircuitNode;
use rust_circuit::circuit::*;
use rust_circuit::opt_einsum::EinsumSpec;
use rust_circuit::rearrange_spec::*;
use rust_circuit::sv;
use rust_circuit::tensor_util::*;
use rust_circuit::timed;
extern crate test;

// TODO: these tests won't compile because the randn_named_seeded function has been replaced
// Calls will need to change from randn_named_seeded(vec, name, seed) to randn_seeded(vec, name, TorchDeviceDtypeOp::default(), seed)
// Ditto for new_tensor_randint_seeded
fn test_notebook_examples(circuits: &[CircuitRc]) {
    let mut settings: OptimizationSettings = Default::default();
    settings.verbose = 2;
    settings.log_simplifications = true;
    let mut context = OptimizationContext::new_settings(settings);
    for circuit in circuits {
        let result = compiler_simp(&circuit, &mut context);
        black_box(result);
        // println!("{}",context.stringify_logs());
        // println!("{:?}", result.info().hash);
    }
    // println!("yo dude");
}

fn test_einsum_specs(einsum_specs: &Vec<EinsumSpec>) {
    for spec in einsum_specs {
        black_box(spec.optimize(None, None, None, None));
    }
}

fn criterion_benchmark(c: &mut Criterion) {
    pyo3::prepare_freethreaded_python();
    #[rustfmt::skip]
    let einsumspecs = vec![EinsumSpec{input_ints:vec![vec![0,1,2],vec![0,3,4],vec![0,3,5],vec![6,2,7],vec![8,9,10],vec![11,7,12],vec![4,13],vec![14,15],vec![16,14],vec![5,13],vec![13,9],vec![17,14],vec![0],vec![12,18],vec![17,18],vec![10,18],vec![16,18],vec![17],vec![16],vec![5],vec![4],vec![5],vec![4],vec![17],vec![16],vec![8,19],vec![11,20],vec![3,21],vec![1,22],vec![19,23],vec![20,24],vec![6,25],vec![1,25],vec![21,26],vec![22,27],vec![23,26],vec![24,27],vec![],vec![]], output_ints:vec![15], int_sizes:vec![32768,32,384,32,384,384,32,384,9,384,384,9,384,768,768,384,384,384,60,32,32,9,9,9,9,5,4,4]},EinsumSpec{input_ints:vec![vec![0,1,2],vec![0,3,4],vec![5,1,6],vec![7,4,8],vec![9,10,11],vec![12,8,13],vec![2,14],vec![15,16],vec![17,15],vec![6,14],vec![14,10],vec![18,15],vec![5],vec![13,19],vec![18,19],vec![11,19],vec![17,19],vec![18],vec![17],vec![6],vec![2],vec![6],vec![2],vec![18],vec![17],vec![9,20],vec![12,21],vec![1,22],vec![3,23],vec![20,24],vec![21,25],vec![7,26],vec![3,26],vec![22,27],vec![23,28],vec![24,27],vec![25,28],vec![],vec![],vec![]], output_ints:vec![16], int_sizes:vec![32768,32,384,32,384,32768,384,32,384,9,384,384,9,384,768,768,384,384,384,60,32,32,9,9,9,9,5,4,4]},EinsumSpec{input_ints:vec![vec![0,1,2],vec![0,1,3],vec![4,5,6],vec![7,6,8],vec![3,9],vec![2,9],vec![9,10],vec![11,12,13],vec![14,15],vec![11,16,17],vec![11,12,14],vec![4],vec![1,11,5],vec![13,18],vec![8,19],vec![17,18],vec![10,19],vec![13],vec![17],vec![2],vec![3],vec![11,16],vec![2],vec![3],vec![13],vec![17],vec![7,20],vec![5,20],vec![1],vec![1],vec![18,21],vec![19,21],vec![],vec![],vec![]], output_ints:vec![15], int_sizes:vec![32768,32,384,384,32768,32,384,32,384,768,384,8,48,384,384,384,48,384,2,2,5,2]},EinsumSpec{input_ints:vec![vec![0,1,2],vec![0,3,4],vec![0,3,5],vec![6,2,7],vec![4,8],vec![5,8],vec![8,9],vec![10,11,12],vec![13,14],vec![10,15,16],vec![10,11,13],vec![0],vec![3,10,1],vec![12,17],vec![7,18],vec![16,17],vec![9,18],vec![12],vec![16],vec![5],vec![4],vec![10,15],vec![5],vec![4],vec![12],vec![16],vec![6,19],vec![1,19],vec![3],vec![3],vec![17,20],vec![18,20],vec![],vec![]], output_ints:vec![14], int_sizes:vec![32768,32,384,32,384,384,32,384,768,384,8,48,384,384,384,48,384,2,2,5,2]},EinsumSpec{input_ints:vec![vec![0,1,2],vec![0,1,3],vec![4,5,6],vec![7,6,8],vec![9,10,11],vec![12,8,13],vec![3,14],vec![15,16],vec![17,15],vec![2,14],vec![14,10],vec![18,15],vec![4],vec![13,19],vec![18,19],vec![11,19],vec![17,19],vec![18],vec![17],vec![2],vec![3],vec![2],vec![3],vec![18],vec![17],vec![9,20],vec![12,21],vec![1,22],vec![5,23],vec![20,24],vec![21,25],vec![7,26],vec![5,26],vec![22,27],vec![23,28],vec![24,27],vec![25,28],vec![],vec![],vec![]], output_ints:vec![16], int_sizes:vec![32768,32,384,384,32768,32,384,32,384,9,384,384,9,384,768,768,384,384,384,60,32,32,9,9,9,9,5,4,4]},EinsumSpec{input_ints:vec![vec![0,1,2],vec![0,3,4],vec![5,1,6],vec![7,4,8],vec![9,10,11],vec![12,8,13],vec![6,14],vec![15,16],vec![17,15],vec![2,14],vec![14,10],vec![18,15],vec![5],vec![13,19],vec![18,19],vec![11,19],vec![17,19],vec![18],vec![17],vec![2],vec![6],vec![2],vec![6],vec![18],vec![17],vec![9,20],vec![12,21],vec![1,22],vec![3,23],vec![20,24],vec![21,25],vec![7,26],vec![3,26],vec![22,27],vec![23,28],vec![24,27],vec![25,28],vec![],vec![],vec![]], output_ints:vec![16], int_sizes:vec![32768,32,384,32,384,32768,384,32,384,9,384,384,9,384,768,768,384,384,384,60,32,32,9,9,9,9,5,4,4]},EinsumSpec{input_ints:vec![vec![0,1,2],vec![0,3,4],vec![5,1,6],vec![7,4,8],vec![2,9],vec![6,9],vec![9,10],vec![11,12,13],vec![14,15],vec![11,16,17],vec![11,12,14],vec![5],vec![1,11,3],vec![13,18],vec![8,19],vec![17,18],vec![10,19],vec![13],vec![17],vec![6],vec![2],vec![11,16],vec![6],vec![2],vec![13],vec![17],vec![7,20],vec![3,20],vec![1],vec![1],vec![18,21],vec![19,21],vec![],vec![],vec![]], output_ints:vec![15], int_sizes:vec![32768,32,384,32,384,32768,384,32,384,768,384,8,48,384,384,384,48,384,2,2,5,2]},EinsumSpec{input_ints:vec![vec![0,1,2],vec![0,3,4],vec![5,1,6],vec![7,4,8],vec![6,9],vec![2,9],vec![9,10],vec![11,12,13],vec![14,15],vec![11,16,17],vec![11,12,14],vec![5],vec![1,11,3],vec![13,18],vec![8,19],vec![17,18],vec![10,19],vec![13],vec![17],vec![2],vec![6],vec![11,16],vec![2],vec![6],vec![13],vec![17],vec![7,20],vec![3,20],vec![1],vec![1],vec![18,21],vec![19,21],vec![],vec![],vec![]], output_ints:vec![15], int_sizes:vec![32768,32,384,32,384,32768,384,32,384,768,384,8,48,384,384,384,48,384,2,2,5,2]},EinsumSpec{input_ints:vec![vec![0,1,2],vec![0,3,4],vec![5,4,6],vec![7,2,8],vec![9,8,10],vec![11,6,12],vec![13,14],vec![15,13],vec![16,13],vec![0],vec![12,17],vec![16,17],vec![10,17],vec![15,17],vec![14],vec![16],vec![15],vec![14],vec![16],vec![15],vec![14],vec![9,18],vec![11,19],vec![1,20],vec![3,21],vec![18,22],vec![19,23],vec![5,24],vec![3,24],vec![7,25],vec![1,25],vec![20,26],vec![21,27],vec![22,26],vec![23,27],vec![],vec![]], output_ints:vec![], int_sizes:vec![32768,32,384,32,384,32,384,32,384,9,384,9,384,768,384,384,384,60,32,32,9,9,9,9,5,5,4,4]}];
    #[rustfmt::skip]
    let circuits:&[CircuitRc] = &[
                    {
        let node0 = ArrayConstant::randn_seeded(sv![50259,384], Some("w.unembed".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 929193938916086232).rc();
        let node1 = Index::nrc(node0.clone(), TensorIndex ( vec![TensorAxisIndex::Single(373), TensorAxisIndex::Slice(Slice { start:None, stop:None })] ), Some("idx w.unembed".to_owned()));
        let node2 = Rearrange::nrc(node1.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("w.unembed_was_sample".to_owned()));
        let node3 = Index::nrc(node0.clone(), TensorIndex ( vec![TensorAxisIndex::Single(318), TensorAxisIndex::Slice(Slice { start:None, stop:None })] ), Some("idx w.unembed".to_owned()));
        let node4 = Rearrange::nrc(node3.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("w.unembed_is_sample".to_owned()));
        let node5 = ArrayConstant::randn_seeded(sv![32,384], Some("w.pos_embeds".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 18302579321424555450).rc();
        let node6 = ScalarConstant::nrc(-1_f64, sv![], Some("unnamed".to_owned()));
        let node7 = ArrayConstant::randn_seeded(sv![50259,384], Some("all_tok_embeds".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 2599709625776908268).rc();
        let node8 = Rearrange::nrc(node7.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![1]], sv![OpSize::from(Some(50259)),OpSize::from(Some(384))]), Some("tok_embeds_pre_idx_flat".to_owned()));
        let node9 = Index::nrc(node8.clone(), TensorIndex ( vec![TensorAxisIndex::new_tensor_randint_seeded(10259872, 50259, TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 4821441715517981202), TensorAxisIndex::Slice(Slice { start:None, stop:None })] ), Some("idx tok_embeds_pre_idx_flat".to_owned()));
        let node10 = Rearrange::nrc(node9.clone(), RearrangeSpec::new(sv![sv![0,1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(320621)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("tok_embeds_post_t_shape".to_owned()));
        let node11 = ScalarConstant::nrc(1_f64, sv![], Some("one".to_owned()));
        let node12 = ArrayConstant::randn_seeded(sv![384,768], Some("m1.w.w1".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 1331227591797635193).rc();
        let node13 = Rearrange::nrc(node12.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(384)),OpSize::from(Some(768)),OpSize::from(Some(20))]), Some("m1.w.w1_sample".to_owned()));
        let node14 = ArrayConstant::randn_seeded(sv![384,768], Some("m1.w.w0".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 13185449622808679385).rc();
        let node15 = Rearrange::nrc(node14.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(384)),OpSize::from(Some(768)),OpSize::from(Some(20))]), Some("m1.w.w0_sample".to_owned()));
        let node16 = ArrayConstant::randn_seeded(sv![768,384], Some("m1.w.out".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 9981532348689177629).rc();
        let node17 = Rearrange::nrc(node16.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(768)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m1.w.out_sample".to_owned()));
        let node18 = ArrayConstant::randn_seeded(sv![768], Some("m1.w.b1".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 1286372835866939057).rc();
        let node19 = Rearrange::nrc(node18.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(768)),OpSize::from(Some(20))]), Some("m1.w.b1_sample".to_owned()));
        let node20 = Rearrange::nrc(node19.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(768)),OpSize::from(Some(1))]), Some("m1.w.b1_sample_rearrange_for_add_1".to_owned()));
        let node21 = ArrayConstant::randn_seeded(sv![768], Some("m1.w.b0".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 4766085074108096736).rc();
        let node22 = Rearrange::nrc(node21.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(768)),OpSize::from(Some(20))]), Some("m1.w.b0_sample".to_owned()));
        let node23 = Rearrange::nrc(node22.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(768)),OpSize::from(Some(1))]), Some("m1.w.b0_sample_rearrange_for_add_1".to_owned()));
        let node24 = ArrayConstant::randn_seeded(sv![384], Some("m1.n.w.scale".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 1636268016078253515).rc();
        let node25 = Rearrange::nrc(node24.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m1.n.w.scale_sample".to_owned()));
        let node26 = ArrayConstant::randn_seeded(sv![384], Some("m1.n.w.mean".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 5460868922970385475).rc();
        let node27 = Rearrange::nrc(node26.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m1.n.w.mean_sample".to_owned()));
        let node28 = Rearrange::nrc(node27.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("m1.n.w.mean_sample_rearrange_for_add_4".to_owned()));
        let node29 = ArrayConstant::randn_seeded(sv![384,768], Some("m0.w.w1".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 311213855405491785).rc();
        let node30 = Rearrange::nrc(node29.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(384)),OpSize::from(Some(768)),OpSize::from(Some(20))]), Some("m0.w.w1_sample".to_owned()));
        let node31 = ArrayConstant::randn_seeded(sv![384,768], Some("m0.w.w0".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 864408194459359880).rc();
        let node32 = Rearrange::nrc(node31.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(384)),OpSize::from(Some(768)),OpSize::from(Some(20))]), Some("m0.w.w0_sample".to_owned()));
        let node33 = ArrayConstant::randn_seeded(sv![768,384], Some("m0.w.out".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 10661202434590036135).rc();
        let node34 = Rearrange::nrc(node33.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(768)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m0.w.out_sample".to_owned()));
        let node35 = ArrayConstant::randn_seeded(sv![768], Some("m0.w.b1".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 11681755502347863569).rc();
        let node36 = Rearrange::nrc(node35.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(768)),OpSize::from(Some(20))]), Some("m0.w.b1_sample".to_owned()));
        let node37 = Rearrange::nrc(node36.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(768)),OpSize::from(Some(1))]), Some("m0.w.b1_sample_rearrange_for_add_1".to_owned()));
        let node38 = ArrayConstant::randn_seeded(sv![768], Some("m0.w.b0".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 2323622703274767530).rc();
        let node39 = Rearrange::nrc(node38.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(768)),OpSize::from(Some(20))]), Some("m0.w.b0_sample".to_owned()));
        let node40 = Rearrange::nrc(node39.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(768)),OpSize::from(Some(1))]), Some("m0.w.b0_sample_rearrange_for_add_1".to_owned()));
        let node41 = ArrayConstant::randn_seeded(sv![384], Some("m0.n.w.scale".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 3754049060485329335).rc();
        let node42 = Rearrange::nrc(node41.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m0.n.w.scale_sample".to_owned()));
        let node43 = ArrayConstant::randn_seeded(sv![384], Some("m0.n.w.mean".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 1526190999291891454).rc();
        let node44 = Rearrange::nrc(node43.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m0.n.w.mean_sample".to_owned()));
        let node45 = Rearrange::nrc(node44.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("m0.n.w.mean_sample_rearrange_for_add_2".to_owned()));
        let node46 = Index::nrc(node10.clone(), TensorIndex ( vec![TensorAxisIndex::Slice(Slice { start:None, stop:None }), TensorAxisIndex::Slice(Slice { start:None, stop:None }), TensorAxisIndex::Slice(Slice { start:Some(0), stop:Some(384) })] ), Some("idx tok_embeds_post_t_shape".to_owned()));
        let node47 = Index::nrc(node46.clone(), TensorIndex ( vec![TensorAxisIndex::new_tensor_randint_seeded(20, 320621, TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 18345059311376053207), TensorAxisIndex::Slice(Slice { start:None, stop:None }), TensorAxisIndex::Slice(Slice { start:None, stop:None })] ), Some("idx idx tok_embeds_post_t_shape".to_owned()));
        let node48 = Rearrange::nrc(node47.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("embed_var_sample_rearrange_for_add_0".to_owned()));
        let node49 = ScalarConstant::nrc(0.044194173824159216_f64, sv![], Some("c.div_seq_len".to_owned()));
        let node50 = Rearrange::nrc(node49.clone(), RearrangeSpec::new(sv![], sv![sv![0]], sv![OpSize::from(Some(20))]), Some("c.div_seq_len_sample".to_owned()));
        let node51 = ArrayConstant::randn_seeded(sv![8,48,384], Some("a0.w.v".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 10133531896693890946).rc();
        let node52 = Rearrange::nrc(node51.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(48)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a0.w.v_sample".to_owned()));
        let node53 = ArrayConstant::randn_seeded(sv![8,1,1], Some("a0.w.sb".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 1867266222616571753).rc();
        let node54 = Rearrange::nrc(node53.clone(), RearrangeSpec::new(sv![sv![0],sv![],sv![]], sv![sv![3],sv![0],sv![],sv![]], sv![OpSize::from(Some(8)),OpSize::from(Some(1)),OpSize::from(Some(1)),OpSize::from(Some(20))]), Some("a0.w.sb_sample".to_owned()));
        let node55 = Rearrange::nrc(node54.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![],sv![]], sv![sv![0],sv![1],sv![],sv![]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(1)),OpSize::from(Some(1))]), Some("a0.w.sb_sample_rearrange_for_add_2".to_owned()));
        let node56 = ArrayConstant::randn_seeded(sv![8,48,384], Some("a0.w.q".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 15164929069836551244).rc();
        let node57 = Rearrange::nrc(node56.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(48)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a0.w.q_sample".to_owned()));
        let node58 = Einsum::nrc(vec![(node56.clone(), sv![0,1,2]),(node5.clone(), sv![3,2])], sv![0,3,1], Some("a0.w.pos_q".to_owned()));
        let node59 = Rearrange::nrc(node58.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48)),OpSize::from(Some(20))]), Some("a0.w.pos_q_sample".to_owned()));
        let node60 = Rearrange::nrc(node59.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48))]), Some("a0.w.pos_q_sample_rearrange_for_add_1".to_owned()));
        let node61 = ArrayConstant::randn_seeded(sv![8,48,384], Some("a0.w.k".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 13890711741635822223).rc();
        let node62 = Einsum::nrc(vec![(node61.clone(), sv![0,1,2]),(node5.clone(), sv![3,2])], sv![0,3,1], Some("a0.w.pos_k".to_owned()));
        let node63 = Rearrange::nrc(node62.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48)),OpSize::from(Some(20))]), Some("a0.w.pos_k_sample".to_owned()));
        let node64 = Rearrange::nrc(node63.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48))]), Some("a0.w.pos_k_sample_rearrange_for_add_1".to_owned()));
        let node65 = ArrayConstant::randn_seeded(sv![8,48,384], Some("a0.w.out".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 11344873045249210841).rc();
        let node66 = Rearrange::nrc(node65.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(48)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a0.w.out_sample".to_owned()));
        let node67 = Rearrange::nrc(node61.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(48)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a0.w.k_sample".to_owned()));
        let node68 = ArrayConstant::randn_seeded(sv![8], Some("a0.w.g1".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 2618613096524235656).rc();
        let node69 = ArrayConstant::randn_seeded(sv![32], Some("a0.c.inv_nelt".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 7885258334619126176).rc();
        let node70 = Einsum::nrc(vec![(node68.clone(), sv![0]),(node69.clone(), sv![1])], sv![0,1], Some("a0.w.g1op".to_owned()));
        let node71 = Rearrange::nrc(node70.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a0.w.g1op_sample".to_owned()));
        let node72 = Add::nrc(vec![node11.clone(), node70.clone()], Some("a0.w.c1".to_owned()));
        let node73 = Rearrange::nrc(node72.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a0.w.c1_sample".to_owned()));
        let node74 = ArrayConstant::randn_seeded(sv![384], Some("a0.n.w.scale".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 13379100888128585973).rc();
        let node75 = Rearrange::nrc(node74.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a0.n.w.scale_sample".to_owned()));
        let node76 = ArrayConstant::randn_seeded(sv![384], Some("a0.n.w.mean".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 14181844882358567796).rc();
        let node77 = Rearrange::nrc(node76.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a0.n.w.mean_sample".to_owned()));
        let node78 = Rearrange::nrc(node77.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("a0.n.w.mean_sample_rearrange_for_add_1".to_owned()));
        let node79 = Einsum::nrc(vec![(node78.clone(), sv![0,1,2]),(node6.clone(), sv![])], sv![0,1,2], Some("ScalarMul".to_owned()));
        let node80 = Add::nrc(vec![node48.clone(), node79.clone()], Some("a0.n.sub_mean_sample".to_owned()));
        let node81 = Einsum::nrc(vec![(node80.clone(), sv![0,1,2]),(node75.clone(), sv![0,2])], sv![0,1,2], Some("a0.n.y_scale_sample".to_owned()));
        let node82 = ArrayConstant::randn_seeded(sv![384], Some("a0.n.w.var".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 2097624483321698950).rc();
        let node83 = ScalarConstant::nrc(0.00001_f64, sv![], Some("a0.n.eps".to_owned()));
        let node84 = Add::nrc(vec![node82.clone(), node83.clone()], Some("a0.n.w.var_p_eps".to_owned()));
        let node85 = GeneralFunction::new_by_name(vec![node84.clone()], "rsqrt".to_owned(), Some("a0.n.w.full_mul".to_owned())).unwrap().rc();
        let node86 = Rearrange::nrc(node85.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a0.n.w.full_mul_sample".to_owned()));
        let node87 = Einsum::nrc(vec![(node81.clone(), sv![0,1,2]),(node86.clone(), sv![0,2])], sv![0,1,2], Some("a0.n.y_out_sample".to_owned()));
        let node88 = Rearrange::nrc(node87.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("a0.n.y_out_sample_rearrange_for_add_1".to_owned()));
        let node89 = ArrayConstant::randn_seeded(sv![384], Some("a0.n.w.bias".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 7836263396355991022).rc();
        let node90 = Rearrange::nrc(node89.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a0.n.w.bias_sample".to_owned()));
        let node91 = Rearrange::nrc(node90.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("a0.n.w.bias_sample_rearrange_for_add_0".to_owned()));
        let node92 = Add::nrc(vec![node91.clone(), node88.clone()], Some("a0.n_sample".to_owned()));
        let node93 = Einsum::nrc(vec![(node52.clone(), sv![0,1,2,3]),(node92.clone(), sv![0,4,3])], sv![0,1,4,2], Some("a0.v_sample".to_owned()));
        let node94 = Einsum::nrc(vec![(node57.clone(),  sv![0,1,2,3]),(node92.clone(),  sv![0,4,3])],  sv![0,1,4,2], Some("a0.q_sample".to_owned()));
        let node95 = Rearrange::nrc(node94.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48))]), Some("a0.q_sample_rearrange_for_add_0".to_owned()));
        let node96 = Einsum::nrc(vec![(node67.clone(),  sv![0,1,2,3]),(node92.clone(),  sv![0,4,3])],  sv![0,1,4,2], Some("a0.k_sample".to_owned()));
        let node97 = Rearrange::nrc(node96.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48))]), Some("a0.k_sample_rearrange_for_add_0".to_owned()));
        let node98 = Add::nrc(vec![node95.clone(), node60.clone()], Some("a0.f_q_sample".to_owned()));
        let node99 = Add::nrc(vec![node97.clone(), node64.clone()], Some("a0.f_k_sample".to_owned()));
        let node100 = ScalarConstant::nrc(0.14433756729740646_f64, sv![], Some("a0.c.div_head_size".to_owned()));
        let node101 = Rearrange::nrc(node100.clone(), RearrangeSpec::new(sv![], sv![sv![0]], sv![OpSize::from(Some(20))]), Some("a0.c.div_head_size_sample".to_owned()));
        let node102 = Einsum::nrc(vec![(node98.clone(), sv![0,1,2,3]),(node99.clone(), sv![0,1,4,3]),(node101.clone(), sv![0])], sv![0,1,2,4], Some("a0.scores_not_masked_sample".to_owned()));
        let node103 = Rearrange::nrc(node102.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(32))]), Some("a0.scores_not_masked_sample_rearrange_for_add_0".to_owned()));
        let node104 = ArrayConstant::randn_seeded(sv![32,32], Some("a0.s.w.scale".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 4874878538922573945).rc();
        let node105 = Rearrange::nrc(node104.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a0.s.w.scale_sample".to_owned()));
        let node106 = ArrayConstant::randn_seeded(sv![32,32], Some("a0.s.w.mean".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 4942623806828509992).rc();
        let node107 = Rearrange::nrc(node106.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a0.s.w.mean_sample".to_owned()));
        let node108 = Rearrange::nrc(node107.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(1))]), Some("a0.s.w.mean_sample_rearrange_for_add_1".to_owned()));
        let node109 = Einsum::nrc(vec![(node108.clone(), sv![0,1,2,3]),(node6.clone(), sv![])], sv![0,1,2,3], Some("ScalarMul".to_owned()));
        let node110 = Add::nrc(vec![node103.clone(), node109.clone()], Some("a0.s.sub_mean_sample".to_owned()));
        let node111 = Einsum::nrc(vec![(node110.clone(), sv![0,1,2,3]),(node105.clone(), sv![0,2,3])], sv![0,1,2,3], Some("a0.s.y_scale_sample".to_owned()));
        let node112 = ArrayConstant::randn_seeded(sv![32,32], Some("a0.s.w.var".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 17367023124078262057).rc();
        let node113 = ScalarConstant::nrc(0.00001_f64, sv![], Some("a0.s.eps".to_owned()));
        let node114 = Add::nrc(vec![node112.clone(), node113.clone()], Some("a0.s.w.var_p_eps".to_owned()));
        let node115 = GeneralFunction::new_by_name(vec![node114.clone()], "rsqrt".to_owned(), Some("a0.s.w.full_mul".to_owned())).unwrap().rc();
        let node116 = Rearrange::nrc(node115.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a0.s.w.full_mul_sample".to_owned()));
        let node117 = Einsum::nrc(vec![(node111.clone(), sv![0,1,2,3]),(node116.clone(), sv![0,2,3])], sv![0,1,2,3], Some("a0.s.y_out_sample".to_owned()));
        let node118 = Rearrange::nrc(node117.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(32))]), Some("a0.s.y_out_sample_rearrange_for_add_1".to_owned()));
        let node119 = ArrayConstant::randn_seeded(sv![32,32], Some("a0.s.w.bias".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 15464796744735661784).rc();
        let node120 = Rearrange::nrc(node119.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a0.s.w.bias_sample".to_owned()));
        let node121 = Rearrange::nrc(node120.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(1))]), Some("a0.s.w.bias_sample_rearrange_for_add_0".to_owned()));
        let node122 = Add::nrc(vec![node121.clone(), node118.clone()], Some("a0.s_sample".to_owned()));
        let node123 = Einsum::nrc(vec![(node122.clone(),  sv![0,1,2,3]),(node50.clone(),  sv![0])],  sv![0,1,2,3], Some("a0.scores_normed_sample".to_owned()));
        let node124 = ArrayConstant::randn_seeded(sv![32,32], Some("a0.c.score_mask".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 8724464318490575396).rc();
        let node125 = Rearrange::nrc(node124.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a0.c.score_mask_sample".to_owned()));
        let node126 = Einsum::nrc(vec![(node123.clone(),  sv![0,1,2,3]),(node125.clone(),  sv![0,2,3])],  sv![0,1,2,3], Some("a0.scores_mul_mask_sample".to_owned()));
        let node127 = Einsum::nrc(vec![(node126.clone(),  sv![0,1,2,3]),(node71.clone(),  sv![0,1,2])],  sv![0,1,2], Some("a0.t1_sample".to_owned()));
        let node128 = Rearrange::nrc(node127.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2],sv![]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(1))]), Some("a0.t1u_sample".to_owned()));
        let node129 = Rearrange::nrc(node128.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![]], sv![sv![0],sv![1],sv![2],sv![]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(1))]), Some("a0.t1u_sample_rearrange_for_add_1".to_owned()));
        let node130 = Einsum::nrc(vec![(node123.clone(), sv![0,1,2,3]),(node73.clone(), sv![0,1,2])], sv![0,1,2,3], Some("a0.t0_sample".to_owned()));
        let node131 = Rearrange::nrc(node130.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(32))]), Some("a0.t0_sample_rearrange_for_add_0".to_owned()));
        let node132 = Einsum::nrc(vec![(node129.clone(), sv![0,1,2,3]),(node6.clone(), sv![])], sv![0,1,2,3], Some("ScalarMul".to_owned()));
        let node133 = Add::nrc(vec![node131.clone(), node132.clone(), node55.clone()], Some("a0.pre_probs_sample".to_owned()));
        let node134 = ArrayConstant::randn_seeded(sv![32,32], Some("a0.pp.c.score_mask".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 8724464318490575396).rc();
        let node135 = Rearrange::nrc(node134.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a0.pp.c.score_mask_sample".to_owned()));
        let node136 = Einsum::nrc(vec![(node133.clone(), sv![0,1,2,3]),(node135.clone(), sv![0,2,3])], sv![0,1,2,3], Some("a0.probs_sample".to_owned()));
        let node137 = Einsum::nrc(vec![(node136.clone(), sv![0,1,2,3]),(node93.clone(), sv![0,1,3,4])], sv![0,2,1,4], Some("a0.comb_v_sample".to_owned()));
        let node138 = Einsum::nrc(vec![(node137.clone(), sv![0,1,2,3]),(node66.clone(), sv![0,2,3,4])], sv![0,1,4], Some("a0_sample".to_owned()));
        let node139 = Rearrange::nrc(node138.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("a0_sample_rearrange_for_add_1".to_owned()));
        let node140 = Einsum::nrc(vec![(node45.clone(), sv![0,1,2]),(node6.clone(), sv![])], sv![0,1,2], Some("ScalarMul".to_owned()));
        let node141 = Add::nrc(vec![node48.clone(), node139.clone(), node140.clone()], Some("m0.n.sub_mean_sample".to_owned()));
        let node142 = Einsum::nrc(vec![(node141.clone(), sv![0,1,2]),(node42.clone(), sv![0,2])], sv![0,1,2], Some("m0.n.y_scale_sample".to_owned()));
        let node143 = ArrayConstant::randn_seeded(sv![384], Some("m0.n.w.var".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 1660750471384108115).rc();
        let node144 = ScalarConstant::nrc(0.00001_f64, sv![], Some("m0.n.eps".to_owned()));
        let node145 = Add::nrc(vec![node143.clone(), node144.clone()], Some("m0.n.w.var_p_eps".to_owned()));
        let node146 = GeneralFunction::new_by_name(vec![node145.clone()], "rsqrt".to_owned(), Some("m0.n.w.full_mul".to_owned())).unwrap().rc();
        let node147 = Rearrange::nrc(node146.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m0.n.w.full_mul_sample".to_owned()));
        let node148 = Einsum::nrc(vec![(node142.clone(), sv![0,1,2]),(node147.clone(), sv![0,2])], sv![0,1,2], Some("m0.n.y_out_sample".to_owned()));
        let node149 = Rearrange::nrc(node148.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("m0.n.y_out_sample_rearrange_for_add_1".to_owned()));
        let node150 = ArrayConstant::randn_seeded(sv![384], Some("m0.n.w.bias".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 7338166352898341219).rc();
        let node151 = Rearrange::nrc(node150.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m0.n.w.bias_sample".to_owned()));
        let node152 = Rearrange::nrc(node151.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("m0.n.w.bias_sample_rearrange_for_add_0".to_owned()));
        let node153 = Add::nrc(vec![node152.clone(), node149.clone()], Some("m0.n_sample".to_owned()));
        let node154 = Einsum::nrc(vec![(node153.clone(), sv![0,1,2]),(node30.clone(), sv![0,2,3])], sv![0,1,3], Some("m0.before_product1_sample".to_owned()));
        let node155 = Rearrange::nrc(node154.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(768))]), Some("m0.before_product1_sample_rearrange_for_add_0".to_owned()));
        let node156 = Einsum::nrc(vec![(node153.clone(), sv![0,1,2]),(node32.clone(), sv![0,2,3])], sv![0,1,3], Some("m0.before_product0_sample".to_owned()));
        let node157 = Rearrange::nrc(node156.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(768))]), Some("m0.before_product0_sample_rearrange_for_add_0".to_owned()));
        let node158 = Add::nrc(vec![node155.clone(), node37.clone()], Some("m0.add1_sample".to_owned()));
        let node159 = Add::nrc(vec![node157.clone(), node40.clone()], Some("m0.add0_sample".to_owned()));
        let node160 = Einsum::nrc(vec![(node159.clone(), sv![0,1,2]),(node158.clone(), sv![0,1,2])], sv![0,1,2], Some("m0.act_sample".to_owned()));
        let node161 = Einsum::nrc(vec![(node160.clone(), sv![0,1,2]),(node34.clone(), sv![0,2,3])], sv![0,1,3], Some("m0_sample".to_owned()));
        let node162 = Rearrange::nrc(node161.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("m0_sample_rearrange_for_add_2".to_owned()));
        let node163 = ArrayConstant::randn_seeded(sv![8,48,384], Some("a1.w.v".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 8687698313936163101).rc();
        let node164 = Rearrange::nrc(node163.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(48)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a1.w.v_sample".to_owned()));
        let node165 = ArrayConstant::randn_seeded(sv![8,1,1], Some("a1.w.sb".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 2763458983135939246).rc();
        let node166 = Rearrange::nrc(node165.clone(), RearrangeSpec::new(sv![sv![0],sv![],sv![]], sv![sv![3],sv![0],sv![],sv![]], sv![OpSize::from(Some(8)),OpSize::from(Some(1)),OpSize::from(Some(1)),OpSize::from(Some(20))]), Some("a1.w.sb_sample".to_owned()));
        let node167 = Rearrange::nrc(node166.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![],sv![]], sv![sv![0],sv![1],sv![],sv![]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(1)),OpSize::from(Some(1))]), Some("a1.w.sb_sample_rearrange_for_add_2".to_owned()));
        let node168 = ArrayConstant::randn_seeded(sv![8,48,384], Some("a1.w.q".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 7589589553252889926).rc();
        let node169 = Rearrange::nrc(node168.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(48)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a1.w.q_sample".to_owned()));
        let node170 = Einsum::nrc(vec![(node168.clone(), sv![0,1,2]),(node5.clone(), sv![3,2])], sv![0,3,1], Some("a1.w.pos_q".to_owned()));
        let node171 = Rearrange::nrc(node170.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48)),OpSize::from(Some(20))]), Some("a1.w.pos_q_sample".to_owned()));
        let node172 = Rearrange::nrc(node171.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48))]), Some("a1.w.pos_q_sample_rearrange_for_add_1".to_owned()));
        let node173 = ArrayConstant::randn_seeded(sv![8,48,384], Some("a1.w.k".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 346631027691184275).rc();
        let node174 = Einsum::nrc(vec![(node173.clone(), sv![0,1,2]),(node5.clone(), sv![3,2])], sv![0,3,1], Some("a1.w.pos_k".to_owned()));
        let node175 = Rearrange::nrc(node174.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48)),OpSize::from(Some(20))]), Some("a1.w.pos_k_sample".to_owned()));
        let node176 = Rearrange::nrc(node175.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48))]), Some("a1.w.pos_k_sample_rearrange_for_add_1".to_owned()));
        let node177 = ArrayConstant::randn_seeded(sv![8,48,384], Some("a1.w.out".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 15478159692831585940).rc();
        let node178 = Rearrange::nrc(node177.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(48)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a1.w.out_sample".to_owned()));
        let node179 = Rearrange::nrc(node173.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![3],sv![0],sv![1],sv![2]], sv![OpSize::from(Some(8)),OpSize::from(Some(48)),OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a1.w.k_sample".to_owned()));
        let node180 = ArrayConstant::randn_seeded(sv![8], Some("a1.w.g1".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 3291412235451830005).rc();
        let node181 = ArrayConstant::randn_seeded(sv![32], Some("a1.c.inv_nelt".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 7885258334619126176).rc();
        let node182 = Einsum::nrc(vec![(node180.clone(), sv![0]),(node181.clone(), sv![1])], sv![0,1], Some("a1.w.g1op".to_owned()));
        let node183 = Rearrange::nrc(node182.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a1.w.g1op_sample".to_owned()));
        let node184 = Add::nrc(vec![node11.clone(), node182.clone()], Some("a1.w.c1".to_owned()));
        let node185 = Rearrange::nrc(node184.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a1.w.c1_sample".to_owned()));
        let node186 = ArrayConstant::randn_seeded(sv![384], Some("a1.n.w.scale".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 2062098532837674558).rc();
        let node187 = Rearrange::nrc(node186.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a1.n.w.scale_sample".to_owned()));
        let node188 = ArrayConstant::randn_seeded(sv![384], Some("a1.n.w.mean".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 10253594586416472532).rc();
        let node189 = Rearrange::nrc(node188.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a1.n.w.mean_sample".to_owned()));
        let node190 = Rearrange::nrc(node189.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("a1.n.w.mean_sample_rearrange_for_add_3".to_owned()));
        let node191 = Einsum::nrc(vec![(node190.clone(), sv![0,1,2]),(node6.clone(), sv![])], sv![0,1,2], Some("ScalarMul".to_owned()));
        let node192 = Add::nrc(vec![node48.clone(), node139.clone(), node162.clone(), node191.clone()], Some("a1.n.sub_mean_sample".to_owned()));
        let node193 = Einsum::nrc(vec![(node192.clone(), sv![0,1,2]),(node187.clone(), sv![0,2])], sv![0,1,2], Some("a1.n.y_scale_sample".to_owned()));
        let node194 = ArrayConstant::randn_seeded(sv![384], Some("a1.n.w.var".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 1425219787154012984).rc();
        let node195 = ScalarConstant::nrc(0.00001_f64, sv![], Some("a1.n.eps".to_owned()));
        let node196 = Add::nrc(vec![node194.clone(), node195.clone()], Some("a1.n.w.var_p_eps".to_owned()));
        let node197 = GeneralFunction::new_by_name(vec![node196.clone()], "rsqrt".to_owned(), Some("a1.n.w.full_mul".to_owned())).unwrap().rc();
        let node198 = Rearrange::nrc(node197.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a1.n.w.full_mul_sample".to_owned()));
        let node199 = Einsum::nrc(vec![(node193.clone(), sv![0,1,2]),(node198.clone(), sv![0,2])], sv![0,1,2], Some("a1.n.y_out_sample".to_owned()));
        let node200 = Rearrange::nrc(node199.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("a1.n.y_out_sample_rearrange_for_add_1".to_owned()));
        let node201 = ArrayConstant::randn_seeded(sv![384], Some("a1.n.w.bias".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 10960967166164370007).rc();
        let node202 = Rearrange::nrc(node201.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("a1.n.w.bias_sample".to_owned()));
        let node203 = Rearrange::nrc(node202.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("a1.n.w.bias_sample_rearrange_for_add_0".to_owned()));
        let node204 = Add::nrc(vec![node203.clone(), node200.clone()], Some("a1.n_sample".to_owned()));
        let node205 = Einsum::nrc(vec![(node164.clone(), sv![0,1,2,3]),(node204.clone(), sv![0,4,3])], sv![0,1,4,2], Some("a1.v_sample".to_owned()));
        let node206 = Einsum::nrc(vec![(node169.clone(), sv![0,1,2,3]),(node204.clone(), sv![0,4,3])], sv![0,1,4,2], Some("a1.q_sample".to_owned()));
        let node207 = Rearrange::nrc(node206.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48))]), Some("a1.q_sample_rearrange_for_add_0".to_owned()));
        let node208 = Einsum::nrc(vec![(node179.clone(),  sv![0,1,2,3]),(node204.clone(),  sv![0,4,3])],  sv![0,1,4,2], Some("a1.k_sample".to_owned()));
        let node209 = Rearrange::nrc(node208.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(48))]), Some("a1.k_sample_rearrange_for_add_0".to_owned()));
        let node210 = Add::nrc(vec![node207.clone(), node172.clone()], Some("a1.f_q_sample".to_owned()));
        let node211 = Add::nrc(vec![node209.clone(), node176.clone()], Some("a1.f_k_sample".to_owned()));
        let node212 = ScalarConstant::nrc(0.14433756729740646_f64, sv![], Some("a1.c.div_head_size".to_owned()));
        let node213 = Rearrange::nrc(node212.clone(), RearrangeSpec::new(sv![], sv![sv![0]], sv![OpSize::from(Some(20))]), Some("a1.c.div_head_size_sample".to_owned()));
        let node214 = Einsum::nrc(vec![(node210.clone(), sv![0,1,2,3]),(node211.clone(), sv![0,1,4,3]),(node213.clone(), sv![0])], sv![0,1,2,4], Some("a1.scores_not_masked_sample".to_owned()));
        let node215 = Rearrange::nrc(node214.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(32))]), Some("a1.scores_not_masked_sample_rearrange_for_add_0".to_owned()));
        let node216 = ArrayConstant::randn_seeded(sv![32,32], Some("a1.s.w.scale".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 3798037696282213373).rc();
        let node217 = Rearrange::nrc(node216.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a1.s.w.scale_sample".to_owned()));
        let node218 = ArrayConstant::randn_seeded(sv![32,32], Some("a1.s.w.mean".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 15738309107844885954).rc();
        let node219 = Rearrange::nrc(node218.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a1.s.w.mean_sample".to_owned()));
        let node220 = Rearrange::nrc(node219.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(1))]), Some("a1.s.w.mean_sample_rearrange_for_add_1".to_owned()));
        let node221 = Einsum::nrc(vec![(node220.clone(),  sv![0,1,2,3]),(node6.clone(),  sv![])],  sv![0,1,2,3], Some("ScalarMul".to_owned()));
        let node222 = Add::nrc(vec![node215.clone(), node221.clone()], Some("a1.s.sub_mean_sample".to_owned()));
        let node223 = Einsum::nrc(vec![(node222.clone(),  sv![0,1,2,3]),(node217.clone(),  sv![0,2,3])],  sv![0,1,2,3], Some("a1.s.y_scale_sample".to_owned()));
        let node224 = ArrayConstant::randn_seeded(sv![32,32], Some("a1.s.w.var".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 4873730304271440433).rc();
        let node225 = ScalarConstant::nrc(0.00001_f64, sv![], Some("a1.s.eps".to_owned()));
        let node226 = Add::nrc(vec![node224.clone(), node225.clone()], Some("a1.s.w.var_p_eps".to_owned()));
        let node227 = GeneralFunction::new_by_name(vec![node226.clone()], "rsqrt".to_owned(), Some("a1.s.w.full_mul".to_owned())).unwrap().rc();
        let node228 = Rearrange::nrc(node227.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a1.s.w.full_mul_sample".to_owned()));
        let node229 = Einsum::nrc(vec![(node223.clone(),  sv![0,1,2,3]),(node228.clone(),  sv![0,2,3])],  sv![0,1,2,3], Some("a1.s.y_out_sample".to_owned()));
        let node230 = Rearrange::nrc(node229.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(32))]), Some("a1.s.y_out_sample_rearrange_for_add_1".to_owned()));
        let node231 = ArrayConstant::randn_seeded(sv![32,32], Some("a1.s.w.bias".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 4903695795856462846).rc();
        let node232 = Rearrange::nrc(node231.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a1.s.w.bias_sample".to_owned()));
        let node233 = Rearrange::nrc(node232.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(1))]), Some("a1.s.w.bias_sample_rearrange_for_add_0".to_owned()));
        let node234 = Add::nrc(vec![node233.clone(), node230.clone()], Some("a1.s_sample".to_owned()));
        let node235 = Einsum::nrc(vec![(node234.clone(),  sv![0,1,2,3]),(node50.clone(),  sv![0])],  sv![0,1,2,3], Some("a1.scores_normed_sample".to_owned()));
        let node236 = ArrayConstant::randn_seeded(sv![32,32], Some("a1.c.score_mask".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 8724464318490575396).rc();
        let node237 = Rearrange::nrc(node236.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a1.c.score_mask_sample".to_owned()));
        let node238 = Einsum::nrc(vec![(node235.clone(),  sv![0,1,2,3]),(node237.clone(),  sv![0,2,3])],  sv![0,1,2,3], Some("a1.scores_mul_mask_sample".to_owned()));
        let node239 = Einsum::nrc(vec![(node238.clone(),  sv![0,1,2,3]),(node183.clone(),  sv![0,1,2])],  sv![0,1,2], Some("a1.t1_sample".to_owned()));
        let node240 = Rearrange::nrc(node239.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2],sv![]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(1))]), Some("a1.t1u_sample".to_owned()));
        let node241 = Rearrange::nrc(node240.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![]], sv![sv![0],sv![1],sv![2],sv![]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(1))]), Some("a1.t1u_sample_rearrange_for_add_1".to_owned()));
        let node242 = Einsum::nrc(vec![(node235.clone(), sv![0,1,2,3]),(node185.clone(), sv![0,1,2])], sv![0,1,2,3], Some("a1.t0_sample".to_owned()));
        let node243 = Rearrange::nrc(node242.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2],sv![3]], sv![sv![0],sv![1],sv![2],sv![3]], sv![OpSize::from(Some(20)),OpSize::from(Some(8)),OpSize::from(Some(32)),OpSize::from(Some(32))]), Some("a1.t0_sample_rearrange_for_add_0".to_owned()));
        let node244 = Einsum::nrc(vec![(node241.clone(),sv![0,1,2,3]),(node6.clone(),sv![])],sv![0,1,2,3], Some("ScalarMul".to_owned()));
        let node245 = Add::nrc(vec![node243.clone(), node244.clone(), node167.clone()], Some("a1.pre_probs_sample".to_owned()));
        let node246 = ArrayConstant::randn_seeded(sv![32,32], Some("a1.pp.c.score_mask".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 8724464318490575396).rc();
        let node247 = Rearrange::nrc(node246.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![2],sv![0],sv![1]], sv![OpSize::from(Some(32)),OpSize::from(Some(32)),OpSize::from(Some(20))]), Some("a1.pp.c.score_mask_sample".to_owned()));
        let node248 = Einsum::nrc(vec![(node245.clone(), sv![0,1,2,3]),(node247.clone(), sv![0,2,3])], sv![0,1,2,3], Some("a1.probs_sample".to_owned()));
        let node249 = Einsum::nrc(vec![(node248.clone(), sv![0,1,2,3]),(node205.clone(), sv![0,1,3,4])], sv![0,2,1,4], Some("a1.comb_v_sample".to_owned()));
        let node250 = Einsum::nrc(vec![(node249.clone(), sv![0,1,2,3]),(node178.clone(), sv![0,2,3,4])], sv![0,1,4], Some("a1_sample".to_owned()));
        let node251 = Rearrange::nrc(node250.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("a1_sample_rearrange_for_add_3".to_owned()));
        let node252 = Einsum::nrc(vec![(node28.clone(),  sv![0,1,2]),(node6.clone(),  sv![])],  sv![0,1,2], Some("ScalarMul".to_owned()));
        let node253 = Add::nrc(vec![node48.clone(), node139.clone(), node162.clone(), node251.clone(), node252.clone()], Some("m1.n.sub_mean_sample".to_owned()));
        let node254 = Einsum::nrc(vec![(node253.clone(),  sv![0,1,2]),(node25.clone(),  sv![0,2])],  sv![0,1,2], Some("m1.n.y_scale_sample".to_owned()));
        let node255 = ArrayConstant::randn_seeded(sv![384], Some("m1.n.w.var".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 7096362628065231700).rc();
        let node256 = ScalarConstant::nrc(0.00001_f64, sv![], Some("m1.n.eps".to_owned()));
        let node257 = Add::nrc(vec![node255.clone(), node256.clone()], Some("m1.n.w.var_p_eps".to_owned()));
        let node258 = GeneralFunction::new_by_name(vec![node257.clone()], "rsqrt".to_owned(), Some("m1.n.w.full_mul".to_owned())).unwrap().rc();
        let node259 = Rearrange::nrc(node258.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m1.n.w.full_mul_sample".to_owned()));
        let node260 = Einsum::nrc(vec![(node254.clone(),sv![0,1,2]),(node259.clone(),sv![0,2])],sv![0,1,2], Some("m1.n.y_out_sample".to_owned()));
        let node261 = Rearrange::nrc(node260.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("m1.n.y_out_sample_rearrange_for_add_1".to_owned()));
        let node262 = ArrayConstant::randn_seeded(sv![384], Some("m1.n.w.bias".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 5952620041495829705).rc();
        let node263 = Rearrange::nrc(node262.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("m1.n.w.bias_sample".to_owned()));
        let node264 = Rearrange::nrc(node263.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("m1.n.w.bias_sample_rearrange_for_add_0".to_owned()));
        let node265 = Add::nrc(vec![node264.clone(), node261.clone()], Some("m1.n_sample".to_owned()));
        let node266 = Einsum::nrc(vec![(node265.clone(),sv![0,1,2]),(node13.clone(),sv![0,2,3])],sv![0,1,3], Some("m1.before_product1_sample".to_owned()));
        let node267 = Rearrange::nrc(node266.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(768))]), Some("m1.before_product1_sample_rearrange_for_add_0".to_owned()));
        let node268 = Einsum::nrc(vec![(node265.clone(), sv![0,1,2]),(node15.clone(), sv![0,2,3])], sv![0,1,3], Some("m1.before_product0_sample".to_owned()));
        let node269 = Rearrange::nrc(node268.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(768))]), Some("m1.before_product0_sample_rearrange_for_add_0".to_owned()));
        let node270 = Add::nrc(vec![node267.clone(), node20.clone()], Some("m1.add1_sample".to_owned()));
        let node271 = Add::nrc(vec![node269.clone(), node23.clone()], Some("m1.add0_sample".to_owned()));
        let node272 = Einsum::nrc(vec![(node271.clone(), sv![0,1,2]),(node270.clone(), sv![0,1,2])], sv![0,1,2], Some("m1.act_sample".to_owned()));
        let node273 = Einsum::nrc(vec![(node272.clone(), sv![0,1,2]),(node17.clone(), sv![0,2,3])], sv![0,1,3], Some("m1_sample".to_owned()));
        let node274 = Rearrange::nrc(node273.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("m1_sample_rearrange_for_add_4".to_owned()));
        let node275 = ArrayConstant::randn_seeded(sv![384], Some("final.n.w.scale".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 6746609514966997473).rc();
        let node276 = Rearrange::nrc(node275.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("final.n.w.scale_sample".to_owned()));
        let node277 = ArrayConstant::randn_seeded(sv![384], Some("final.n.w.mean".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 5720117413700968387).rc();
        let node278 = Rearrange::nrc(node277.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("final.n.w.mean_sample".to_owned()));
        let node279 = Rearrange::nrc(node278.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("final.n.w.mean_sample_rearrange_for_add_5".to_owned()));
        let node280 = Einsum::nrc(vec![(node279.clone(), sv![0,1,2]),(node6.clone(), sv![])], sv![0,1,2], Some("ScalarMul".to_owned()));
        let node281 = Add::nrc(vec![node48.clone(), node139.clone(), node162.clone(), node251.clone(), node274.clone(), node280.clone()], Some("final.n.sub_mean_sample".to_owned()));
        let node282 = Einsum::nrc(vec![(node281.clone(), sv![0,1,2]),(node276.clone(), sv![0,2])], sv![0,1,2], Some("final.n.y_scale_sample".to_owned()));
        let node283 = ArrayConstant::randn_seeded(sv![384], Some("final.n.w.var".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 4811093865619151916).rc();
        let node284 = ScalarConstant::nrc(0.00001_f64, sv![], Some("final.n.eps".to_owned()));
        let node285 = Add::nrc(vec![node283.clone(), node284.clone()], Some("final.n.w.var_p_eps".to_owned()));
        let node286 = GeneralFunction::new_by_name(vec![node285.clone()], "rsqrt".to_owned(), Some("final.n.w.full_mul".to_owned())).unwrap().rc();
        let node287 = Rearrange::nrc(node286.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("final.n.w.full_mul_sample".to_owned()));
        let node288 = Einsum::nrc(vec![(node282.clone(), sv![0,1,2]),(node287.clone(), sv![0,2])], sv![0,1,2], Some("final.n.y_out_sample".to_owned()));
        let node289 = Rearrange::nrc(node288.clone(), RearrangeSpec::new(sv![sv![0],sv![1],sv![2]], sv![sv![0],sv![1],sv![2]], sv![OpSize::from(Some(20)),OpSize::from(Some(32)),OpSize::from(Some(384))]), Some("final.n.y_out_sample_rearrange_for_add_1".to_owned()));
        let node290 = ArrayConstant::randn_seeded(sv![384], Some("final.n.w.bias".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 1794834663544597504).rc();
        let node291 = Rearrange::nrc(node290.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![1],sv![0]], sv![OpSize::from(Some(384)),OpSize::from(Some(20))]), Some("final.n.w.bias_sample".to_owned()));
        let node292 = Rearrange::nrc(node291.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(384)),OpSize::from(Some(1))]), Some("final.n.w.bias_sample_rearrange_for_add_0".to_owned()));
        let node293 = Add::nrc(vec![node292.clone(), node289.clone()], Some("final.n_sample".to_owned()));
        let node294 = Einsum::nrc(vec![(node293.clone(), sv![0,1,2]),(node2.clone(), sv![0,2])], sv![0,1], Some("logits_was_sample".to_owned()));
        let node295 = Rearrange::nrc(node294.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(32))]), Some("logits_was_sample_rearrange_for_add_1".to_owned()));
        let node296 = Einsum::nrc(vec![(node293.clone(), sv![0,1,2]),(node4.clone(), sv![0,2])], sv![0,1], Some("logits_is_sample".to_owned()));
        let node297 = Rearrange::nrc(node296.clone(), RearrangeSpec::new(sv![sv![0],sv![1]], sv![sv![0],sv![1]], sv![OpSize::from(Some(20)),OpSize::from(Some(32))]), Some("logits_is_sample_rearrange_for_add_0".to_owned()));
        let node298 = Einsum::nrc(vec![(node295.clone(),  sv![0,1]),(node6.clone(),  sv![])],  sv![0,1], Some("ScalarMul".to_owned()));
        let node299 = Add::nrc(vec![node297.clone(), node298.clone()], Some("logit_diff_all_sample".to_owned()));
        let node300 = ArrayConstant::randn_seeded(sv![320621], Some("is_is".to_owned()), TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 2613995473774786597).rc();
        let node301 = Index::nrc(node299.clone(), TensorIndex ( vec![TensorAxisIndex::Slice(Slice { start:None, stop:None }), TensorAxisIndex::Single(-1)] ), Some("idx logit_diff_all_sample".to_owned()));
        let node302 = Index::nrc(node300.clone(), TensorIndex ( vec![TensorAxisIndex::new_tensor_randint_seeded(20, 320621, TorchDeviceDtypeOp { device: Some("cuda:0".to_owned()), dtype: Some("float32".to_owned()) }, 18345059311376053207)] ), Some("idx is_is".to_owned()));
        let node303 = Einsum::nrc(vec![(node301.clone(), sv![0]),(node302.clone(), sv![0])], sv![0], Some("logit_diff_times_correct_sample".to_owned()));
        let node304 = Rearrange::nrc(node303.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![0]], sv![OpSize::from(Some(20))]), Some("logit_diff_times_correct_sample_rearrange_for_add_0".to_owned()));
        let node305 = GeneralFunction::new_by_name(vec![node301.clone()], "sigmoid".to_owned(), Some("logit_diff_sigmoid_sample".to_owned())).unwrap().rc();
        let node306 = GeneralFunction::new_by_name(vec![node301.clone()], "log_exp_p_1".to_owned(), Some("logit_diff_log_exp_p_1_sample".to_owned())).unwrap().rc();
        let node307 = Rearrange::nrc(node306.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![0]], sv![OpSize::from(Some(20))]), Some("logit_diff_log_exp_p_1_sample_rearrange_for_add_1".to_owned()));
        let node308 = Einsum::nrc(vec![(node307.clone(), sv![0]),(node6.clone(), sv![])], sv![0], Some("ScalarMul".to_owned()));
        let node309 = Add::nrc(vec![node304.clone(), node308.clone()], Some("log_loss_sample".to_owned()));
        let node310 = Rearrange::nrc(node309.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![0]], sv![OpSize::from(None)]), Some("flatten".to_owned()));
        let node311 = ScalarConstant::nrc(0.05_f64, sv![20], Some("empirical_weights_for_sampled".to_owned()));
        let node312 = Rearrange::nrc(node311.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![0]], sv![OpSize::from(None)]), Some("flatten".to_owned()));
        let node313 = Rearrange::nrc(node305.clone(), RearrangeSpec::new(sv![sv![0]], sv![sv![0]], sv![OpSize::from(None)]), Some("flatten".to_owned()));
        Concat::nrc(vec![node312.clone(), node310.clone(), node313.clone()], 0, Some("flat_concat".to_owned()))
    },];
    let mut group = c.benchmark_group("all");
    // group.measurement_time(Duration::from_millis(10000));
    // group.sample_size(20);
    // group.bench_function("einsum_opt", |b| {
    //     b.iter(|| {
    //         for _i in 0..1 {
    //             test_einsum_specs(black_box(&einsumspecs));
    //         }
    //     })
    // });
    group.bench_function("notebook_examples", |b| {
        b.iter(|| {
            for _i in 0..1 {
                test_notebook_examples(black_box(circuits))
            }
        })
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);

#[bench]
fn the_benchmarks(_b: &mut Bencher) {
    benches();

    Criterion::default().configure_from_args().final_summary();
}
