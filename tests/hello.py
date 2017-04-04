# -*- coding: utf-8 -*-
from .conftest import redis_uri
from tinyq.app import Application

app = Application(redis_uri)


@app.task()
def hello(x, y):
    return x + y
