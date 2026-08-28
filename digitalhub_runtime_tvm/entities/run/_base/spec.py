# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.run._base.spec import RunSpec, RunValidator

from digitalhub_runtime_tvm.entities.function.tvm.spec import TvmFormat


class RunSpecTvmRun(RunSpec):
    """
    Tvm run specifications.
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
        format: TvmFormat | None = None,
        ir_model: str | None = None,
        so_model: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            task=task,
            function=function,
            workflow=workflow,
            volumes=volumes,
            resources=resources,
            envs=envs,
            secrets=secrets,
            profile=profile,
            **kwargs,
        )
        self.model = model
        self.inputs = inputs if inputs is not None else {}
        self.format = format
        self.ir_model = ir_model
        self.so_model = so_model


class RunValidatorTvmRun(RunValidator):
    """
    Tvm run validator.
    """

    model: str
    inputs: dict[str, str] | None = None
    format: TvmFormat | None = None
    ir_model: str | None = None
    so_model: str | None = None
