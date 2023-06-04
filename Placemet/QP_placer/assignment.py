import math
def assignment(index_GNP, gate_index):
    [G, N, P] = index_GNP
    x_gate = gate_index[0]
    mid = math.ceil(G/2)
    num_gate_left = x_gate.argsort()[:mid]
    num_gate_right = x_gate.argsort()[mid:]
    
    return [num_gate_left, num_gate_right]