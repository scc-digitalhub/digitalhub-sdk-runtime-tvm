# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.model._base.builder import ModelBuilder
from digitalhub.entities.model._base.status import ModelStatus

from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.model.onnx.entity import ModelOnnx
from digitalhub_runtime_tvm.entities.model.onnx.spec import ModelSpecOnnx


class ModelOnnxBuilder(ModelBuilder):
    """ModelOnnx builder."""

    ENTITY_CLASS = ModelOnnx
    ENTITY_SPEC_CLASS = ModelSpecOnnx
    ENTITY_STATUS_CLASS = ModelStatus
    ENTITY_KIND = EntityKinds.MODEL_ONNX.value
