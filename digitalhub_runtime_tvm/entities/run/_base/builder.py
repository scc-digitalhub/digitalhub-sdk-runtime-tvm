# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import typing

from digitalhub.entities._mixin.runtime_entity.builder import EntityError
from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.run._base.entity import RunTvmRun


class RunTvmRunBuilder(RunBuilder, RuntimeEntityBuilderTvm):
    """
    RunTvmRunBuilder runner.
    """

    def build(
        self,
        project: str,
        kind: str,
        name: str | None = None,
        uuid: str | None = None,
        extensions: list[dict] | None = None,
        labels: list[str] | None = None,
        task: str | None = None,
        model: str | None = None,
        local_execution: bool = False,
        **kwargs,
    ) -> RunTvmRun:
        """
        Create a new object.
        """
        # Check task validity
        if task is None:
            raise EntityError("Missing task in run spec")
        if model is None:
            raise EntityError("Missing model in run spec")

        self._check_kind_validity(task)

        uuid = self.build_uuid(uuid)
        metadata = self.build_metadata(
            project=project,
            name=name,
            labels=labels,
        )
        if name is None:
            name = metadata.name
        spec = self.build_spec(
            task=task,
            model=model,
            local_execution=local_execution,
            **kwargs,
        )
        status = self.build_status()
        return self.build_entity(
            project=project,
            name=name,
            uuid=uuid,
            kind=kind,
            metadata=metadata,
            spec=spec,
            status=status,
            extensions=extensions,
        )
