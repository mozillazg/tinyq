# -*- coding: utf-8 -*-
import os

import pytest
import redis

from tinyq.app import Application
from tinyq import task

redis_uri = os.environ['TINYQ_TESTING_REDIS_URI']


@pytest.fixture()
def app():
    instance = redis.StrictRedis.from_url(redis_uri)
    app = Application(instance)
    yield app
    instance.flushdb()
    task._task_names.clear()


@pytest.fixture()
def redis_instance():
    instance = redis.StrictRedis.from_url(redis_uri)
    yield instance
    instance.flushdb()
