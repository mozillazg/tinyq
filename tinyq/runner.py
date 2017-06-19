# -*- coding: utf-8 -*-
import argparse
from multiprocessing import cpu_count, current_process
import logging
import os
import signal
import sys

from tinyq import __version__
from tinyq.worker import (
    SchedulerWorker, JobWorker, ThreadWorkerCreator
)
from tinyq.task import _task_names
from tinyq.utils import import_object_from_path

logger = logging.getLogger(__name__)


def setup_logging(args_obj):
    if args_obj.verbose:
        level = logging.DEBUG
    else:
        level = logging.getLevelName(args_obj.log_level.upper())
    formatter = logging.Formatter(
        fmt='%(asctime)-15s - %(levelname)s - %(name)s'
            '[line:%(lineno)d thread:%(threadName)s(%(thread)d) '
            'process:%(processName)s(%(process)d)]'
            ' - %(message)s'
    )

    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def parse_args(args):
    parser = argparse.ArgumentParser(description='Starts a TinyQ worker.')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-u', '--uri', default='redis://',
                        help='The Redis URI (default: redis://)')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Show more output')
    parser.add_argument('-w', '--worker-number', type=int, default=cpu_count(),
                        help='Worker number (default: {0})'.format(cpu_count())
                        )
    parser.add_argument('-a', '--app', default='app.app',
                        help='Application path (default: app.app)')
    parser.add_argument('-l', '--log-level', default='warn',
                        choices=('debug', 'info', 'warn', 'error', 'critical'),
                        help='Logging level (default: warn)')
    return parser.parse_args(args)


class Worker:
    def __init__(self, schedule_queue, job_queue, worker_creator,
                 worker_number=1, schedule_sleep_interval=0.1,
                 worker_sleep_interval=0.1,
                 main_stop_flag_timeout=0.1):
        self.schedule_queue = schedule_queue
        self.job_queue = job_queue
        self.scheduler_sleep_interval = schedule_sleep_interval
        self.worker_sleep_interval = worker_sleep_interval
        self.worker_creator = worker_creator()
        self.worker_number = worker_number
        self.received_stop = False
        self.main_stop_flag_timeout = main_stop_flag_timeout
        self.process_list = [current_process()]

    def start(self):  # pragma: nocover
        logger.warn('Starting TinyQ worker, version {0}...'.format(__version__)
                    )
        logger.debug('Task names:\n{0}'.format(
            '\n'.join('* ' + name for name in _task_names)
        ))
        self.start_works()
        self.setup_signal_handlers()

        while True:
            try:
                self.worker_creator.stop_flag.wait(self.main_stop_flag_timeout)
            except KeyboardInterrupt:
                logger.warn('Received Ctrl + C, warm shutdown...')
                self.stop()
            except:
                logger.exception('Got exception, will exit worker')
                self.stop()
            else:
                if self.received_stop:
                    self.stop()

            if self.worker_creator.is_stopped():
                for process in self.process_list[1:]:
                    if self.worker_creator.is_alive(process):
                        break
                else:
                    break

        logger.warn('Exit workers.')

    def start_works(self):
        logger.debug('Create scheduler worker.')
        scheduler = SchedulerWorker(
            self.schedule_queue, self.job_queue,
            sleep_interval=self.scheduler_sleep_interval
        )
        scheduler_process = self.create_process(scheduler, name='Scheduler')
        self.process_list.append(scheduler_process)

        logger.debug('Create job workers.')
        job_worker_process_list = []
        job_worker = JobWorker(self.job_queue,
                               sleep_interval=self.worker_sleep_interval)
        for n in range(self.worker_number):
            process = self.create_process(job_worker,
                                          name='Worker-{0}'.format(n))
            job_worker_process_list.append(process)
            self.process_list.append(process)

        logger.debug('Start scheduler worker...')
        scheduler_process.start()
        logger.debug('Start job workers...')
        for worker in job_worker_process_list:
            worker.start()

    def create_process(self, worker, name):
        def func():
            try:
                logger.debug('Started worker: {0}'.format(name))
                while not self.worker_creator.is_stopped():
                    worker.run_once()
                    worker.sleep()
                logger.warn('Exit worker {0}.'.format(name))
            except KeyboardInterrupt:
                pass
            except:
                logger.exception('Worker {0} dead!'.format(name))
        return self.worker_creator.create(func, name)

    def setup_signal_handlers(self):
        def stop_process(signum, frame):
            logger.warn('Received stop signal, warm shutdown...')
            self.received_stop = True

        signal.signal(signal.SIGINT, stop_process)
        signal.signal(signal.SIGTERM, stop_process)

    def stop(self):
        self.worker_creator.set_stop()


def get_app(app_path):
    try:
        app = import_object_from_path(app_path)
        return app
    except (ImportError, AttributeError):
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
            return get_app(app_path)
        else:
            raise ImportError(
                'Import App object from path "{0}" failed!'.format(app_path)
            )


def main(args=None, start_now=True):
    args_obj = parse_args(args)
    app_path = args_obj.app
    app = get_app(app_path)
    setup_logging(args_obj)

    worker = Worker(app.schedule_queue, app.job_queue,
                    worker_creator=ThreadWorkerCreator,
                    worker_number=args_obj.worker_number)
    if start_now:
        worker.start()
        return

    return worker


if __name__ == '__main__':
    main()
