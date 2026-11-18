# DigitalHub SDK Runtime TVM

[![license](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/scc-digitalhub/digitalhub-sdk-runtime-tvm/blob/main/LICENSE) ![GitHub Release](https://img.shields.io/github/v/release/scc-digitalhub/digitalhub-sdk-runtime-tvm)
![Status](https://img.shields.io/badge/status-stable-gold)

The TVM extension for the [DigitalHub SDK](https://github.com/scc-digitalhub/digitalhub-sdk)
creates Functions and Runs for ONNX/TFLite import, CPU/CUDA compilation and Go/Rust serving
through CORE. Compilation runs on Kubernetes; this package is the client.

See the [TVM SDK reference](https://scc-digitalhub.github.io/docs/0.16/sdk/reference/runtimes/tvm/overview/)
for all action parameters and examples.

## Quick start

To install the Digitalhub SDK Runtime Tvm, you can use pip:

```bash
pip install digitalhub-runtime-tvm
```

## TVM run options (CORE 0.16)

Use this extension with CORE 0.16's Run specs:

| Object      | Settings                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------- |
| Function    | Source `model`, `format`; generated `ir_model` reference                                       |
| Task        | `function`, `resources`, `profile`, `envs`, `secrets`, `volumes`                            |
| Build Run   | `image` and ONNX conversion options                                                         |
| Compile Run | `model_path`, `target_architecture` or `target`, `tag`, `image`, `optimization`, `tuning`   |
| Serve Run   | `model_path`, `served_name`, `image`, `replicas`, `workers`, `service_type`, `service_name` |

Pass TVM options to each Run; old Task options and previous Runs do not provide
defaults. Common Task settings can be overridden for one Run.

```python
import digitalhub as dh

project = dh.get_or_create_project("my-project")
model = project.log_onnx(name="xinet", source="model.onnx")
function = project.new_function(name="xinet", kind="tvm", model=model.key)
function.run("build", sort_onnx=True, simplify=True, wait=True)
compiled = function.run(
    "compile",
    target_architecture="amd64",
    resources={"cpu": "4", "mem": "8Gi"},
    optimization={"opt_level": 3, "exec_mode": "bytecode", "benchmark_runs": 10},
    tuning={"tuning_mode": "off"},
    wait=True,
)
function.run(
    "serve",
    model_path=compiled.status.to_dict()["outputs"]["compiled_so"],
    served_name="xinet",
    workers=1,
    resources={"cpu": "4", "mem": "2Gi"},
)
```

Build options include `image`, `sort_onnx`, `simplify`, `target_opset`, `opset_override`,
`strict_shape_inference`, `data_prop`, `keep_params_in_input` and `sanitize_input_names`.

`sort_onnx` defaults to `False` in the builder. Set it to `True` to order nodes by their
dependencies. It is independent of `simplify`. With sorting disabled, ONNX validation
remains enabled and rejects unordered graphs. The source ONNX Model is preserved;
the build publishes the converted TVM IR rather than a separate sorted ONNX Model.

Compile accepts `model_path` to override `function.ir_model`; serve requires a
versioned `model_path` from the chosen Compile's `status.outputs.compiled_so`.
Other serve options are `served_name`, `image`,
`replicas`, `workers`, `service_type` and `service_name`.

Compile options are serialized in `optimization` and `tuning` groups, as in CORE.
Flat keyword arguments such as `opt_level=3` and `tuning_mode="off"` are also accepted;
explicit grouped values take precedence. Omitted values use CORE defaults.

CORE saves only the build's `ir_model` reference on the Function. Each Compile keeps
its own output, so compiling for another architecture does not change the Model
selected by a Serve. Legacy Function `so_model` values are ignored; a new Serve
without `model_path` is rejected. Existing services retain their selected Model.

### CPU profiles and explicit targets

`profile` chooses platform scheduling/resources, such as a Raspberry Pi node;
it does not choose the generated code's architecture.

`target_architecture` is a profile name configured by CORE in `runtime-tvm.yaml`,
not a fixed SDK enumeration. The console lists the configured profiles. CORE validates
names and resolves any configured aliases.

For a one-off CPU configuration, omit `target_architecture` (or set it to `auto`)
and pass a standard TVM target object instead. The separate `profile` parameter
can still select platform scheduling and resources:

```python
function.run(
    "compile",
    target={"kind": "llvm", "mtriple": "aarch64-linux-gnu", "mcpu": "cortex-a72"},
    optimization={"cross_cc": "aarch64-linux-gnu-g++"},
    wait=True,
)
```

Do not combine an explicit target with a non-auto `target_architecture`. Optional
`optimization.cross_cc_options` takes separate compiler arguments, for example
`["--sysroot=/opt/sysroots/arm64"]`; that directory must exist in the compile image.
When selecting a preset, omit it to inherit the preset's arguments, or pass `[]`
to clear them. An explicit target does not inherit preset linker settings.
Use `image` when another toolchain is needed. The LLVM target above selects Linux
CPU compilation; CUDA needs the device and host configuration below.

`tuning_mode="off"` (the default) preserves but ignores all other tuning values.
`tune` requires `tuning_trials`; `apply` requires `tuning_model_path` and ignores search
settings. Local tuning ignores RPC fields; RPC tuning requires `rpc_tracker_host`,
`rpc_tracker_port` and `rpc_tracker_key`, and ignores the local runner timeout.
CORE also checks compatibility with the selected target, toolchain and Job resources.

| Target         | CPU profile                                                         |
| -------------- | ------------------------------------------------------------------- |
| `auto`         | Generic CPU of the compile node                                     |
| `amd64`        | Intel/AMD 64-bit, x86-64-v2                                         |
| `amd64_v3`     | Intel/AMD 64-bit, x86-64-v3 (AVX2)                                  |
| `amd64_native` | CPU of the AMD64 compile node; requires compatible serving hardware |
| `arm64`        | Generic ARM 64-bit (AArch64)                                        |
| `arm64_pi5`    | Raspberry Pi 5, Cortex-A76                                          |
| `arm32`        | ARM 32-bit, ARMv7 hard-float with NEON                              |

The aliases accepted by CORE (`cpu`, `llvm`, `x86`, `x86_v3`, `x86_native`, `armv7l`)
resolve to these profiles without rewriting the saved run. They do not enable
additional architectures.

### CUDA device and Linux host

An explicit CUDA target requires `arch` (for example `sm_87` or `sm_90a`) and a nested
`host` target with `kind="llvm"` and an explicit Linux GNU AMD64 or ARM64 `mtriple`.
Standard TVM options on both targets are preserved. As with an LLVM target, leave
`target_architecture` omitted or `auto` when supplying `target`.

```python
function.run(
    "compile",
    target={
        "kind": "cuda",
        "arch": "sm_87",
        "host": {"kind": "llvm", "mtriple": "aarch64-linux-gnu", "mcpu": "cortex-a78"},
    },
    image="your-registry/tvm-toolkit-cuda:your-tag",
    profile="jetson-orin",
    resources={"cpu": "4", "mem": "8Gi", "gpu": "1"},
    optimization={"cross_cc": "aarch64-linux-gnu-g++"},
    wait=True,
)
```

Use `x86_64-linux-gnu` for an AMD64 host. CORE also provides the
`target_architecture="jetson_orin_cuda"` preset for `sm_87` with an
`aarch64-linux-gnu` host; omit `target` when selecting it. Target selection does
not choose a Kubernetes profile, request a GPU, or supply a CUDA image. Set those
Task/Run settings for the cluster and use a CUDA-enabled TVM toolchain with `nvcc`
and a linker for the selected host. The image and scheduling profile above are
placeholders for your cluster configuration.

CUDA tuning requires explicit device limits from the real GPU profile:
`max_shared_memory_per_block`, `max_threads_per_block` and `thread_warp_size` in
`target`. Local tuning needs a visible GPU on a matching host; RPC tuning uses the
configured remote GPU. CPU cache flushing is unsupported for CUDA tuning.

Serving uses the compiled Model's target metadata to select the backend. Use the
same Serve Run options with a CUDA-capable serving image and a compatible visible
NVIDIA GPU/driver; there is no separate serve device option.

## Development

The fixtures under `test/instances/` describe Function, Task, Run and Model schemas.
Keep them aligned with CORE when changing the SDK specs. Compile contract tests check
both the SDK schema and the CORE export under `test/instances/schemas`; populate that
directory from `schemas/specs` in the matching CORE checkout. These tests validate
serialization and schema contracts without executing CUDA workloads.
Set `TVM_CORE_SCHEMA_DIR=/path/to/digitalhub-core/schemas/specs` for local contract
tests and `TVM_REQUIRE_CORE_SCHEMAS=1` to fail if exports are missing. The CI still
uses CORE `main` by default. Its manual `core_schema_ref` input supports a specific
CORE commit for coordinated integration checks; matching exports must reach main
before normal CI can pass. A passing local test does not update remote schemas.

To run the complete suite against a local CORE checkout, use a Python environment
with this package's `.[dev]` dependencies installed and run the following from this
repository's root. Set the paths to the matching CORE and DigitalHub SDK checkouts.
The shared SDK checkout must provide the typed Pydantic specs and test helpers.
The entity fixture tests read `instances/schemas`, while the contract tests also
accept `TVM_CORE_SCHEMA_DIR`.

```bash
core_schemas=/path/to/digitalhub-core/schemas/specs
shared_sdk=/path/to/digitalhub-sdk
test_dir="$(mktemp -d)"
mkdir "$test_dir/instances"
cp test/test_*.py "$test_dir/"
cp -R test/instances/entities "$test_dir/instances/"
ln -s "$core_schemas" "$test_dir/instances/schemas"
PYTHONPATH="$PWD:$shared_sdk:$shared_sdk/test/_digitalhub_test_helpers" \
  TVM_CORE_SCHEMA_DIR="$core_schemas" TVM_REQUIRE_CORE_SCHEMAS=1 \
  python -m pytest "$test_dir" -q
```

TVM-specific fields belong to Run specs, while Tasks carry common Kubernetes
settings. Align both repositories and all six TVM Task/Run schemas when integrating
upstream changes that placed TVM fields on Tasks. Deployment profile names are
validated against the server configuration; the SDK cannot enumerate them.

Both runtime validation and JSON Schema apply tuning constraints only to active
fields. CUDA tuning requires the three real device limits and rejects CPU cache
flushing. Integral CUDA numbers such as `32.0` normalize to integers; booleans,
strings, fractions and nonpositive limits are rejected. SDK profile strings are
trimmed and lowercased before serialization; schemas describe the serialized form.

See [Contributing](#contributing).

## Security Policy

The current release is the supported version. Security fixes are released together with all other fixes in each new release.

If you discover a security vulnerability in this project, please do not open a public issue.

Instead, report it privately by emailing us at digitalhub@fbk.eu. Include as much detail as possible to help us understand and address the issue quickly and responsibly.

## Contributing

To report a bug or request a feature, please first check the existing issues to avoid duplicates. If none exist, open a new issue with a clear title and a detailed description, including any steps to reproduce if it's a bug.

To contribute code, start by forking the repository. Clone your fork locally and create a new branch for your changes. Make sure your commits follow the [Conventional Commits v1.0](https://www.conventionalcommits.org/en/v1.0.0/) specification to keep history readable and consistent.

Once your changes are ready, push your branch to your fork and open a pull request against the main branch. Be sure to include a summary of what you changed and why. If your pull request addresses an issue, mention it in the description (e.g., “Closes #123”).

Please note that new contributors may be asked to sign a Contributor License Agreement (CLA) before their pull requests can be merged. This helps us ensure compliance with open source licensing standards.

We appreciate contributions and help in improving the project!

## Authors

This project is developed and maintained by **DSLab – Fondazione Bruno Kessler**, with contributions from the open source community. A complete list of contributors is available in the project’s commit history and pull requests.

For questions or inquiries, please contact: [digitalhub@fbk.eu](mailto:digitalhub@fbk.eu)

## Copyright and license

Copyright © 2025 DSLab – Fondazione Bruno Kessler and individual contributors.

This project is licensed under the Apache License, Version 2.0.
You may not use this file except in compliance with the License. Ownership of contributions remains with the original authors and is governed by the terms of the Apache 2.0 License, including the requirement to grant a license to the project.
