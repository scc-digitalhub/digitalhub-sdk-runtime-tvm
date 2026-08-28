# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.models import CoreServiceType
from pydantic import Field

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun, RunValidatorTvmRun


class RunSpecTvmRunServe(RunSpecTvmRun):
    """
    Tvm serve run specifications.
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
        model_path: str | None = None,
        served_name: str | None = None,
        image: str | None = None,
        replicas: int | None = None,
        workers: int | None = None,
        service_type: str | None = None,
        service_name: str | None = None,
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
        self.model_path = model_path
        self.served_name = served_name
        self.image = image
        self.replicas = replicas
        self.workers = workers
        self.service_type = service_type
        self.service_name = service_name


class RunValidatorTvmRunServe(RunValidatorTvmRun):
    """
    Tvm serve run validator.
    """

    model_path: str | None = Field(default=None)
    served_name: str | None = Field(default=None)
    image: str | None = None
    replicas: int | None = Field(default=None, ge=0)
    workers: int | None = Field(default=None, ge=1)
    service_type: CoreServiceType | None = None
    service_name: str | None = None
