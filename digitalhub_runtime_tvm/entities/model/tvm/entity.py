# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.model._base.entity import Model

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.model.tvm.spec import ModelSpecTvm
    from digitalhub_runtime_tvm.entities.model.tvm.status import ModelStatusTvm


class ModelTvm(Model):
    """Shared base entity for TVM models."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: ModelSpecTvm
        self.status: ModelStatusTvm
