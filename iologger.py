# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import datetime


class Trace(object):
    def __init__(self, filters):
        self.stack = []
        self.filters = filters
        self.nodes = []

    def write(self, out):
        def puts(x):
            out(x)
            out('\n')

        for node in self.nodes:
            if node.is_valid:
                node.write(puts)
        del self.nodes[:]

    def run(self, frame, event, arg):
        if event == 'c_call' or event == 'c_return':
            return

        for f in self.filters:
            if not f.is_target(frame):
                continue
            if event == 'call':
                node = Node(frame, f.write, len(self.stack))
                self.nodes.append(node)
                self.stack.append(node)
            if event == 'return':
                if self.stack:
                    self.stack.pop().call_return(frame, arg)


class Node(object):
    def __init__(self, frame, formatter, indent):
        self.start_at = datetime.datetime.now()
        self.indent = indent
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
