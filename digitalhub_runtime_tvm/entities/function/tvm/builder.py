# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.builder import FunctionBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.function.tvm.entity import FunctionTvm
from digitalhub_runtime_tvm.entities.function.tvm.spec import (
    FunctionSpecTvm,
    FunctionValidatorTvm,
)
from digitalhub_runtime_tvm.entities.function.tvm.status import FunctionStatusTvm


class FunctionTvmBuilder(FunctionBuilder, RuntimeEntityBuilderTvm):
    """
    FunctionTvm builder.
    """

    ENTITY_CLASS = FunctionTvm
    ENTITY_SPEC_CLASS = FunctionSpecTvm
    ENTITY_SPEC_VALIDATOR = FunctionValidatorTvm
    ENTITY_STATUS_CLASS = FunctionStatusTvm
    ENTITY_KIND = EntityKinds.FUNCTION_TVM.value
