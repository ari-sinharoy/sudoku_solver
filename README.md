# sudoku_solver

For the past 10 years, I've been spending way too much time everyday solving sudoku. What's more annoying was that every now and then I failed to solve one. Hence, created this code and applied on sudokus from nine.websudoku.com - average solving time varies between less than a second for hard puzzles to a little over one second for evil ones.

Algorithm:
1. Find missing values in each box
2. Find possible entries in each cell of a box
3. Assign to a cell following sudoku rules (no repeat along any row or column)
4. Repeat till all the missing values are assigned
