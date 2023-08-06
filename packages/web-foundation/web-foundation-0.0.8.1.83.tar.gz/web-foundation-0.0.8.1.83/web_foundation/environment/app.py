from __future__ import annotations

import asyncio
import json
from asyncio import Future
from pathlib import Path
from typing import List, Type, Generic, Dict, Any

from web_foundation import settings
from web_foundation.environment.container import GenericAppDepContainer
from web_foundation.kernel.abstract.app import AbstractApp
from web_foundation.kernel.abstract.container import GenericDepContainer
from web_foundation.kernel.configuration import GenericConfig
from web_foundation.environment.metrics.dispatcher import MetricsDispatcher
from web_foundation.environment.resources.file_repo.repo import FileRepository
from web_foundation.environment.resources.stores.store import AppStore
from web_foundation.environment.services.service import Service
from web_foundation.kernel.messaging.dispatcher import IDispatcher
from web_foundation.kernel.worker import GenWorker, Worker


class App(AbstractApp, Generic[GenericAppDepContainer]):
    name: str
    workers: Dict[str, Worker]
    services: Dict[str, Service]
    dispatcher: IDispatcher
    container: GenericAppDepContainer

    # debug: bool  # type: ignore

    def __init__(self, container: GenericAppDepContainer):
        super().__init__(container)
        self.name = container.app_config().app_name
        self.dispatcher = MetricsDispatcher() if settings.METRICS_ENABLE else IDispatcher()

    async def _before_app_run(self):
        await self.container.init_resources()
        await self.before_app_run()
        await self.container.shutdown_resources()

    async def before_app_run(self):
        pass

    def _add_worker(self, worker: GenWorker):
        if not worker.configured:
            raise RuntimeError("Worker not configured")
        worker.store = self.container.store()
        worker.repo = self.container.file_repository()
        worker.app_name = self.name
        worker.container = self.container
        self.dispatcher.reg_worker(worker)
        worker.post_configure()
        self.workers.update({worker.name: worker})

    def add_worker(self, worker: GenWorker | List[GenWorker]):
        """
        Set isolate to environment and set isolate debug and name
        :param worker: isolate to apply
        :return: None
        """
        if isinstance(worker, list):
            for w in worker:
                self._add_worker(w)
        else:
            self._add_worker(worker)

    def add_service(self, service: Service):
        self.services.update({service.__class__.__name__: service})

    def find_worker_by_pid(self, pid: int):
        for worker in self.workers.values():
            if worker.pid == pid:
                return worker

    def perform(self) -> List[Future[Any]]:
        """
        Call performs from isolates and return all isolates Futures
        :return: None
        """
        return [worker.perform() for worker in self.workers.values()]

    async def run(self):
        await self._before_app_run()
        """
        Func to run environment manually (without Runner)
        :return: None
        """
        return await asyncio.wait(self.perform() + self.dispatcher.preform())
