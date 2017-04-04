# -*- coding: utf-8 -*-
from tinyq.worker import SchedulerWorker, JobWorker


def test_scheduler_worker(app):
    schedule_queue = app.schedule_queue
    job_queue = app.job_queue
    worker = SchedulerWorker(schedule_queue, job_queue)

    @app.task()
    def count(x, y):
        return x + y

    count.delay(1, 3)
    assert len(schedule_queue.connection.keys(schedule_queue.key)) == 1
    assert len(job_queue.connection.keys(job_queue.key)) == 0
    assert worker.run_once()
    assert len(schedule_queue.connection.keys(schedule_queue.key)) == 0
    assert len(job_queue.connection.keys(job_queue.key)) == 1


def test_scheduler_worker_no_job(app, redis_instance):
    schedule_queue = app.schedule_queue
    job_queue = app.job_queue
    worker = SchedulerWorker(schedule_queue, job_queue)

    assert len(schedule_queue.connection.keys(schedule_queue.key)) == 0
    assert len(job_queue.connection.keys(job_queue.key)) == 0
    assert worker.run_once() is None
    assert len(schedule_queue.connection.keys(schedule_queue.key)) == 0
    assert len(job_queue.connection.keys(job_queue.key)) == 0


def test_job_worker(app):
    schedule_queue = app.schedule_queue
    job_queue = app.job_queue
    scheduler_worker = SchedulerWorker(schedule_queue, job_queue)
    job_worker = JobWorker(job_queue)

    @app.task()
    def count(x, y):
        return x + y

    count.delay(1, 3)
    assert len(job_queue.connection.keys(job_queue.key)) == 0
    assert scheduler_worker.run_once()
    assert len(job_queue.connection.keys(job_queue.key)) == 1
    assert job_worker.run_once() == 4
    assert len(job_queue.connection.keys(job_queue.key)) == 0


def test_job_worker_no_job(app):
    schedule_queue = app.schedule_queue
    job_queue = app.job_queue
    scheduler_worker = SchedulerWorker(schedule_queue, job_queue)
    job_worker = JobWorker(job_queue)
    assert len(job_queue.connection.keys(job_queue.key)) == 0
    scheduler_worker.run_once()
    assert len(job_queue.connection.keys(job_queue.key)) == 0
    assert job_worker.run_once() is None
    assert len(job_queue.connection.keys(job_queue.key)) == 0
