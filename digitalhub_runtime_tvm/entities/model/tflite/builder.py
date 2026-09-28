# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.model._base.builder import ModelBuilder

from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.model.tflite.entity import ModelTflite
from digitalhub_runtime_tvm.entities.model.tflite.spec import ModelSpecTflite, ModelValidatorTflite
from digitalhub_runtime_tvm.entities.model.tflite.status import ModelStatusTflite


class ModelTfliteBuilder(ModelBuilder):
    """ModelTflite builder."""

    ENTITY_CLASS = ModelTflite
    ENTITY_SPEC_CLASS = ModelSpecTflite
    ENTITY_SPEC_VALIDATOR = ModelValidatorTflite
    ENTITY_STATUS_CLASS = ModelStatusTflite
    ENTITY_KIND = EntityKinds.MODEL_TFLITE.value
