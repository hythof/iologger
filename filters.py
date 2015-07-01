# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import re


class FilterBase(object):
    func = ''
    path = ''

    def is_target(self, frame):
        func = frame.f_code.co_name
        path = frame.f_code.co_filename
        return func == self.func and path.endswith(self.path)

    def show(self, v):
        try:
            return repr(v)
        except:
            return type(v).__name__

    def write(self, node, puts):
        raise NotImplementedError("FilterBase.write")


class RedisFilter(FilterBase):
    func = 'execute_command'
    path = 'redis/client.py'

    def write(self, node, puts):
        v = node.frame2.f_locals
        args = [str(x) for x in v['args']]
        puts('[redis] {} # {}'.format(' '.join(args), self.show(node.ret)))


class MysqlFilter(FilterBase):
    func = 'execute'
    path = 'MySQLdb/cursors.py'
    _sql_sub = re.compile(r'SELECT .*? FROM ')

    def write(self, node, puts):
        v = node.frame2.f_locals
        sql = self._sql_sub.sub('SELECT * FROM ', v['query'])
        puts('[mysql] {}'.format(sql))
