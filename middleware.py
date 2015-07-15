# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import sys
import os
import re
from django.conf import settings
from .iologger import Trace
from .filters import RedisFilter, MysqlFilter


_default_conf = {
    'filter': ['redis', 'mysql'],
    'output': sys.stdout.write,
}


class IOLoggerMiddleware(object):
    def __init__(self):
        conf = getattr(settings, 'IOLogger', _default_conf)
        filter_conf = conf['filter']

        filters = []
        if 'redis' in filter_conf:
            filters.append(RedisFilter())
        if 'mysql' in filter_conf:
            filters.append(MysqlFilter())

        self.trace = Trace(filters)
        self.output = conf['output']
        rule = os.environ.get('show_stack', False)
        if rule:
            self.show_stack = re.compile(rule)
        else:
            self.show_stack = None

    def process_request(self, request):
        sys.setprofile(self.trace.run)

    def process_response(self, request, response):
        self.output("-- {} {} {}\n".format(
            request.method,
            request.path,
            response.status_code
        ))
        self.trace.write(self.output, self.show_stack)
        self.trace.clear()
        sys.setprofile(None)
        return response
