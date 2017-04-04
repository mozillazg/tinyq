# -*- coding: utf-8 -*-

import pytest

from tinyq import task
from tinyq.exceptions import TaskNameConflictError


def test_app_task_name_default(app):
    @app.task()
    def count(x, y):
        return x + y

    assert 'count' in task._task_names
    assert task.get_func_via_task_name('count')


def test_app_task_name_custom(app):
    @app.task(name='test')
    def count(x, y):
        return x + y

    assert 'test' in task._task_names
    assert task.get_func_via_task_name('test')


def test_app_task_name_error(app):
    @app.task()
    def count(): pass

    with pytest.raises(TaskNameConflictError):
        @app.task()   # noqa
        def count(): pass
