# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecTvmServe(TaskSpecFunction):
    """Common serve task settings; TVM options belong to the run."""


class TaskValidatorTvmServe(TaskValidatorFunction):
    """Tvm serve task validator."""
