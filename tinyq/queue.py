# -*- coding: utf-8 -*-
from redis import StrictRedis


class RedisQueue:
    key_prefix = 'tinyq'

    def __init__(self, uri_or_instance, key):
        if isinstance(uri_or_instance, StrictRedis):
            self.connection = uri_or_instance
        else:
            self.connection = StrictRedis.from_url(uri_or_instance)
        self.key = '{prefix}:{key}'.format(prefix=self.key_prefix, key=key)

    def enqueue(self, data):
        """入队"""
        return self.connection.rpush(self.key, data)

    def dequeue(self):
        """出队"""
        return self.connection.lpop(self.key)
