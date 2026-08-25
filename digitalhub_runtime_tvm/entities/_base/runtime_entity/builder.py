# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._commons.utils import map_actions
from digitalhub.entities._mixin.runtime_entity.builder import RuntimeEntityBuilder

from digitalhub_runtime_tvm.entities._commons.enums import Actions, EntityKinds


class RuntimeEntityBuilderTvm(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_TVM.value
    TASKS_KINDS = map_actions(
        [
            (
                EntityKinds.TASK_TVM_BUILD.value,
                Actions.BUILD.value,
            ),
            (
                EntityKinds.TASK_TVM_COMPILE.value,
                Actions.COMPILE.value,
            ),
            (
                EntityKinds.TASK_TVM_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )
    RUN_KINDS = map_actions(
        [
            (
                EntityKinds.RUN_TVM_BUILD.value,
                Actions.BUILD.value,
            ),
            (
                EntityKinds.RUN_TVM_COMPILE.value,
                Actions.COMPILE.value,
            ),
            (
                EntityKinds.RUN_TVM_SERVE.value,
                Actions.SERVE.value,
            ),
        ]
    )
