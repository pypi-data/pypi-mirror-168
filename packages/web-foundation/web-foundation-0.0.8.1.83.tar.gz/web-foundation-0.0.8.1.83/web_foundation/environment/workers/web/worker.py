from __future__ import annotations

import asyncio
import copy
import os
import socket
from functools import partial
from typing import List, Callable, Any, Type, Generic

import orjson
from sanic import Sanic
from sanic.server.socket import bind_socket

from web_foundation.environment.metrics.mixin import ApiMetricsMixin
from web_foundation.environment.workers.web.ext.addons_loader import AddonsLoader
from web_foundation.environment.workers.web.ext.error_handler import ExtendedErrorHandler
from web_foundation.environment.workers.web.ext.router import ExtRouter
from web_foundation.environment.workers.web.realtime.rt_connection import RtConnection, RtEventCallback
from web_foundation.kernel import GenericIMessage, IMessage
from web_foundation.kernel.abstract.container import GenericDepContainer
from web_foundation.kernel.configuration import ServerConfig
from web_foundation.kernel.worker import Worker


class HttpServer(Worker, ApiMetricsMixin, Generic[GenericDepContainer]):
    config: ServerConfig
    sock: socket.socket
    sanic_app: Sanic
    router: ExtRouter | None
    rt_connections: List[RtConnection]
    api_addons_loader: AddonsLoader | None

    def __init__(self, config: ServerConfig, *args, **kwargs):
        super(HttpServer, self).__init__(*args, **kwargs)
        self.config = config

    def _configure(self, sock: socket.socket = None, ext_router: ExtRouter = None,
                   api_addons_loader: AddonsLoader = None):  # type: ignore
        self.sock = sock if sock else self.create_socket(self.config.host, self.config.port)
        self.router = copy.deepcopy(ext_router)
        self.sanic_app = Sanic(self.name, router=self.router, dumps=orjson.dumps, loads=orjson.loads)
        self.sanic_app.error_handler = ExtendedErrorHandler()
        self.sanic_app.after_server_stop(self.close)
        self.rt_connections = []
        self.api_addons_loader = api_addons_loader

    def _post_configure(self):
        self._set_sanic_confs()
        if self.api_addons_loader and not (self.repo or self.store):
            raise AttributeError(f"You need FileRepository and AppStore to use MiddlewareManager")
        if self.api_addons_loader and issubclass(self.api_addons_loader.__class__, AddonsLoader):
            self.api_addons_loader.store = self.store
            self.api_addons_loader.repo = self.repo
            self.api_addons_loader.reg_channel_middleware()

    def _set_sanic_confs(self):
        self.sanic_app.config.SWAGGER_UI_CONFIGURATION = {
            "docExpansion": 'none'
        }

    async def after_worker_fork(self):
        for service, name in self.container.services():
            service.worker = self

    async def _before_sanic(self, app, loop):
        await self._container.init_resources()
        await self._after_worker_fork()
        if self.api_addons_loader:
            await self.api_addons_loader.discover_middleware()
            await self.api_addons_loader.import_middleware()

        # noinspection PyAsyncCall
        self.sanic_app.add_task(self.channel.listen_consume())

    def _startup(self):
        if self.router and issubclass(self.router.__class__, ExtRouter):
            self.router.apply_routes(self.sanic_app, self.container, self.api_addons_loader)
        # noinspection PyAsyncCall
        self.sanic_app.before_server_start(self._before_sanic)
        # asyncio.run(self._run())
        try:
            self.sanic_app.run(sock=self.sock)
        except KeyboardInterrupt:
            self._close()

    @staticmethod
    def create_socket(host: str, port: int) -> socket.socket:
        sock = bind_socket(host, port)
        sock.set_inheritable(True)
        return sock

    async def broadcasts_rt(self, message: GenericIMessage, resolve_callback: RtEventCallback = None):
        promises = []
        for conn in self.rt_connections:
            if conn.resolve_callback.__name__ == resolve_callback.__name__:
                promises.append(conn.send_after_call(message))
        await asyncio.gather(*promises)

    async def accept_rt_connection(self, conn: RtConnection,
                                   on_disconnect_callback: Callable[[HttpServer, RtConnection], Any] | None = None):
        # conn.debug = self.debug if self.debug else conn.debug
        self.rt_connections.append(conn)

        async def _on_rt_close():
            nonlocal self
            nonlocal conn
            nonlocal on_disconnect_callback
            self.rt_connections.remove(conn)
            if on_disconnect_callback:
                await on_disconnect_callback(self, conn)

        await conn.freeze_request(_on_rt_close)


def create_io_workers(server_cls: Type[HttpServer],
                      config: ServerConfig,
                      router: ExtRouter,
                      api_addons_loader: AddonsLoader = None,
                      workers_num: int = 1,
                      fast: bool = False,
                      **kwargs
                      ) -> List[HttpServer]:
    """
    RESERVE 0 WORKER TO CREATE FRONT SERVICE SERVING
    """
    sock = HttpServer.create_socket(config.host,
                                    config.port)
    workers: List[HttpServer] = []
    w_num = workers_num
    if fast and workers_num != 1:
        raise RuntimeError("You cannot use both fast=True and workers=X")
    if fast:
        try:
            w_num = len(os.sched_getaffinity(0))
        except AttributeError:  # no cov
            w_num = os.cpu_count() or 1
    for i in range(w_num):
        worker = server_cls(config)
        worker.configure(f"web_worker_{i + 1}", ext_router=router, sock=sock,
                         api_addons_loader=api_addons_loader, **kwargs)
        workers.append(worker)
    return workers


def create_rt_subscribes(*workers: HttpServer,
                         event_type: List[Type[IMessage] | str] | Type[IMessage] | str,
                         resolve_callback: RtEventCallback,
                         **kwargs):
    for worker in workers:
        worker.channel.add_event_listener(event_type, partial(worker.broadcasts_rt, resolve_callback=resolve_callback),
                                          **kwargs)
