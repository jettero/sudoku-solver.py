#!/usr/bin/env python
# coding: utf-8

import re
from collections import namedtuple

class PYTR:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)
        self._m = self._g = self._gd = None

    def match(self, target):
        self._m = self._regex.match(target)
        self._g = self._gd = None
        return bool(self._m)

    def search(self, target):
        self._m = self._regex.search(target)
        self._g = self._gd = None
        return bool(self._m)

    @property
    def groups(self):
        if self._g is None:
            if self._m:
                self._g = self._m.groups()
            else:
                self._g = list()
        return self._g

    @property
    def groupdict(self):
        if self._gd is None:
            if self._m:
                gd = self._m.groupdict()
                gdc = namedtuple('GDC', gd.keys())
                gdc.__getitem__ = gd.__getitem__
                gdc.get = gd.get
                self._gd = gdc(**gd)
            else:
                self._gd = dict()
        return self._gd

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.groups[key]
        if isinstance(key, str):
            return self.groupdict[key]
        raise TypeError(f'not sure how to lookup key="{key}"')

    def __eq__(self, actual):
        return bool(self._regex.search(actual))

    def __repr__(self):
        return self._regex.pattern