# -*- coding: utf-8 -*-


class TinyQError(Exception):
    pass


class TaskNameConflictError(TinyQError):
    def __init__(self, name):
        super().__init__(name)

        self.name = name

    def __str__(self):
        return '<{cls_name}: Same name {task_name} already registered!'.format(
            cls_name=self.__class__.__name__, task_name=self.name
        )


class JobFailedError(TinyQError):
    def __init__(self, job):
        super().__init__(job)

        self.job = job

    def __str__(self):
        return '<{cls_name}: Run {job} failed!'.format(
            cls_name=self.__class__.__name__, job=self.job
        )


class SerializeError(TinyQError):
    def __init__(self, obj):
        super().__init__(obj)

        self.obj = obj

    def __str__(self):
        return '<{cls_name}: Can not serialize object: {obj}!'.format(
            cls_name=self.__class__.__name__, obj=repr(self.obj)
        )


class DeserializeError(TinyQError):
    def __init__(self, data):
        super().__init__(data)

        self.data = data

    def __str__(self):
        return '<{cls_name}: Can not deserialize data: {data}!'.format(
            cls_name=self.__class__.__name__, data=repr(self.data)
        )
