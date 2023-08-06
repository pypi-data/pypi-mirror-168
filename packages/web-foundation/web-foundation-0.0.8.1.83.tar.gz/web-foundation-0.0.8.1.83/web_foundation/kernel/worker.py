from __future__ import annotations

from typing import TypeVar, Generic

from web_foundation import settings
from web_foundation.environment.events.settings import SettingsChange
from web_foundation.environment.metrics.mixin import MetricsMixin
from web_foundation.kernel.abstract.container import GenericDepContainer
from web_foundation.environment.resources.file_repo.repo import FileRepository
from web_foundation.environment.resources.stores.store import AppStore
from web_foundation.kernel import Isolate


class Worker(Isolate, MetricsMixin, Generic[GenericDepContainer]):
    _container: GenericDepContainer
    app_name: str
    _configured: bool
    _store: AppStore | None = None
    _repo: FileRepository | None = None

    def __init__(self, *args, **kwargs):
        self._configured = False

    @property
    def configured(self) -> bool:
        return self._configured

    def _configure(self, *args, **kwargs):
        raise NotImplementedError

    def configure(self, name: str, *args, **kwargs):
        self._configure_isolate(name)
        self._configure(*args, **kwargs)
        self.channel.add_event_listener(SettingsChange, self.on_settings_change)
        self._configured = True

    def post_configure(self):
        self._reg_metrics()
        self._post_configure()

    def _post_configure(self):
        raise NotImplementedError

    async def after_worker_fork(self):
        raise NotImplementedError

    async def _after_worker_fork(self):
        await self._container.init_resources()
        await self.after_worker_fork()

    async def run(self):
        pass

    async def on_settings_change(self, event: SettingsChange):
        setattr(settings, event.name, event.value)

    async def _run(self):
        await self._after_worker_fork()
        await self.run()

    async def close(self, *args, **kwargs):
        await self._container.shutdown_resources()

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, store: AppStore):
        store.channel = self.channel
        self._store = store

    @property
    def repo(self):
        return self._repo

    @repo.setter
    def repo(self, value: FileRepository):
        self._repo = value

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value: GenericDepContainer):
        self._container = value


GenWorker = TypeVar("GenWorker", bound=Worker)
