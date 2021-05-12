"""
Created on Mon Mar 29 11:28:07 2021

@author: JJ
"""

import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# load a puzzle from nine.websudoku.com

def load_puzzle(level = 'Evil'):
    puzzle = np.zeros((9,9))
    # lev = input("Specify the level of the puzzle (Easy/Medium/Hard/Evil): ")
    # Load a medium level sudoku from websudoku.com
    url0 = "https://nine.websudoku.com/?level="
    url = url0 + level
    resp=requests.get(url) 
    # http_respone 200 means OK status 
    if resp.status_code==200:
        print("Successfully opened the web page") 
        # use built-in HTML parser 
        soup=BeautifulSoup(resp.text,'html.parser')
        tab_pzl = soup.find("table",{"id":"puzzle_grid"})
        tab_tds = tab_pzl.find_all("td")
        for rows in range(9):
            for cols in range(9):
                num = rows*9+cols
                try:
                    puzzle[rows,cols] = int(tab_tds[num].input.attrs['value'])
                except KeyError:
                    puzzle[rows,cols] = 0
                    
    puzzle = puzzle.astype(int)
    
    return puzzle
                
# define the box range

def box_range(box):
    m = (box-1)//3
    x = (box-1)%3
    r1, r2 = m*3, (m+1)*3
    c1, c2 = x*3, (x+1)*3
    return r1,r2,c1,c2

# locate the empty cells by box

def empty_cells(puzzle, box):
    empty = np.where(puzzle == 0)
    empty = np.array(list(zip(empty[0], empty[1])))
    r1,r2,c1,c2 = box_range(box)
    return empty[((empty[:,0]>=r1) & (empty[:,0]<r2) & 
                  (empty[:,1]>=c1) & (empty[:,1]<c2))]

# find missing elements by box

def box_elems(puzzle, box):
    r1,r2,c1,c2 = box_range(box)    
    full = np.array([1,2,3,4,5,6,7,8,9])
    elems = np.setdiff1d(full, np.ndarray.flatten(puzzle[r1:r2,c1:c2]))
    
    return elems

# row & column check

def check_rules(puzzle, box):
    empty = empty_cells(puzzle, box)
    elems = box_elems(puzzle, box)
    res = pd.DataFrame(columns = ['position', 'elements'])
    for pos in empty:
        for item in elems:
            if ((np.count_nonzero(puzzle[pos[0]] == item) == 0) &
                (np.count_nonzero(puzzle[:,pos[1]] == item) == 0)):
                res = res.append({'position': pos,
                                  'elements': item},
                                 ignore_index = True)
    return res
                
# assign the values 

def assign_s1(puzzle):
    for box in range(1,10):
        s1 = check_rules(puzzle, box)
        s2a = s1.elements.value_counts()
        s2 = list(s2a[s2a==1].index)
        s3a = s1.position.value_counts()
        s3 = list(s3a[s3a==1].index)
        for x in s2:
            puzzle[tuple(s1[s1.elements == x].position.values[0])] = x
        for i in range(len(s3)):
            val = s1[[tuple(x) == tuple(s3[i]) 
                       for x in s1.position]].elements.values[0]
            puzzle[tuple(s3[i])] = val
    return puzzle


# run the program

def run(puzzle):
    p = puzzle.copy()
    c0 = sum(sum(p == 0))
    d0 = 1
    while (d0 > 0) & (c0 > 0):
        try:
            assign_s1(p)
        except IndexError:
            pass
        d0 = c0 - sum(sum(p == 0))
        c0 = sum(sum(p == 0))
    return p