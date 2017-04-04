tinyq
=====

|Build| |Coverage| |Pypi version|

A tiny job queue framework.


Install
----------

::

    pip install tinyq


Usage
-------

start redis server ::

    $ redis-server


app.py ::


    from tinyq import Application

    app = Application()


    @app.task()
    def add(m, n):
        return m + n


add jobs ::

    for m in range(10):
        for n in range(3):
            add.delay(m, n)

start worker ::

    $ tinyq -l info
    2017-03-12 21:27:12,322 - WARNING - tinyq.runner[line:73 thread:MainThread(140736379601856) process:MainProcess(15388)] - Starting TinyQ worker, version 0.1.0...
    2017-03-12 21:27:12,446 - INFO - tinyq.worker[line:65 thread:Worker-2(123145554059264) process:MainProcess(15388)] - Got a job: <Job: id: 9687d9dd-30f4-4920-bd0c-924e672d9794, task_name: add>
    2017-03-12 21:27:12,447 - INFO - tinyq.worker[line:67 thread:Worker-2(123145554059264) process:MainProcess(15388)] - Finish run job <Job: id: 9687d9dd-30f4-4920-bd0c-924e672d9794, task_name: add>
    2017-03-12 21:27:12,500 - INFO - tinyq.worker[line:65 thread:Worker-5(123145569824768) process:MainProcess(15388)] - Got a job: <Job: id: 315f4ead-cedb-4b7a-b3c6-d328b0152e35, task_name: add>
    2017-03-12 21:27:12,501 - INFO - tinyq.worker[line:67 thread:Worker-5(123145569824768) process:MainProcess(15388)] - Finish run job <Job: id: 315f4ead-cedb-4b7a-b3c6-d328b0152e35, task_name: add>
    2017-03-12 21:27:12,610 - INFO - tinyq.worker[line:65 thread:Worker-1(123145548804096) process:MainProcess(15388)] - Got a job: <Job: id: a014ee87-0200-4b78-af25-6fe8dcca3f14, task_name: add>
    2017-03-12 21:27:12,610 - INFO - tinyq.worker[line:67 thread:Worker-1(123145548804096) process:MainProcess(15388)] - Finish run job <Job: id: a014ee87-0200-4b78-af25-6fe8dcca3f14, task_name: add>
    ^C2017-03-12 21:27:13,863 - WARNING - tinyq.runner[line:144 thread:MainThread(140736379601856) process:MainProcess(15388)] - Received stop signal, warm shutdown...
    2017-03-12 21:27:13,886 - WARNING - tinyq.runner[line:135 thread:Worker-2(123145554059264) process:MainProcess(15388)] - Exit worker Worker-2.
    2017-03-12 21:27:13,896 - WARNING - tinyq.runner[line:135 thread:Worker-7(123145580335104) process:MainProcess(15388)] - Exit worker Worker-7.
    2017-03-12 21:27:13,906 - WARNING - tinyq.runner[line:135 thread:Scheduler(123145538293760) process:MainProcess(15388)] - Exit worker Scheduler.
    2017-03-12 21:27:13,924 - WARNING - tinyq.runner[line:135 thread:Worker-5(123145569824768) process:MainProcess(15388)] - Exit worker Worker-5.
    2017-03-12 21:27:13,936 - WARNING - tinyq.runner[line:135 thread:Worker-0(123145543548928) process:MainProcess(15388)] - Exit worker Worker-0.
    2017-03-12 21:27:13,956 - WARNING - tinyq.runner[line:135 thread:Worker-4(123145564569600) process:MainProcess(15388)] - Exit worker Worker-4.
    2017-03-12 21:27:13,978 - WARNING - tinyq.runner[line:135 thread:Worker-6(123145575079936) process:MainProcess(15388)] - Exit worker Worker-6.
    2017-03-12 21:27:14,017 - WARNING - tinyq.runner[line:135 thread:Worker-1(123145548804096) process:MainProcess(15388)] - Exit worker Worker-1.
    2017-03-12 21:27:14,068 - WARNING - tinyq.runner[line:135 thread:Worker-3(123145559314432) process:MainProcess(15388)] - Exit worker Worker-3.
    2017-03-12 21:27:14,068 - WARNING - tinyq.runner[line:101 thread:MainThread(140736379601856) process:MainProcess(15388)] - Exit workers.
    $

.. |Build| image:: https://img.shields.io/travis/mozillazg/tinyq/master.svg
   :target: https://travis-ci.org/mozillazg/tinyq
.. |Coverage| image:: https://img.shields.io/coveralls/mozillazg/tinyq/master.svg
   :target: https://coveralls.io/r/mozillazg/tinyq
.. |PyPI version| image:: https://img.shields.io/pypi/v/tinyq.svg
   :target: https://pypi.python.org/pypi/tinyq
