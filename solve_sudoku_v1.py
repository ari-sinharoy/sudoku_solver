# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:12:07 2020

@author: JJ
"""

import numpy as np 

# Check for duplicate elements along the rows and columns
def check(p,elem,x,y):
    nrow = p.shape[0]
    ncol = p.shape[1]
    p_cop = p.copy()
    p_cop[x,y] = elem
    res = 1
    # row check
    for rows in range(nrow):
        if sum(p_cop[rows]==elem) >1:
            res = 0
    # column check
    for cols in range(ncol):
        if sum(p_cop[:,cols]==elem) >1:
            res = 0
    if res == 1:
        return elem

# Pick individual 3x3 boxes
def box_sel(p,n):
    if n>9:
        ans = 'InputError: Input an integer <= 9'
    else:
        if n/3 <= 1:
            row_i = 0
        elif n/3 <= 2:
            row_i = 3
        else:
            row_i = 6
        col_i = (n-row_i-1)*3
        ans = p[row_i:row_i+3,col_i:col_i+3]
    return ans


# For each cell in a box, find potential assignment 
def box_pot_sol(p,n):
    #boxes = best_box(p)
    if n <=3:
        row_a = 0
    elif ((n>3) & (n<=6)):
        row_a = 3
    else:
        row_a = 6
    lst = []
    box = box_sel(p,n)
    nrow = box.shape[0]
    ncol = box.shape[1]
    ms_elems = list(set(range(1,10))-set(box.flatten('C'))-set([0]))
    for x in range(nrow):
        for y in range(ncol):
            if box[x,y]==0:
                x1 = x + row_a
                y1 = y + (n-row_a-1)*3
                lst_x = [(x1,y1)]
                for item in ms_elems:
                    val = check(p,item,x1,y1)
                    if val in range(1,10):
                        lst_x += [item]
                    else:
                        lst_x += ['None']
                lst += [lst_x]
    return np.array(lst)
        
# Assign numbers to a particular cell
def pr_assgn(p):
    px = p.copy()
    for n in range(1,10):
        sol_1 = box_pot_sol(px,n)
        box = box_sel(px,n)
        ms_elems = list(set(range(1,10))-set(box.flatten('C'))-set([0]))
        for item in sol_1:
            item = item[item!='None']
            if len(item)==2:
                x = item[0][0]
                y = item[0][1]
                px[x,y] = item[1]
            else:
                for x in ms_elems:
                    if sum(sum(sol_1==x))==1:
                        cords = np.where(sol_1==x)[0][0]
                        px[sol_1[cords][0][0],sol_1[cords][0][1]] = x
    return px
    
# Iterate checking and assigning numbers until the solution is found
def trial(p,n_max):
    px = p.copy()
    res = ''
    for i in range(n_max):
        if ((sum(sum(px==0))>0) & (i<n_max-1)):
            px = pr_assgn(px)
        elif sum(sum(px==0))==0:
            res += 'Solution found after '+str(i)+'-th iterations'
            break
        elif ((sum(sum(px==0))>0) & (i==n_max-1)):
            res += 'Failed to find a solution after '+str(n_max)+' iterations'
    print('The original puzzle was\n'+str(p))
    print(res)
    return px