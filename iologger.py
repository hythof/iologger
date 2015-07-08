# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import datetime
import traceback


class Trace(object):
    def __init__(self, filters):
        self.filters = filters
        self.nodes = []
        self.stack = []

    def write(self, out, stack_search):
        def puts(x):
            out(x)
            out('\n')

        for node in self.nodes:
            if node.is_valid:
                node.write(puts)
                if stack_search:
                    self._write_stack(puts, node, stack_search)

    def _write_stack(self, puts, node, stack_search):
        def search(frame):
            (path, line, _, code) = frame  # _ is function name
            s = '{}:{} {}'.format(path, line, code)
            return stack_search.search(s)

        frames = [x for x in node.stack if search(x)]
        if frames:
            size = max([1 + len(x[0]) + len(str(x[1])) for x in frames])
            for frame in frames:
                (path, line, func, code) = frame
                fmt = '    {:<' + str(size) + '} | {}'
                puts(fmt.format(path + ':' + str(line), code))

    def clear(self):
        del self.nodes[:]
        del self.stack[:]

    def run(self, frame, event, arg):
        if event == 'c_call' or event == 'c_return':
            return

        for f in self.filters:
            if not f.is_target(frame):
                continue
            if event == 'call':
                stacktrace = traceback.extract_stack()[:-1]  # hide this func
                node = Node(frame, f.write, stacktrace)
                self.nodes.append(node)
                self.stack.append(node)
            if event == 'return':
                if self.stack:
                    self.stack.pop().call_return(frame, arg)


class Node(object):
    def __init__(self, frame, formatter, stack):
        self.start_at = datetime.datetime.now()
        self.stack = stack
        self.indent = len(stack)
        self.msec = 0
        self.frame1 = frame
        self._formatter = formatter
        self.is_valid = False

    def call_return(self, frame, ret):
        self.frame2 = frame
        self.ret = ret
        self.msec = (datetime.datetime.now() - self.start_at).microseconds
        self.is_valid = True

    def write(self, puts):
        self._formatter(self, puts)
