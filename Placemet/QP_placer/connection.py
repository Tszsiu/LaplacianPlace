import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def connection(index_gate_net_pad, net_gatepad):
    def combination(net_gates):
        gate_combine = []
        for i in range(len(net_gates)):
            for j in range(i+1, len(net_gates)):
                gate_combine = np.append(gate_combine, [net_gates[i], net_gates[j]])
        return gate_combine
    [G, N, P] = index_gate_net_pad
    
    # 非对角元
    dia_val = np.zeros(G)
    dia_row = np.arange(G)
    dia_col = np.arange(G)

    C = coo_matrix((dia_val, (dia_row, dia_col)), shape=(G, G))

    combine = np.array([])

    for i in range(N):
        net_gates = net_gatepad[i].gates
        if len(net_gates) > 1:
            combine = np.append(combine, combination(net_gates))
    combine = combine.reshape(-1,2)

    # 写入非对角元
    for add_ele in combine:
        C +=  coo_matrix(([1,1], ([add_ele[0], add_ele[1]], [add_ele[1], add_ele[0]])), shape=(G, G))

    dia_row = np.arange(G)
    dia_col = np.arange(G)
    dia_val_sum = C.sum(axis=1)
    dia_vals = np.array([])
    for dia_val in dia_val_sum:
        dia_vals = np.append(dia_vals, dia_val)

    dia_vals = np.array([])
    dia_row = np.array([])
    dia_col = np.array([])

    w = 1

    for i in range(N):
        net_pads = net_gatepad[i].pads
        if len(net_pads) > 0:
            net_gates = net_gatepad[i].gates
            for net_gate in net_gates:
                dia_vals = np.append(dia_vals, w)
                dia_row = np.append(dia_row, net_gate)
                dia_col = np.append(dia_col, net_pads)
    
    B = coo_matrix((dia_vals, (dia_row, dia_col)), shape=(G, P))

    return B, C