#!/usr/bin/env python

import sudoku

def do_a_puzzle(p, outf):
    print p._before_string
    print p

    s = sudoku.solver(p)
    solved = 0
    while not solved:
        s._loop_once()
        print p
        solved = 1
        # NOTE: this should all, of course, be in the solver, not out here in
        # main...  First, we need a puzzle that fails to solve after one loop.

    outf.write(str(p))
    outf.write("\n")

if __name__ == "__main__":
    import re
    ofh = open("Output.txt", "w")

    puzzles = []

    f = open("Puzzles.txt")
    try:
        this_puzzle = []
        for line in f:
            elements = [ int(m) if m!='.' else 0 for m in re.findall('[0-9.]', line) ]
            if elements:
                if len(elements) != 9:
                    raise RuntimeError, "input file (Puzzles.txt) seems to be malformated, 9 values per row please"
                this_puzzle.append(elements)
                if len(this_puzzle) == 9:
                    puzzles.append( sudoku.puzzle(this_puzzle) )
                    this_puzzle = []
    finally:
        f.close()

        if len(this_puzzle) != 0:
            raise RuntimeError, "input file (Puzzles.txt) seems to be malformated, there should be n*9 rows in the input file"

    for p in puzzles:
        do_a_puzzle(p, ofh)
