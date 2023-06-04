import numpy as np
from scipy.sparse import coo_matrix

def containment(sign, index_GNP, num_gate_left, num_gate_right, gate_index, pin_index, C, B):
    [G, N, P] = index_GNP
    # x_gate = gate_index[0]
    y_gate = gate_index[1]
    if sign == 'left':
        num_gate_main = num_gate_left
        num_gate_secondary = num_gate_right
    elif sign == 'right':
        num_gate_main = num_gate_right
        num_gate_secondary = num_gate_left

    # 用左右对矩阵进行切片，其中：
    # left left 成为新的gates连接矩阵C
    C_new = C[num_gate_main].T[num_gate_main].T
    # right right 成为右侧新的gates连接矩阵，这里被舍弃
    # C_rr = C[num_gate_secondary].T[num_gate_secondary].T
    # C_lr C_rl 被移动后成为Pads
    C_lr = C[num_gate_main].T[num_gate_secondary].T
    # C_rl = C[num_gate_secondary].T[num_gate_main].T

    B_new_gate = np.array([]) # gate部分
    x_pin_new_gate = np.array([])
    y_pin_new_gate = np.array([])

    C_connection = C_lr.toarray()

    for num_new_gate in range(len(num_gate_secondary)):
        if any(C_connection[:,num_new_gate]):
            B_new_gate = np.append(B_new_gate, C_connection[:,num_new_gate])
            x_pin_new_gate = np.append(x_pin_new_gate, 50)
            y_pin_new_gate = np.append(y_pin_new_gate, y_gate[num_gate_secondary[num_new_gate]])

    B_new_gate = B_new_gate.reshape(-1,len(num_gate_main)).T

    x_pin = pin_index[0]
    y_pin = pin_index[1]

    B_new_pad = np.array([]) # 原pad部分
    x_pin_new_pad = np.array([])
    y_pin_new_pad = np.array([])

    num_pin = 0
    for x in x_pin:
        row = np.array([])
        # gate在左边，写入B_left，x_pin，y_pin
        for num_gate in num_gate_main:
            row = np.append(row, B.toarray()[num_gate][num_pin])
        B_new_pad= np.append(B_new_pad, row)
        # 若pin在右侧则移动到中点
        if sign == 'left':
            x_new = min(50.0, x_pin[num_pin])
        elif sign == 'right':
            x_new = max(50.0, x_pin[num_pin])

        x_pin_new_pad = np.append(x_pin_new_pad, x_new)
        y_pin_new_pad = np.append(y_pin_new_pad, y_pin[num_pin])

        num_pin += 1

    B_new_pad = B_new_pad.reshape(-1,len(num_gate_main)).T

    # 删除孤立的pin
    B_new_temp = np.array([])
    x_pin_new_pad_temp = np.array([])
    y_pin_new_pad_temp = np.array([])
    for num_pin in range(P):
        if any(B_new_pad[:,num_pin]):
            B_new_temp = np.append(B_new_temp, B_new_pad[:,num_pin])
            x_pin_new_pad_temp = np.append(x_pin_new_pad_temp, x_pin_new_pad[num_pin])
            y_pin_new_pad_temp = np.append(y_pin_new_pad_temp, y_pin_new_pad[num_pin])

    B_new_pad = B_new_temp.reshape(-1,len(num_gate_main)).T
    x_pin_new_pad = x_pin_new_pad_temp
    y_pin_new_pad = y_pin_new_pad_temp

    B_new = coo_matrix(np.hstack((B_new_gate, B_new_pad)))

    x_pin_new = np.append(x_pin_new_gate, x_pin_new_pad)
    y_pin_new = np.append(y_pin_new_gate, y_pin_new_pad)

    pin_index_new =  np.append(x_pin_new, y_pin_new).reshape(2,-1)
    index_GNP_new = [len(num_gate_main), 0, len(x_pin_new)]

    return [index_GNP_new, B_new, C_new, pin_index_new]