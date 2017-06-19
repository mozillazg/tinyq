# -*- coding: utf-8 -*-
import copy
import logging
import pickle
import uuid

from tinyq.exceptions import (
    SerializeError, DeserializeError,
    JobFailedError
)
from tinyq.utils import gen_task_name_via_func

logger = logging.getLogger(__name__)


class Job:
    def __init__(self, func, func_args, func_kwargs, id=None):
        self._func = func
        self._func_args = func_args
        self._func_kwargs = func_kwargs
        self._task_name = gen_task_name_via_func(func)
        self._id = id or self._gen_id()

    @property
    def id(self):
        return self._id

    @property
    def task_name(self):
        return self._task_name

    def run(self):
        try:
            return self._func(*self._func_args, **self._func_kwargs)
        except Exception as e:
            raise JobFailedError(self) from e

    def dumps(self):
        obj = copy.deepcopy(self)
        obj._func = None
        try:
            return pickle.dumps(obj)
        except Exception as e:
            raise SerializeError(self) from e

    @staticmethod
    def loads(data):
        from tinyq.task import get_func_via_task_name
        try:
            obj = pickle.loads(data)
        except Exception as e:
            raise DeserializeError(data) from e

        obj._func = get_func_via_task_name(obj._task_name)
        return obj

    @staticmethod
    def _gen_id():
        return str(uuid.uuid4())

    def __str__(self):
        return '<Job: id: {id}, task_name: {task_name}>'.format(
            id=self.id, task_name=self.task_name
        )

    def __repr__(self):
        return (
            '<Job: id: {id}, task_name: {task_name}, '
            'args: {args!r}, kwargs: {kwargs!r}>'.format(
                id=self.id, task_name=self.task_name, args=self._func_args,
                kwargs=self._func_kwargs)
        )
