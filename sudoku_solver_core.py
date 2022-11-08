'''
Solves a sudoku from a string input.

Input string must contain exactly 81 characters.
Each character must be a number between 0 (empty space) and 9.

Functions:
    solve_sudoku(input) -> str
'''

import numpy as np
import copy
import re

DOMAIN = set(range(1,10))
GRID_STATES = []
POSSIBLE_VALUES_STATES = []
ARC_CONSISTENCY = True

grid = np.zeros(shape=(9,9), dtype=np.int32)
possible_values = np.empty((9, 9), dtype=set)
solutions = []

def solve(input):
    '''Input must be a 81-character long and contain only values 1-9 and dots'''

    global grid

    # validate input
    if len(input) != 81 or re.search('[^0-9]', input):
        raise ValueError

    # initialize grid
    grid = np.array([*input], dtype=np.int32).reshape(9,9)

    # initialize possible_values
    for row in range(9):
        for col in range(9):
            if (grid[row,col] > 0):
                possible_values[row,col] = set([grid[row,col]])
            else:
                possible_values[row,col] = DOMAIN.copy()

    # first propagation
    for row in range(9):
        for col in range(9):
            if(grid[row,col] > 0):
                _propagate_constraint(grid[row,col], row, col)

    _do_solve()

    return [''.join(sol.astype(dtype=str).flatten().tolist()) for sol in solutions]


def _do_solve():
    global grid
    global possible_values
    global solutions

    for row in range(9):
        for col in range(9):
            if(grid[row,col] == 0):
                for value in [*possible_values[row,col]]:
                    # state snapshot
                    GRID_STATES.append(grid.copy())
                    POSSIBLE_VALUES_STATES.append(copy.deepcopy(possible_values))
                    
                    # assign and try solve with this value
                    grid[row,col] = value
                    possible_values[row,col] = set([value])
                    _propagate_constraint(grid[row,col], row, col)
                    _do_solve()
                    
                    # restore state and go ahead trying different values
                    grid = GRID_STATES.pop()
                    possible_values = POSSIBLE_VALUES_STATES.pop()
                    possible_values[row,col].discard(value)


                return
    solutions.append(grid)


def _remove_possible_value(value, row, col):
    possible_values[row,col].discard(value)


def _propagate_constraint(value, row, col):
    if value not in range(1, 10):
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