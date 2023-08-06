from __future__ import annotations

from abc import ABC
from typing import TypeVar

from web_foundation.kernel.abstract.dependency import Dependency
from web_foundation.utils.helpers import in_obj_classes


class AbstractDependencyContainer(ABC):
    def __init__(self, **kwargs):
        for dep, name in in_obj_classes(self, Dependency):
            dep_init = kwargs.get(name)
            if dep_init:
                dep.from_initialized(dep_init)

    async def init_resources(self):
        pass

    async def shutdown_resources(self):
        pass


GenericDepContainer = TypeVar("GenericDepContainer", bound=AbstractDependencyContainer)
