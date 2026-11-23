# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.spec import TaskSpecFunction
from pydantic import ConfigDict


class TvmTaskSpec(TaskSpecFunction):
    """Shared task settings. Older snapshots can also contain run options."""

    model_config = ConfigDict(extra="ignore")
