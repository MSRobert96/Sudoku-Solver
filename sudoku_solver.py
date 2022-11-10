'''
This is a terminal wrapper for sudoku_solver_core.
Use this if you want to use the program from terminal.
'''

import argparse
import re
from textwrap import wrap
import sudoku_solver_core

PROGRAM_NAME = 'Sudoku solver'
PROGRAM_AUTHOR = 'Roberto Milan'
PROGRAM_VERSION = '0.0.1'
PROGRAM_EPILOG = '''README:
The sudoku must be 81 characters long (whitespaces are ignored).
Any non 1-9 character will count as a blank cell, represented internally as a dot '.' .
'''


def main():
    params, terminal = init_terminal()
    sudoku: str = load_sudoku(params)

    solutions = sudoku_solver_core.solve(sudoku)
    output(sudoku, solutions, params['output'])

    terminal.exit(0)


def format_sudoku(string: str) -> str:
    '''Formats sudoku in a human readable format'''

    formatted = '+-------+-------+-------+\n'
    for row, line in enumerate(wrap(string, 9)):
        if (row in [3,6]): formatted += '+-------+-------+-------+\n'
        formatted += '| '
        for col, cell in enumerate(line):
            formatted += cell + ' ' + ('| ' if col in [2,5] else '')
        formatted += '|\n'
    formatted += '+-------+-------+-------+\n'

    return formatted

def load_sudoku(params: dict) -> str:
    '''Loads a sudoku as a 81-character string'''
    sudoku = load_sudoku_from_file(params['sudoku']) if params['file'] else params['sudoku']
    sudoku = re.sub(r'\s', '', sudoku)
    sudoku = re.sub(r'[^1-9]', '.', sudoku)
    return sudoku


def load_sudoku_from_file(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def init_terminal():
    '''Load command line helper'''
    terminal = argparse.ArgumentParser(
        prefix_chars='-/',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'{PROGRAM_NAME} by {PROGRAM_AUTHOR}',
        epilog=f'{PROGRAM_EPILOG}'
    )
    terminal.add_argument('sudoku', type=str, help='String representing the sudoku', )
    terminal.add_argument('-f', '--file', action='store_true', help='Treat input as path to sudoku file')
    terminal.add_argument('-o', '--output', type=str, help='Specify path of solution file')
    return vars(terminal.parse_args()), terminal


def output(sudoku: str, solutions: str, output_path: str):
    '''Outputs the solved sudoku to termina or to a file'''

    if solutions:
        output = 'Found {} solution(s) to this sudoku: \n\n{}\n\nSOLUTIONS:\n'.format(len(solutions), format_sudoku(sudoku))
        output += ''.join([f'\nSolution #{idx+1}\n{format_sudoku(sol)}\n' for idx, sol in enumerate(solutions)])
    else:
        output = 'Your input is not valid or it does not have any solution.'

    if(output_path):
        with open(output_path, 'w') as f:
            f.write(output)
    else:
        print(output)


if __name__ == '__main__':
    main()
