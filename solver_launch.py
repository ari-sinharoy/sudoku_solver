# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 01:14:05 2020

@author: JJ
"""

import sudoku_reader as sr
import solve_sudoku_v1 as ssv1

def solve_sudoku(level,n_max):
    n_puzzle = sr.reader(level)
    return ssv1.trial(n_puzzle,n_max)