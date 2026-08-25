# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.function._base.entity import Function

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.function.tvm.spec import FunctionSpecTvm
    from digitalhub_runtime_tvm.entities.function.tvm.status import FunctionStatusTvm


class FunctionTvm(Function):
    """
    FunctionTvm class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: FunctionSpecTvm
        self.status: FunctionStatusTvm
