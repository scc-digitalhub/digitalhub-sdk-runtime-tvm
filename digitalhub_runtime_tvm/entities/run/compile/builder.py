# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.run.compile.entity import RunTvmRunCompile
from digitalhub_runtime_tvm.entities.run.compile.spec import RunSpecTvmRunCompile, RunValidatorTvmRunCompile
from digitalhub_runtime_tvm.entities.run.compile.status import RunStatusTvmRunCompile


class RunTvmRunCompileBuilder(RunBuilder, RuntimeEntityBuilderTvm):
    """
    RunTvmRunCompileBuilder runner.
    """

    ENTITY_CLASS = RunTvmRunCompile
    ENTITY_SPEC_CLASS = RunSpecTvmRunCompile
    ENTITY_SPEC_VALIDATOR = RunValidatorTvmRunCompile
    ENTITY_STATUS_CLASS = RunStatusTvmRunCompile
    ENTITY_KIND = EntityKinds.RUN_TVM_COMPILE.value
