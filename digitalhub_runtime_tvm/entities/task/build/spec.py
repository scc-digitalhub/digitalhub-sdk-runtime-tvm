# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecTvmBuild(TaskSpecFunction):
    """Common build task settings; TVM options belong to the run."""


class TaskValidatorTvmBuild(TaskValidatorFunction):
    """Tvm build task validator."""
