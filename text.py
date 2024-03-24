from scipy.optimize import linear_sum_assignment    
import numpy as np

matrix = np.array([[6, 2, 3], [-1, 5, 6], [7, 8, 5]])

row_ind, col_ind = linear_sum_assignment(matrix)
print(row_ind, col_ind)
print(matrix[row_ind, col_ind].sum())