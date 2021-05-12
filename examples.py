"""
Created on Wed May 12 22:59:46 2021

@author: JJ
"""

from sudoku_solver import *
import time

# Solve a hard & evil puzzle from nine.websudoku.com

levels = ['Hard', 'Evil']

for level in levels:
    puzzle = load_puzzle(level)
    start = time.time()
    solution = run(puzzle)
    end = time.time()
    timing = end - start
    if sum(sum(sol==0)) == 0:
        print("Solved a %s puzzle in %f seconds" %(level, timing))
    else:
        print("Oops! Failed to solve a %s puzzle" %level)