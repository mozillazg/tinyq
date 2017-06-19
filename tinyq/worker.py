# -*- coding: utf-8 -*-
import abc
import multiprocessing
import logging
import random
import threading
import time

from tinyq.exceptions import JobFailedError
from tinyq.job import Job

logger = logging.getLogger(__name__)


class BaseWorker(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run_once(self):
        pass

    @abc.abstractmethod
    def sleep(self):
        pass


class SchedulerWorker(BaseWorker):
    def __init__(self, schedule_queue, job_queue, sleep_interval=1):
        self.queue = schedule_queue
        self.job_queue = job_queue
        self.sleep_interval = sleep_interval

    def run_once(self):
        try:
            job = self._get_job()
            if job is not None:
                logger.debug('Schedule new job: {job}.'.format(job=job))
                return self._schedule_job(job)
        except:
            logger.exception('Raise an exception when schedule job!')

    def sleep(self):
        time.sleep(self.sleep_interval * (1 + random.SystemRandom().random()))

    def _get_job(self):
        data = self.queue.dequeue()
        if data is None:
            return

        return Job.loads(data)

    def _schedule_job(self, job):
        logger.debug('Put a new job({job}) into job queue.'.format(job=job))
        return self.job_queue.enqueue(job.dumps())


class JobWorker(BaseWorker):
    def __init__(self, job_queue, sleep_interval=1):
        self.queue = job_queue
        self.sleep_interval = sleep_interval

    def run_once(self):
        try:
            job = self._get_job()
            if job is not None:
                logger.info('Got a job: {job}'.format(job=job))
                result = self.run_job(job)
                logger.info('Finish run job {job}'.format(job=job))
                return result
        except:
            logger.exception('Raise an exception when run job!')

    def sleep(self):
        time.sleep(self.sleep_interval * (1 + random.SystemRandom().random()))

    def _get_job(self):
        data = self.queue.dequeue()
        if data is None:
            return

        return Job.loads(data)

    def run_job(self, job):
        logger.debug('Start run a job: {job}'.format(job=job))
        try:
            result = job.run()
            logger.debug('Run job({job!r}) success. Result: {result!r}'.format(
                         job=job, result=result))
            return result
        except JobFailedError as e:
            logger.exception('Run job {job} failed!'.format(job=job))


class BaseWorkerCreator(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, runnable, name):
        pass

    @abc.abstractmethod
    def set_stop(self):
        pass

    @abc.abstractmethod
    def is_stopped(self):
        pass

    @abc.abstractmethod
    def is_alive(self, process):
        pass


class ThreadWorkerCreator(BaseWorkerCreator):
    def __init__(self):
        self.stop_flag = threading.Event()

    def create(self, runnable, name):
        thread = threading.Thread(target=runnable, name=name)
        return thread

    def set_stop(self):
        self.stop_flag.set()

    def is_stopped(self):
        return self.stop_flag.is_set()

    def is_alive(self, process):
        return process.is_alive()


class ProcessWorkerCreator(BaseWorkerCreator):
    def __init__(self):
        self.stop_flag = multiprocessing.Event()

    def create(self, runnable, name):
        process = multiprocessing.Process(target=runnable, name=name)
        return process

    def set_stop(self):
        self.stop_flag.set()

    def is_stopped(self):
        return self.stop_flag.is_set()

    def is_alive(self, process):
        return process.is_alive()
