To develop circuit_compiler_rust, install rust, switch to nightly, then run `maturin develop` - this compiles the rust, and installs it as a python package.

Detailed instructions:
- Install `rustup` from https://rustup.rs/ . Do the default installation.
- Put it in your environment using `source ~/.cargo/env`
- Set default to nightly. `rustup override set nightly`
- Install patchelf and clang (both available on apt-get ubuntu) needed for z3
- Install `maturin`. `pip install -r ~/unity/requirements.txt`

- `cd interp/circuit/rust_circuit`
- (Mac only) Follow the `z3` installation instructions further down before using `maturin develop`
- Run `maturin develop`
  - If `maturin develop` fails with linker errors, you can run `maturin build` then `pip install [path_to_wheel]`. Also you can add the dir containing `libpython3.9.so.1.0` or such to `LD_LIBRARY_PATH`. If you use Conda, maturin can usually find libpython by itself.

  
We publish `rust_circuit` as a pip package, and include `rust_circuit==X.X.X` in our python `requirements.txt`. Right before we merge a PR with Rust changes into main, we have to bump the version number in `requirements.txt` and `Cargo.toml`, and publish the pip package. To publish, manually trigger the CircleCI pipeline with parameter `action=publish`. To publish for just your local OS and python version (which wont work for everyone on the team) and have our PyPI password, use `maturin publish`.

If you're using vscode, we recommend the extension `rust_analyzer` and the following vscode setting:
```
    "rust-analyzer.linkedProjects": [
        "[PATH_TO_UNITY]/unity/interp/circuit/rust_circuit/Cargo.toml"
    ],
```
which allows you to use rust_analyzer when your vscode is opened to a folder other than rust_circuit

## I get a bunch of linker errors when trying to test

Try `cargo test --features "real-pyo3" --no-default-features`. See [here](https://pyo3.rs/latest/faq.html#i-cant-run-cargo-test-im-having-linker-issues-like-symbol-not-found-or-undefined-reference-to-_pyexc_systemerror).

## Installing z3 on Mac

By default, `maturin develop` fails with a z3 related error (such as `z3.h` not found). To fix this you should install `z3` yourself and put it in the system path.

* Option 1: `brew install z3`
  * Link the dylib to your system lib path (`sudo ln -s /opt/homebrew/lib/libz3.dylib /usr/local/lib`)
  * Link the headers to your system header path (`sudo ln -s /opt/homebrew/include/z3*.h /usr/local/include`)

* Option 2: Build `z3` from source yourself
  * Clone z3 (`git clone https://github.com/Z3Prover/z3 && cd z3`)
  * Build z3 from source (see the commands under "Execute:" [here](https://github.com/Z3Prover/z3#building-z3-using-make-and-gccclang))
  * Copy the dylib to your system lib path (`sudo cp build/libz3.dylib /usr/local/lib`)
  * Copy the headers to your system header path (`sudo cp src/api/z3*.h /usr/local/include`)

* Re-run `cargo check` and you should be good to go!
* If this fails, you can also use the `--features static-z3` flag on all cargo commands and on `maturin develop`. This has slower link times but doesn't require the above to work

## Anyhow build error after starting up in rust analyzer

[do what this comment says/read issue more generally](https://github.com/dtolnay/anyhow/issues/250#issuecomment-1209629746)

## About rust_circuit

Rust_circuit is a framework for expressing, manipulating, and optimally computing tensor computations, particularly geared toward computing cumulants. It's based on our python `interp/circuit` codebase. 

Some basic info: We store tensor computations/circuits in AST form in the Circuit/CircuitRc/Einsum/Add... structs. These structs often have multiple references to equivelent nodes, which we handle by hashing nodes with a cryptographic hash function (blake3 currently) and implement Eq by hash, and deduplicating on construction.

Currently, the rust_circuit codebase just optimizes circuits and computes them, and manual creation/manipulation of circuits is in the Python circuits codebase. Eventually creation/manual manipulation will be done on Rust circuits from python.

## Misc advice

- You can view docs locally with `cargo doc --open`

## Correctness conditions not enforced by types

If you mutate a circuit (only the top level, children are in Rc which makes them immutable), you must call `.init_info` after the last mutation to set the node's shape, hash, ect based on children. Normally you just want to call `.new` or `.nrc` or whatever once and not mutate.

## Profiling

To benchmark code, write tests in `benches/benches.rs`, add to Criterion group, and run `cargo bench --no-default-features --features real-pyo3`. 
Currently only simp is benchmarked

To profile code, use
`cargo bench --no-default-features --features real-pyo3  --no-run; flamegraph -o flamegraph.svg --  target/release/deps/benches-36e0a557364e8efa --nocapture`
or generally cargo bench --no-run then an executable profiler.
