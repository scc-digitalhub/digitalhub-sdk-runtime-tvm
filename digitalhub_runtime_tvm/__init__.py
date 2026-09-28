# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from digitalhub_runtime_tvm.entities import entity_plugins
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds

entity_builders = tuple((plugin.kind, plugin.builder) for plugin in entity_plugins)

try:
    from digitalhub_runtime_tvm.runtimes.builder import RuntimeTvmBuilder

    runtime_kinds = (
        EntityKinds.FUNCTION_TVM,
        EntityKinds.TASK_TVM_BUILD,
        EntityKinds.TASK_TVM_COMPILE,
        EntityKinds.TASK_TVM_SERVE,
        EntityKinds.RUN_TVM_BUILD,
        EntityKinds.RUN_TVM_COMPILE,
        EntityKinds.RUN_TVM_SERVE,
    )
    runtime_builders = ((kind.value, RuntimeTvmBuilder) for kind in runtime_kinds)
except ImportError as e:
    from digitalhub.utils.logger.logger import get_logger

    logger = get_logger(__name__)
    logger.debug(f"Error importing runtime builders: {e}")
    runtime_builders = ()
