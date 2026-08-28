# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.models import CoreServiceType
from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction
from pydantic import Field


class TaskSpecTvmServe(TaskSpecFunction):
    """
    Tvm serve task specifications.
    """

    def __init__(
        self,
        function: str,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
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
            function=function,
            volumes=volumes,
            resources=resources,
            envs=envs,
            secrets=secrets,
            profile=profile,
            **kwargs,
        )
        self.model_path = model_path
        self.served_name = served_name
        self.image = image
        self.replicas = replicas
        self.workers = workers
        self.service_type = service_type
        self.service_name = service_name


class TaskValidatorTvmServe(TaskValidatorFunction):
    """
    Tvm serve task validator.
    """

    model_path: str | None = Field(default=None)
    served_name: str | None = Field(default=None)
    image: str | None = None
    replicas: int | None = Field(default=None, ge=0)
    workers: int | None = Field(default=None, ge=1)
    service_type: CoreServiceType | None = None
    service_name: str | None = None
