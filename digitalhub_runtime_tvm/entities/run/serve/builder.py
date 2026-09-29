# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.run.serve.entity import RunTvmRunServe
from digitalhub_runtime_tvm.entities.run.serve.spec import RunSpecTvmRunServe, RunValidatorTvmRunServe
from digitalhub_runtime_tvm.entities.run.serve.status import RunStatusTvmRunServe


class RunTvmRunServeBuilder(RunBuilder, RuntimeEntityBuilderTvm):
    """
    RunTvmRunServeBuilder runner.
    """

    ENTITY_CLASS = RunTvmRunServe
    ENTITY_SPEC_CLASS = RunSpecTvmRunServe
    ENTITY_SPEC_VALIDATOR = RunValidatorTvmRunServe
    ENTITY_STATUS_CLASS = RunStatusTvmRunServe
    ENTITY_KIND = EntityKinds.RUN_TVM_SERVE.value
