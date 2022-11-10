'''
Solves a sudoku from a string input.

Input string must contain exactly 81 characters.
Each character must be a number between 1 and 9.
Empty cells are represented by a dot (.).

Functions:
    solve(input: str, params: dict) -> str
'''

import re

DOMAIN = '123456789'
STATES = []
verbose = False

solutions = []

def solve(input, params = None):
    '''Input must be a 81-character long and contain only values 1-9 and dots'''

    global grid
    global verbose
    if ('verbose' in params.keys()):
        verbose = params['verbose']

    # validate input
    if len(input) != 81 or re.search('[^1-9.]', input):
        return []

    # initialize grid
    grid = [el.replace('.', DOMAIN) for el in input]

    if verbose: print('--------------- START ---------------')
    _do_solve()
    if verbose: print('---------------- END ----------------')

    return [''.join(sol) for sol in solutions]


def _do_solve():
    global grid
    global solutions

    if verbose: print("Propagating constraints...")
    _constraints_propagation()

    # traverse tree
    for row in range(9):
        for col in range(9):
            # arc constraint removed all possible values from this cell
            if len(grid[row*9+col]) == 0:
                return
            # there is more than one value to choose from
            if len(grid[row*9+col]) > 1:
                for value in grid[row*9+col]:
                    if verbose: print(f'Branching on cell ({row},{col}) with value {value}')

                    # state snapshot
                    STATES.append(grid.copy())
                    
                    # assign and try solve with this value
                    grid[row*9+col] = value
                    _do_solve()
                    
                    # restore state and go ahead trying different values
                    grid = STATES.pop()
                    grid[row*9+col] = grid[row*9+col].replace(value, '')
                # no more values to try for this cell
                return
    
    if verbose: print('Found solution!')
    solutions.append(grid.copy())


def _constraints_propagation():
    global grid
    while True:
        PREV_STATE = grid.copy()
        for row in range(9):
            for col in range(9):
                _propagate_single_constraint(grid[row*9+col], row, col)

        if grid == PREV_STATE:
            break



def _propagate_single_constraint(value, row, col):
    if len(value) == 1:
        # Direct constraints

        # a number can appear only once per row
        for c in range(9):
            if (c != col):
                grid[row*9+c] = grid[row*9+c].replace(value, '')

        # a number can appear only once per column
        for r in range(9):
            if (r != row):
                grid[r*9+col] = grid[r*9+col].replace(value, '')

        # a number can appear only once per box
        for r in range(9):
            for c in range(9):
                if (r//3 == row//3 and c//3 == col//3 and (r,c) != (row,col)):
                    grid[r*9+c] = grid[r*9+c].replace(value, '')

    else: 
        # Indirect constraints
        connected_values = set()
        for c in range(9):
            if c != col:
                connected_values.update(set(grid[row*9+c]))
        for r in range(9):
            if r != row:
                connected_values.update(set(grid[r*9+col]))
        for r in range(9):
            for c in range(9):
                if (r//3 == row//3 and c//3 == col//3):
                    connected_values.update(set(grid[r*9+c]))

        candidate = set(grid[row*9+col]).difference(connected_values)

        if len(candidate) == 1:
            grid[row*9+col] = candidate.pop()


if __name__ == '__main__':
    print('This is the core package for sudoku-solver.')
    print('Please use sudoku-solver.py for interactive use')
    exit(0)