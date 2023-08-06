from typing import Generic, TypeVar, Dict

from apscheduler.triggers.base import BaseTrigger

from web_foundation.environment.workers.background.worker import BackgroundTask, TaskErrorCallback, TaskIMessage
from web_foundation.kernel import IMessage
from web_foundation.kernel.worker import GenWorker


class Service(Generic[GenWorker]):
    _worker: GenWorker

    async def run_background(self, task: BackgroundTask,
                             *args,
                             trigger: BaseTrigger = None,
                             on_error_callback: TaskErrorCallback = None,
                             add_job_kw: Dict = None, return_event: bool = False, **kwargs,
                             ):
        await self.emmit_event(
            TaskIMessage(task,
                         trigger,
                         on_error_callback=on_error_callback,
                         add_job_kw=add_job_kw,
                         args=args,
                         kwargs=kwargs,
                         return_event=return_event))

    async def wait_for_response(self, msg: IMessage):
        return await self.worker.channel.produce_for_response(msg)

    @property
    def worker(self) -> GenWorker:
        return self._worker

    @worker.setter
    def worker(self, worker: GenWorker):
        self._worker = worker

    async def emmit_event(self, event: IMessage):
        await self.worker.channel.produce(event)


# async def microtask(self, task: Coroutine):
#     return asyncio.create_task(task)


GenericService = TypeVar("GenericService", bound=Service)
