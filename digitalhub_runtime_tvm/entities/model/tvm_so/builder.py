# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import ModelBuilder, ModelStatus

from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.model.tvm_so.entity import ModelTvmSo
from digitalhub_runtime_tvm.entities.model.tvm_so.spec import ModelSpecTvmSo


class ModelTvmSoBuilder(ModelBuilder):
    """ModelTvmSo builder."""

    ENTITY_CLASS = ModelTvmSo
    ENTITY_SPEC_CLASS = ModelSpecTvmSo
    ENTITY_STATUS_CLASS = ModelStatus
    ENTITY_KIND = EntityKinds.MODEL_TVM_SO.value
