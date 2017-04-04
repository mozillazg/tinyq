# -*- coding: utf-8 -*-


def test_app_delay(app):

    @app.task()
    def count(x, y):
        return x + y

    count.delay(1, 2)
    assert len(app.schedule_queue.connection.keys('*')) == 1
    assert app.schedule_queue.dequeue()


def test_app_call(app):

    @app.task()
    def count(x, y):
        return x + y

    assert count(1, 2) == 3
    assert len(app.schedule_queue.connection.keys('*')) == 0
