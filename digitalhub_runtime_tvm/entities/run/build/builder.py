# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.run.build.entity import RunTvmRunBuild
from digitalhub_runtime_tvm.entities.run.build.spec import RunSpecTvmRunBuild, RunValidatorTvmRunBuild
from digitalhub_runtime_tvm.entities.run.build.status import RunStatusTvmRunBuild


class RunTvmRunBuildBuilder(RunBuilder, RuntimeEntityBuilderTvm):
    """
    RunTvmRunBuildBuilder runner.
    """

    ENTITY_CLASS = RunTvmRunBuild
    ENTITY_SPEC_CLASS = RunSpecTvmRunBuild
    ENTITY_SPEC_VALIDATOR = RunValidatorTvmRunBuild
    ENTITY_STATUS_CLASS = RunStatusTvmRunBuild
    ENTITY_KIND = EntityKinds.RUN_TVM_BUILD.value
