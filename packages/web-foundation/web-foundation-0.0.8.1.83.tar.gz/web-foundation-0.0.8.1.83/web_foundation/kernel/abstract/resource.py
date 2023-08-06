from abc import ABC
from typing import Generic, TypeVar

from web_foundation.kernel.configuration import GenericConfig


class Resource(ABC, Generic[GenericConfig]):
    async def init(self, config: GenericConfig, *args, **kwargs):
        pass

    async def shutdown(self, *args, **kwargs):
        pass


GenericResource = TypeVar("GenericResource", bound=Resource)
