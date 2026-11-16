# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun


class RunSpecTvmRunBuild(RunSpecTvmRun):
    """
    Tvm build run specifications.
    """

    image: str | None = None
    simplify: bool | None = None
    target_opset: int | None = None
    opset_override: int | None = None
    strict_shape_inference: bool | None = None
    data_prop: bool | None = None
    keep_params_in_input: bool | None = None
    sanitize_input_names: bool | None = None


class RunValidatorTvmRunBuild(RunSpecTvmRunBuild):
    """Compatibility name for the typed TVM build-run spec."""
