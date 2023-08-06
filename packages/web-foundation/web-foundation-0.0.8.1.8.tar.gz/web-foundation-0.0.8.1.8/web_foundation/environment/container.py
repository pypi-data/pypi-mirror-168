from __future__ import annotations

from pathlib import Path
from typing import Generic, TypeVar

from pydantic import BaseSettings

from web_foundation.environment.resources.file_repo.repo import FileRepository
from web_foundation.environment.resources.file_repo.system_repo import SystemFileRepository
from web_foundation.environment.resources.stores.memory import InMemoryDictStore
from web_foundation.environment.resources.stores.store import AppStore
from web_foundation.environment.services.service import Service
from web_foundation.kernel.abstract.container import AbstractDependencyContainer, Dependency
from web_foundation.kernel.abstract.resource import Resource
from web_foundation.kernel.configuration import GenericConfig
from web_foundation.utils.helpers import in_obj_subclasses, in_obj_classes, in_obj_cls_items


class AppDependencyContainer(AbstractDependencyContainer, Generic[GenericConfig]):
    app_config: Dependency[GenericConfig] = Dependency(instance_of=BaseSettings)
    store: Dependency[AppStore] = Dependency(instance_of=AppStore, default=InMemoryDictStore())
    file_repository: Dependency[FileRepository] = Dependency(instance_of=FileRepository,
                                                             default=SystemFileRepository(root=Path("applied_files")))

    async def init_resources(self):
        for resource, name in in_obj_subclasses(self, Resource):
            await resource.init(self.app_config())

    async def shutdown_resources(self):
        for resource, name in in_obj_subclasses(self, Resource):
            await getattr(self, name).shutdown()

    def services(self):
        return set(in_obj_subclasses(self, Service))


GenericAppDepContainer = TypeVar("GenericAppDepContainer", bound=AppDependencyContainer)
