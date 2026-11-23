# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.spec import TaskSpecFunction

from digitalhub_runtime_tvm.entities._mixin.execution.spec import TvmBuildSpecMixin


class TaskSpecTvmBuild(TaskSpecFunction, TvmBuildSpecMixin):
    """Common task settings and TVM build options."""
