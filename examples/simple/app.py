# -*- coding: utf-8 -*-
from tinyq import Application

app = Application()


@app.task()
def add(m, n):
    return m + n


if __name__ == '__main__':
    for m in range(10):
        for n in range(3):
            add.delay(m, n)
