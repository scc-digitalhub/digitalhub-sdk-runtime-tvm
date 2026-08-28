# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecTvmBuild(TaskSpecFunction):
    """
    Tvm build task specifications.
    """

    def __init__(
        self,
        function: str,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        image: str | None = None,
        simplify: bool | None = None,
        target_opset: int | None = None,
        opset_override: int | None = None,
        strict_shape_inference: bool | None = None,
        data_prop: bool | None = None,
        keep_params_in_input: bool | None = None,
        sanitize_input_names: bool | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function=function,
            volumes=volumes,
            resources=resources,
            envs=envs,
            secrets=secrets,
            profile=profile,
            **kwargs,
        )
        self.image = image
        self.simplify = simplify
        self.target_opset = target_opset
        self.opset_override = opset_override
        self.strict_shape_inference = strict_shape_inference
        self.data_prop = data_prop
        self.keep_params_in_input = keep_params_in_input
        self.sanitize_input_names = sanitize_input_names


class TaskValidatorTvmBuild(TaskValidatorFunction):
    """
    Tvm build task validator.
    """

    image: str | None = None
    simplify: bool | None = None
    target_opset: int | None = None
    opset_override: int | None = None
    strict_shape_inference: bool | None = None
    data_prop: bool | None = None
    keep_params_in_input: bool | None = None
    sanitize_input_names: bool | None = None
