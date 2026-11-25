# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import ModelBuilder, ModelStatus

from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.model.tflite.entity import ModelTflite
from digitalhub_runtime_tvm.entities.model.tflite.spec import ModelSpecTflite


class ModelTfliteBuilder(ModelBuilder):
    """ModelTflite builder."""

    ENTITY_CLASS = ModelTflite
    ENTITY_SPEC_CLASS = ModelSpecTflite
    ENTITY_STATUS_CLASS = ModelStatus
    ENTITY_KIND = EntityKinds.MODEL_TFLITE.value
