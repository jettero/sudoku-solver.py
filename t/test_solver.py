#!/usr/bin/env python
# coding: utf-8

import logging
from sudoku.solver import process_opts, solve, Karen

log = logging.getLogger(__name__)

def test_process_opts():
    opts0 = process_opts(None)
    opts1 = process_opts(['human', 'dog', 'test'])
    opts2 = process_opts('this is my human dog test hybrid')
    opts3 = process_opts('human')
    opts4 = process_opts('dog')

    assert opts0 == set()
    assert opts1 == {'human', 'test'}
    assert opts2 == {'human', 'test'}
    assert opts3 == {'human',}
    assert opts4 == set()

def test_solver_doesnt_ruin_any_puzzle(any_p):
    q = solve(any_p)
    c = q.check()
    ok = bool(c)
    if not c:
        log.info('original puzzle that failed:\n%s\n\nour "solution":\n%s\nsolution history:', any_p, q)
        for item in q.history:
            log.info('  %s', item)
        log.info('problems:')
        for item in c:
            log.error("  %s", item)
    assert ok

def test_solvers_load_the_same_local_modules():
    assert set(Karen().local_modules) == set(Karen().local_modules)

def LPN(*a, **kw): # list plugin names
    return set(x[0] for x in Karen(*a, **kw).list_name_plugin() if x[1] is not None)

def test_solvers_reject_filters_work():
    lpn_0 = LPN()
    lpn_a = LPN(accept_filter='nop')
    lpn_r = LPN(reject_filter='nop')

    assert lpn_0 != lpn_a
    assert lpn_0 != lpn_r
    assert lpn_a != lpn_r
    assert len(lpn_a) == 1
    assert 't.rules.nop' in lpn_a
    assert 't.rules.nop' not in lpn_r
