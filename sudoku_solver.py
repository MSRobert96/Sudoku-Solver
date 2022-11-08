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
Any non 1-9 character will count as a blank cell, represented as a dot '.' .
'''


def main():
    params, terminal = init_terminal()
    sudoku: str = load_sudoku(params)

    try:
        solutions = sudoku_solver_core.solve(sudoku)
    except ValueError:
        terminal.error('Provided sudoku must be exactly 81 characters long (whitespaces excluded).')
    except:
        terminal.error('Something went wrong')
    
    output(sudoku, solutions, params['output'])

    terminal.exit(0)


def format_sudoku(string: str) -> str:
    '''Formats sudoku in a human readable format'''
    string = string.replace('0', '.')
    return '\n'.join([' '.join(wrap(line, 3)) for line in wrap(string, 9)])

def load_sudoku(params: dict) -> str:
    '''Loads a sudoku as a 81-character string'''
    sudoku = load_sudoku_from_file(params['sudoku']) if params['file'] else params['sudoku']
    sudoku = re.sub(r'\s', '', sudoku)
    sudoku = re.sub(r'[^1-9]', '0', sudoku)
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
    terminal.add_argument('--version', action='version', version=f'%(prog)s {PROGRAM_VERSION}')
    terminal.add_argument('sudoku', type=str, help='String representing the sudoku', )
    terminal.add_argument('-f', '--file', action='store_true', help='Treat input as path to sudoku file')
    terminal.add_argument('-o', '--output', type=str, help='Specify path of solution file')
    return vars(terminal.parse_args()), terminal


def output(sudoku: str, solutions: str, output_path: str):
    '''Outputs the solved sudoku to termina or to a file'''
    solutions = [format_sudoku(sol) for sol in solutions]

    output = 'Found {} solution(s) to this sudoku: \n\n{}\n\nSOLUTIONS:\n'.format(len(solutions), format_sudoku(sudoku))

    for idx, sol in enumerate(solutions):
        output += '\nSolution #{}\n{}\n'.format(idx+1, sol)


    if(output_path):
        with open(output_path, 'w') as f:
            f.write(output)
    else:
        print(output)


if __name__ == '__main__':
    main()
