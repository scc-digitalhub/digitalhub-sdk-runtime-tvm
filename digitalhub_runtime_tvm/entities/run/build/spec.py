# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun, RunValidatorTvmRun


class RunSpecTvmRunBuild(RunSpecTvmRun):
    """
    Tvm build run specifications.
    """

    def __init__(
        self,
        task: str,
        model: str,
        function: str | None = None,
        workflow: str | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        inputs: dict[str, str] | None = None,
        format: str | None = None,
        ir_model: str | None = None,
        so_model: str | None = None,
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
            task=task,
            model=model,
            function=function,
            workflow=workflow,
            volumes=volumes,
            resources=resources,
            envs=envs,
            secrets=secrets,
            profile=profile,
            inputs=inputs,
            format=format,
            ir_model=ir_model,
            so_model=so_model,
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


class RunValidatorTvmRunBuild(RunValidatorTvmRun):
    """
    Tvm build run validator.
    """

    image: str | None = None
    simplify: bool | None = None
    target_opset: int | None = None
    opset_override: int | None = None
    strict_shape_inference: bool | None = None
    data_prop: bool | None = None
    keep_params_in_input: bool | None = None
    sanitize_input_names: bool | None = None
