# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 20:58:04 2020

@author: JJ
"""

'''
Load a puzzle from nine.websudoku.com
'''

import requests 
from bs4 import BeautifulSoup
import numpy as np

def find_level(lev):
    if lev == 'Hard':
        ans = 'level=3'
    elif lev == 'Medium':
        ans = 'level=2'
    elif lev == 'Easy':
        ans = 'level=1'
    return ans

# Load a medium level sudoku from websudoku.com

def reader(puzzle_lev):
    puzzle = np.zeros((9,9))
    #puzzle_lev = str(input("Define the difficulty level: (Easy/Medium/Hard): "
    #                       ))
    url = "https://nine.websudoku.com/?"+find_level(puzzle_lev)
    resp=requests.get(url) 
    # http_respone 200 means OK status 
    if resp.status_code==200:
        print("Successfully opened the web page") 
        # use built-in HTML parser 
        soup=BeautifulSoup(resp.text,'html.parser')
        puzzle_id = soup.find('a',{'title':'Copy link for this puzzle'}).text
        print("Loaded "+puzzle_id+" from https://nine.websudoku.com")
        tab_pzl = soup.find("table",{"id":"puzzle_grid"})
        tab_tds = tab_pzl.find_all("td")
        for rows in range(9):
            for cols in range(9):
                num = rows*9+cols
                try:
                    puzzle[rows,cols] = int(tab_tds[num].input.attrs['value'])
                except KeyError:
                    puzzle[rows,cols]
        return puzzle
    else:
        return 'Failed to load sudoku, error: '+resp.status_code