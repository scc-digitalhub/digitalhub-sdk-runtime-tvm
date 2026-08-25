# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecTvmServe(TaskSpecFunction):
    """Tvm serve task specifications."""


class TaskValidatorTvmServe(TaskValidatorFunction):
    """Tvm serve task validator."""
