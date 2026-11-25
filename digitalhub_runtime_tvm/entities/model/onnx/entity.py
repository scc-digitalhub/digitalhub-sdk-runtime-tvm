# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.plugins import Model

if typing.TYPE_CHECKING:
    from digitalhub.plugins import ModelStatus

    from digitalhub_runtime_tvm.entities.model.onnx.spec import ModelSpecOnnx


class ModelOnnx(Model):
    """ModelOnnx class."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: ModelSpecOnnx
        self.status: ModelStatus
