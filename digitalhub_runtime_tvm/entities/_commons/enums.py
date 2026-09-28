# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class EntityKinds(Enum):
    """
    Entity kinds.
    """

    MODEL_ONNX = "onnx"
    MODEL_TFLITE = "tflite"
    MODEL_TVM_IR = "tvm-ir"
    MODEL_TVM_SO = "tvm-so"
    FUNCTION_TVM = "tvm"
    TASK_TVM_BUILD = "tvm+build"
    TASK_TVM_COMPILE = "tvm+compile"
    TASK_TVM_SERVE = "tvm+serve"
    RUN_TVM_BUILD = "tvm+build:run"
    RUN_TVM_COMPILE = "tvm+compile:run"
    RUN_TVM_SERVE = "tvm+serve:run"


class Actions(Enum):
    """
    Task actions.
    """

    BUILD = "build"
    COMPILE = "compile"
    SERVE = "serve"
