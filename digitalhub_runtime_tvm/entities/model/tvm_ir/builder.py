# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import ModelBuilder, ModelStatus

from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.model.tvm_ir.entity import ModelTvmIr
from digitalhub_runtime_tvm.entities.model.tvm_ir.spec import ModelSpecTvmIr


class ModelTvmIrBuilder(ModelBuilder):
    """ModelTvmIr builder."""

    ENTITY_CLASS = ModelTvmIr
    ENTITY_SPEC_CLASS = ModelSpecTvmIr
    ENTITY_STATUS_CLASS = ModelStatus
    ENTITY_KIND = EntityKinds.MODEL_TVM_IR.value
