# -*- coding: utf-8 -*-
import functools
import logging

from tinyq.exceptions import TaskNameConflictError
from tinyq.job import Job
from tinyq.utils import gen_task_name_via_func

logger = logging.getLogger(__name__)
_task_names = {}


class Task:
    def __init__(self, schedule_queue):
        self.queue = schedule_queue

    def __call__(self, name=None):
        def wrapper(func, name=name):
            # 注册 task name
            if not name:
                name = gen_task_name_via_func(func)
            if name in _task_names:
                raise TaskNameConflictError(name)
            _task_names[name] = func

            delay_wrapper = DelayWrapper(self.queue, func)
            return functools.wraps(func)(delay_wrapper)

        return wrapper


class DelayWrapper:
    """装饰函数，增加 delay 方法"""
    def __init__(self, schedule_queue, func):
        self.queue = schedule_queue
        self.func = func

    def delay(self, *args, **kwargs):
        logger.debug(
            'Delay func({func!r}) with: args({args!r}), '
            'kwargs({kwargs!r})'.format(
                func=self.func, args=args, kwargs=kwargs
            )
        )
        job = Job(func=self.func, func_args=args, func_kwargs=kwargs)
        job_data = job.dumps()
        self.queue.enqueue(job_data)
        return job

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def get_func_via_task_name(name):
    return _task_names[name]
