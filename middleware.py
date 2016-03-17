from __future__ import print_function
from __future__ import unicode_literals
import sys
import os
import re
from django.conf import settings
from .iologger import Trace
from .filters import RedisFilter, MysqlFilter


_default_conf = {
    'response': True,
    'filter': ['redis', 'mysql'],
    'output': sys.stdout.write,
}


def noop(*args, **kwargs):
    pass


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
        self.on_response = self.show_response if conf['response'] else noop
        rule = os.environ.get('show_stack', False)
        if rule:
            self.show_stack = re.compile(rule)
        else:
            self.show_stack = None

    def process_request(self, request):
        sys.setprofile(self.trace.run)

    def process_response(self, request, response):
        self.on_response(request, response)
        sys.setprofile(None)
        self.trace.write(self.write_with_indent, self.show_stack)
        self.trace.clear()
        return response

    def show_response(self, request, response):
        qs = request.META['QUERY_STRING']
        self.output("\n\n-- {} {}{} {}\n{}\n\n".format(
            request.method,
            request.path,
            "?" + qs if qs else "",
            response.status_code,
            response.content
        ))

    def write_with_indent(self, msg):
        self.output("    {}".format(msg))
