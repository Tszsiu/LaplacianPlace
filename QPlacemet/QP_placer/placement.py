import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def placement(index_gate_net_pad, B, C, pin_index):
    [G, N, P] = index_gate_net_pad

    x_pin = pin_index[0] # pin的坐标
    y_pin = pin_index[1]

    dia_row = np.arange(G)
    dia_col = np.arange(G)
    dia_val_sum_gate = C.sum(axis=1) # 利用C求gate对对角元的贡献
    dia_val_sum_pad = B.sum(axis=1) # 利用B求pad对对角元的贡献
 

    dia_val_sum = dia_val_sum_gate + dia_val_sum_pad
    dia_vals = np.array([])

    for dia_val in dia_val_sum:
        dia_vals = np.append(dia_vals, dia_val)

    A_dia = coo_matrix((dia_vals, (dia_row, dia_col)), shape=(G, G))

    A = A_dia - C

    b_x = B*x_pin
    b_y = B*y_pin

    dia_vals = np.array([])
    dia_row = np.array([])
    dia_col = np.array([])

    x_gate = spsolve(A.tocsr(), b_x)
    y_gate = spsolve(A.tocsr(), b_y)
    gate_index = np.append(x_gate, y_gate)
    gate_index = gate_index.reshape(2,-1)
    return gate_index