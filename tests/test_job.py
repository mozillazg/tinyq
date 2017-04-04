# -*- coding: utf-8 -*-
import pytest

from tinyq.exceptions import (
    SerializeError, DeserializeError, JobFailedError, TinyQError
)
from tinyq.job import Job


def test_delay_new_job(app):
    @app.task()
    def count(x, y):
        return x + y

    job = count.delay(2, 3)

    assert job.id
    assert job.task_name == 'count'
    assert job.run() == 5

    new_job = job.loads(job.dumps())
    assert new_job._func is job._func
    assert new_job.run() == job.run()


def test_job_dumps_error(app):
    @app.task()
    def test(x):
        return x

    job = Job(lambda: 'test', lambda: 'hello', {})

    with pytest.raises(SerializeError):
        job.dumps()


def test_job_loads_error():

    with pytest.raises(DeserializeError):
        Job.loads('hello')


def test_run_job_failed():
    job = Job(lambda x: x + 1, lambda: 'hello', {})

    with pytest.raises(JobFailedError):
        job.run()

    with pytest.raises(TinyQError):
        job.run()
