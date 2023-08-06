from __future__ import annotations

import asyncio
from abc import ABC
from asyncio import Future
from typing import List, Dict, Any, Generic

from web_foundation import settings
from web_foundation.environment.metrics.dispatcher import MetricsDispatcher
from web_foundation.environment.resources.file_repo.repo import FileRepository
from web_foundation.environment.resources.stores.store import AppStore
from web_foundation.environment.services.service import Service
from web_foundation.kernel.abstract.container import GenericDepContainer
from web_foundation.kernel.configuration import GenericConfig
from web_foundation.kernel.messaging.dispatcher import IDispatcher
from web_foundation.kernel.worker import GenWorker, Worker


class AbstractApp(ABC, Generic[GenericDepContainer]):
    name: str
    workers: Dict[str, Worker]
    container: GenericDepContainer
    dispatcher: IDispatcher

    def __init__(self, container: GenericDepContainer):
        self.container = container
        self.workers = {}
        self.services = {}

    async def _before_app_run(self):
        pass

    async def before_app_run(self):
        pass

    def _add_worker(self, worker: GenWorker):
        pass

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
