# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import RunBuilder, RunStatus

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.run.serve.entity import RunTvmRunServe
from digitalhub_runtime_tvm.entities.run.serve.spec import RunSpecTvmRunServe


class RunTvmRunServeBuilder(RunBuilder, RuntimeEntityBuilderTvm):
    """
    RunTvmRunServeBuilder runner.
    """

    ENTITY_CLASS = RunTvmRunServe
    ENTITY_SPEC_CLASS = RunSpecTvmRunServe
    ENTITY_STATUS_CLASS = RunStatus
    ENTITY_KIND = EntityKinds.RUN_TVM_SERVE.value
