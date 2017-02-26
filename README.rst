tinyq
=====

A tiny job queue framework.


Install
----------

::

    pip install tinyq


Usage
-------

启动一个 redis 服务 ::

    $ redis-server


app.py ::


    from tinyq import Application

    app = Application()


    @app.task()
    def add(m, n):
        return m + n


添加队列任务 ::

    for m in range(10):
        for n in range(3):
            add.delay(m, n)

启动 worker ::

    $ tinyq
    2017-02-19 22:58:50,676 - WARNING - runner - start - 72 - MainProcess - MainThread - Starting TinyQ worker, version 0.1.0...
    2017-02-19 22:58:51,796 - INFO - worker - run_once - 56 - MainProcess - Worker-6 - Got a job: <Job: id: 91eb9414-7d61-4234-8ab7-b691f0c4e390, task_name: add>
    2017-02-19 22:58:51,796 - INFO - worker - run_once - 58 - MainProcess - Worker-6 - Finish run job <Job: id: 91eb9414-7d61-4234-8ab7-b691f0c4e390, task_name: add>
    2017-02-19 22:58:51,931 - INFO - worker - run_once - 56 - MainProcess - Worker-2 - Got a job: <Job: id: 10e4751f-6832-45df-8910-465725cc250d, task_name: add>
    2017-02-19 22:58:51,931 - INFO - worker - run_once - 58 - MainProcess - Worker-2 - Finish run job <Job: id: 10e4751f-6832-45df-8910-465725cc250d, task_name: add>
    ^C2017-02-19 22:58:52,205 - WARNING - runner - start - 83 - MainProcess - MainThread - Warm shutdown...
    2017-02-19 22:58:52,205 - WARNING - runner - start - 94 - MainProcess - MainThread - Exit worker.
    2017-02-19 22:58:52,439 - WARNING - runner - func - 126 - MainProcess - Worker-5 - Exit worker Worker-5.
    2017-02-19 22:58:52,488 - WARNING - runner - func - 126 - MainProcess - Worker-0 - Exit worker Worker-0.
    2017-02-19 22:58:52,536 - WARNING - runner - func - 126 - MainProcess - Worker-3 - Exit worker Worker-3.
    2017-02-19 22:58:52,972 - WARNING - runner - func - 126 - MainProcess - Worker-2 - Exit worker Worker-2.
    2017-02-19 22:58:52,972 - WARNING - runner - func - 126 - MainProcess - Scheduler - Exit worker Scheduler.
    2017-02-19 22:58:53,192 - WARNING - runner - func - 126 - MainProcess - Worker-7 - Exit worker Worker-7.
    2017-02-19 22:58:53,542 - WARNING - runner - func - 126 - MainProcess - Worker-1 - Exit worker Worker-1.
    2017-02-19 22:58:53,720 - WARNING - runner - func - 126 - MainProcess - Worker-6 - Exit worker Worker-6.
    2017-02-19 22:58:53,917 - WARNING - runner - func - 126 - MainProcess - Worker-4 - Exit worker Worker-4.
    $
