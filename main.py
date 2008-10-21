#!/usr/bin/env python

import sudoku;

p = sudoku.puzzle([
    [ 2,1,0, 6,0,0, 0,0,0 ],
    [ 0,0,0, 0,0,5, 4,0,0 ],
    [ 0,0,8, 0,0,0, 0,3,0 ],

    [ 9,0,3, 0,2,0, 0,6,0 ],
    [ 0,0,0, 0,0,0, 0,0,0 ],
    [ 0,7,0, 0,1,0, 5,0,4 ],

    [ 0,5,0, 0,0,0, 2,0,0 ],
    [ 0,0,6, 8,0,0, 0,0,0 ],
    [ 0,0,0, 0,0,4, 0,9,7 ],
]);

# s = sudoku.solver(p)
# s._loop_once()

print p
for row in p.rows:
    print [len(e.possibilities) for e in row]

for row in p.rows:
    for e in row:
        if len(e.possibilities) == 1:
            print e.possibilities
            e.i_am(e.possibilities[0])
