# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecTvmCompile(TaskSpecFunction):
    """Common compile task settings; TVM options belong to the run."""


class TaskValidatorTvmCompile(TaskValidatorFunction):
    """Tvm compile task validator."""
