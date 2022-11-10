'''
Solves a sudoku from a string input.

Input string must contain exactly 81 characters.
Each character must be a number between 1 and 9.
Empty cells are represented by a dot (.).

Functions:
    solve(input: str) -> str
'''

import numpy as np
import re

DOMAIN = '123456789'
STATES = []

solutions = []

def solve(input):
    '''Input must be a 81-character long and contain only values 1-9 and dots'''

    global grid

    # validate input
    if len(input) != 81 or re.search('[^1-9.]', input):
        raise ValueError

    # initialize grid
    grid = np.array([el.replace('.', DOMAIN) for el in input], dtype=str).reshape(9,9)

    # initial constraints propagation to ensure arc consistency
    # NB: this alone should solve th easiest sudokus with only 1 possible solution
    for row in range(9):
        for col in range(9):
            _propagate_constraint(row, col)

    _do_solve()

    return [''.join(sol.astype(dtype=str).flatten().tolist()) for sol in solutions]


def _do_solve():
    global grid
    global solutions

    for row in range(9):
        for col in range(9):
            # arc constraint removed all possible values from this cell
            if len(grid[row,col]) == 0:
                return
            # there are values to choose from
            if len(grid[row,col]) > 1:
                for value in grid[row,col]:
                    # state snapshot
                    STATES.append(grid.copy())
                    
                    # assign and try solve with this value
                    grid[row,col] = value
                    _propagate_constraint(row, col)
                    _do_solve()
                    
                    # restore state and go ahead trying different values
                    grid = STATES.pop()
                    grid[row,col] = grid[row,col].replace(value, '')
                # no more values to try for this cell
                return
    
    solutions.append(grid.copy())


def _remove_possible_value(value, row, col):
    if value in grid[row,col]:
        grid[row,col] = grid[row,col].replace(value, '')
        if len(grid[row,col]) == 1:
            _propagate_constraint(row, col)


def _propagate_constraint(row, col):
    value = grid[row,col]

    if len(value) > 1:
        return

    # a number can appear only once per row
    for c in range(9):
        if (c != col):
            _remove_possible_value(value, row, c)

    # a number can appear only once per column
    for r in range(9):
        if (r != row):
            _remove_possible_value(value, r, col)

    # a number can appear only once per box
    for r in range(9):
        for c in range(9):
            if (r//3 == row//3 and c//3 == col//3 and r != row and c != col):
                _remove_possible_value(value, r, c)

if __name__ == '__main__':
    print('This is the core package for sudoku-solver.')
    print('Please use sudoku-solver.py for interactive use')
    exit(0)