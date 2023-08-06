import asyncio
from abc import ABCMeta, abstractmethod
from asyncio import Future

from aioprocessing import AioProcess
from web_foundation.kernel.messaging.channel import IChannel


class Isolate(metaclass=ABCMeta):
    _name: str
    _channel: IChannel
    _proc: AioProcess
    _created = False

    @property
    def name(self):
        return self._name

    @property
    def created(self):
        return self._created

    def _configure_isolate(self, name: str):
        self._name = name
        self._proc = AioProcess(target=self._startup)
        self._channel = IChannel(self._name)
        self._created = True

    async def _run(self):
        await self.run()

    @abstractmethod
    async def run(self):
        pass

    @abstractmethod
    async def close(self):
        pass

    async def _close(self):
        await self.close()

    def _startup(self):
        asyncio.run(self._run())
        asyncio.run(self._close())

    async def _exec(self):
        self._proc.start()

    def perform(self) -> Future:
        if not self._created:
            raise AttributeError("Call configure_isolate() before start perform")
        return asyncio.ensure_future(self._exec())

    @property
    def channel(self) -> IChannel:
        return self._channel

    @property
    def pid(self) -> int:
        return self._proc.pid

    @property
    def process(self) -> AioProcess:
        return self._proc

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}) on pid: {self.pid}"
