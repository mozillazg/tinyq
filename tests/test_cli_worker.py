# -*- coding: utf-8 -*-
from multiprocessing import Process
import os
import signal
import time

import pytest

from .hello import redis_uri
from tinyq.runner import main

args = ['--uri', redis_uri, '--app', 'tests.hello.app']


def test_worker_import_error():
    with pytest.raises(ImportError):
        main(args=[], start_now=False)


def test_worker():
    worker = main(args, start_now=False)
    worker.start_works()
    worker.setup_signal_handlers()
    assert len([p for p in worker.process_list if p.is_alive()]) == \
        worker.worker_number + 2
    worker.stop()
    time.sleep(1)

    assert len([p for p in worker.process_list if p.is_alive()]) == 1


def test_worker_sigint():
    worker = main(args, start_now=False)
    process = Process(target=worker.start)
    process.start()
    time.sleep(1)
    os.kill(process.pid, signal.SIGINT)


def test_worker_sigterm():
    worker = main(args, start_now=False)
    process = Process(target=worker.start)
    process.start()
    time.sleep(1)
    os.kill(process.pid, signal.SIGTERM)
