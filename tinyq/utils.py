# -*- coding: utf-8 -*-
import importlib


def gen_task_name_via_func(func):
    """生成函数对象对应的 task name"""
    return '{name}'.format(name=func.__name__)


def import_object_from_path(path, default_obj_name='app'):
    """从定义的字符串信息中导入对象

    :param path: ``task.app``
    """
    module_name, obj_name = path.rsplit('.', 1)
    if not obj_name:
        obj_name = default_obj_name

    module = importlib.import_module(module_name)
    return getattr(module, obj_name)
