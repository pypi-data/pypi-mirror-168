from __future__ import annotations

import asyncio
import datetime
import os
import uuid
from dataclasses import dataclass, field
from functools import partial
from inspect import iscoroutine, iscoroutinefunction, isawaitable
from time import time_ns
from typing import Dict, Callable, Coroutine, Any, TypeVar, Generic

import loguru
from apscheduler.events import EVENT_JOB_SUBMITTED, JobSubmissionEvent, JobExecutionEvent, \
    EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.executors.base import BaseExecutor
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.job import Job
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from pytz import utc

from web_foundation.kernel.abstract.container import GenericDepContainer
from web_foundation.kernel.worker import Worker

BackgroundTask = TypeVar("BackgroundTask", Callable[..., Coroutine[Any, Any, Any]], partial)


@dataclass
class Task:
    id: str
    status: str
    name: str
    scheduled_trigger: BaseTrigger
    scheduled_job: Job | None = field(default=None)
    on_error_callback: TaskErrorCallback = field(default=None)
    next_call_time: datetime.datetime | None = field(default=None)
    execution_time: float = field(default=0)
    done_time: float = field(default=0)
    call_time: float = field(default=0)
    call_counter: int = field(default=0)
    create_time: datetime.datetime | None = field(default_factory=datetime.datetime.now)
    error: BaseException | None = field(default=None)


TaskErrorCallback = Callable[[JobExecutionEvent, Task], Coroutine[Any, Any, None]]

from web_foundation.kernel import IMessage


class TaskIMessage(IMessage):
    message_type = "background_task"
    task: BackgroundTask
    args: Any | None
    kwargs: Any | None
    trigger: BaseTrigger
    add_job_kw: Dict
    on_error_callback: TaskErrorCallback

    def __init__(self, task: BackgroundTask,
                 trigger=None,
                 args: Any = None,
                 kwargs: Any | None = None,
                 add_job_kw: Dict = None,
                 on_error_callback: TaskErrorCallback = None):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self.add_job_kw = add_job_kw if add_job_kw else {}
        self.trigger = trigger
        self.on_error_callback = on_error_callback


class TaskExecutor(Worker, Generic[GenericDepContainer]):
    _tasks: Dict[str, Task]
    _scheduler: BackgroundScheduler

    def __init__(self, **kwargs):
        self._tasks = {}
        super().__init__(**kwargs)

    def _configure(self, *args, executors: Dict[str, BaseExecutor] = None, job_defaults=None, **kwargs):
        executor = {
            'default': ProcessPoolExecutor(os.cpu_count())
        }
        job_default = {
            "misfire_grace_time": 1,
            'coalesce': False,
            'max_instances': 10
        }
        self._scheduler = BackgroundScheduler(jobstores={"default": MemoryJobStore()},
                                              executors=executors if executors else executor,
                                              job_defaults=job_defaults if job_defaults else job_default,
                                              timezone=utc)
        self._add_listeners()

    async def _run(self):
        self.channel.add_event_listener(TaskIMessage, self._task_message_handler)
        self._scheduler.start()
        await self.channel.listen_consume()

    def _get_callable(self, fnc: BackgroundTask):
        caller = fnc
        if iscoroutine(fnc) or isawaitable(fnc):
            def __call(*args, **kwargs):
                loop = asyncio.get_running_loop()
                loop.run_until_complete(fnc)

            caller = __call

        elif iscoroutinefunction(fnc):
            def __call(*args, **kwargs):
                loop = asyncio.get_running_loop()
                loop.run_until_complete(fnc(*args, **kwargs))

            caller = __call

        return caller

    async def add_task(self, struct: TaskIMessage):
        await self._task_message_handler(struct)

    async def _task_message_handler(self, message: TaskIMessage):
        message.task = self._get_callable(message.task)
        arc_task = Task(id=str(uuid.uuid4()),
                        name=message.task.__name__,
                        status="new",
                        scheduled_trigger=message.trigger,
                        on_error_callback=message.on_error_callback)
        arc_task.scheduled_job = self._scheduler.add_job(message.task,
                                                         name=arc_task.name,
                                                         id=arc_task.id,
                                                         trigger=message.trigger,
                                                         args=message.args,
                                                         kwargs=message.kwargs,
                                                         **message.add_job_kw)
        arc_task.next_call_time = arc_task.scheduled_job.next_run_time
        self._tasks.update({arc_task.id: arc_task})

    def _get_task(self, id: str):
        return self._tasks.get(id)

    def _add_listeners(self):
        def _on_job_submitted(event: JobSubmissionEvent):
            nonlocal self
            task = self._get_task(event.job_id)
            task.call_time = time_ns()
            task.call_counter += 1
            task.status = "called"

        def _on_job_exec(event: JobExecutionEvent):
            nonlocal self
            task = self._get_task(event.job_id)
            task.done_time = time_ns()
            task.execution_time = task.done_time - task.call_time
            task.status = "done"
            task.next_call_time = task.scheduled_job.next_run_time
            if event.exception:
                task.error = event.exception
                task.status = 'error'
                if task.on_error_callback:
                    asyncio.create_task(task.on_error_callback(event, task))

        self._scheduler.add_listener(_on_job_submitted, EVENT_JOB_SUBMITTED)
        self._scheduler.add_listener(_on_job_exec, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    async def after_worker_fork(self):
        pass

    def post_configure(self):
        pass

    async def close(self, *args, **kwargs):
        self._scheduler.shutdown()
