# Sudoku Solver

## What is a sudoku 

A sudoku puzzle is composed of a square 9x9 board divided into 3 rows and 3 columns of smaller 3x3 boxes. The goal is to fill the board with digits from 1 to 9 such that:
- each number appears only once for each row column and 3x3 box;
- each row, column, and 3x3 box should containing all 9 digits.

---

## What does this program do
The solver takes as input a string where empty squares are represented by a dot ".", while known square are represented by the corresponding digit (1,...,9). For example:

```
37.5....6...36..12....9175....154.7...3.7.6...5.638....6498....59..26...2....5.64
```

Alternately, it can take a file name as a input (see CLI help -h).

Given a sudoku, it returns the solution(s).

---

## Prerequisites:
- `Python 3.7+`


## How to use

1. Download this repository on your device
2. From your cli, run `sudoku_solver.py` with Python:

```
~: python3 .\sudoku_solver_py -h
```

3. The CLI should print out the command helper

---

> Coded for the 1st assignment of "Foundations of Machine Learning" @ Ca' Foscari University 2022/2023
