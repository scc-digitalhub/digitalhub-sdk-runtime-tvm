# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities._base.entity.spec import Spec
from digitalhub.entities.task._base.spec import TaskSpecFunction


class TvmBuildSpecMixin(Spec):
    image: str | None = None
    simplify: bool | None = None
    target_opset: int | None = None
    opset_override: int | None = None
    strict_shape_inference: bool | None = None
    data_prop: bool | None = None
    keep_params_in_input: bool | None = None
    sanitize_input_names: bool | None = None


class TaskSpecTvmBuild(TaskSpecFunction, TvmBuildSpecMixin):
    """Common task settings and TVM build options."""


class TaskValidatorTvmBuild(TaskSpecTvmBuild):
    """Compatibility name for the typed TVM build-task spec."""
