# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import RunBuilder, RunStatus

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.run.compile.entity import RunTvmRunCompile
from digitalhub_runtime_tvm.entities.run.compile.spec import RunSpecTvmRunCompile


class RunTvmRunCompileBuilder(RunBuilder, RuntimeEntityBuilderTvm):
    """
    RunTvmRunCompileBuilder runner.
    """

    ENTITY_CLASS = RunTvmRunCompile
    ENTITY_SPEC_CLASS = RunSpecTvmRunCompile
    ENTITY_STATUS_CLASS = RunStatus
    ENTITY_KIND = EntityKinds.RUN_TVM_COMPILE.value
