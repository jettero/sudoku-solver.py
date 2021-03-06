#!/usr/bin/env python
# coding: utf-8

import os
import logging
import pkgutil
import importlib

import pluggy
import sudoku.rules

log = logging.getLogger(__name__)

NAMESPACES = ("sudoku.rules",)
INSTALLED_DIR = os.path.dirname(__file__)
KNOWN_OPTS = { 'human', 'test' }
# we don't actually use opts for anything (yet?)

def _process_opts(opts):
    if isinstance(opts, str):
        opts = opts.split()
    try:
        for item in opts:
            yield item
    except TypeError:
        pass


def process_opts(opts):
    return set(_process_opts(opts)).intersection(KNOWN_OPTS)


class RulesManager(pluggy.PluginManager):
    _local_modules = set()

    @property
    def local_modules(self):
        yield from self._load_local_modules()

    @classmethod
    def _load_local_modules(cls):
        if cls._local_modules:
            return cls._local_modules

        for namespace in NAMESPACES:
            plugin_path = os.path.join(INSTALLED_DIR, *namespace.split(".")[1:])
            log.debug("loading %s.* from %s", namespace, plugin_path)
            for item in pkgutil.iter_modules([plugin_path], f"{namespace}."):
                if item.name == __name__:
                    continue # pragma: no cover ; too rare to bother with
                log.debug("loading %s", item.name)
                m = importlib.import_module(item.name)
                cls._local_modules.add(m)

        return cls._local_modules

    def __init__(self, opts=None):
        super().__init__("sudoku")

        self.opts = process_opts(opts)
        if not self.opts:
            self.opts.add("human")

        log.debug("RulesManager.init [start]")

        self.add_hookspecs(sudoku.rules)
        for m in self.local_modules:
            log.debug("registering %s", m)
            self.register(m)
            log.debug("registered %s", m)

        # log.debug("loading setuptools 'sudoku_plugins' entrypoints")
        # self.load_setuptools_entrypoints("sudoku_plugins")

        log.debug("RulesManager.init [end]")

        self.step_count = 0

    def step(self, puzzle):
        # this doesn't give me pre/post functions for each hook
        # in any way I can actually figure out:
        #
        # ret = sum(self.hook.main(puzzle=puzzle, opts=self.opts))
        #
        # So, ima just do it myself:

        dc = 0
        for name,hook in self.list_name_plugin():
            try:
                dc += hook.main(puzzle=puzzle, opts=self.opts)
            except Exception as e:
                puzzle.describe_inference(f'{name} seems broken: {e}', __name__)
                continue
            chk = puzzle.check()
            if not chk: # pragma: no cover ; no need to check this, we check check() elsewhere
                puzzle.describe_inference(f'puzzle broke during {name}:', __name__)
                for item in chk:
                    puzzle.describe_inference(f'[!]  {item}', __name__)
                return 0
        return dc

    def solve(self, puzzle):
        puzzle = puzzle.clone()

        while self.step(puzzle) > 0:
            pass

        return puzzle


_manager = None


def get_manager(opts=None):
    global _manager
    if _manager is None:
        _manager = RulesManager(opts=opts)
    return _manager


Solver = Karen = get_manager


def solve(puzzle, opts=None):
    """ instantiate a Solver and solve the given puzzle """
    return Karen(opts=opts).solve(puzzle=puzzle)
