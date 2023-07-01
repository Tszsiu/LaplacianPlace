import numpy as np
import QP_placer.Nets_gatepad as Nets_gatepad

def input_data(file_name):
    """
    读取文本文件，并返回：1.nets，gate，pads的数量。2.pads的坐标。3.net数据结构，以储存每个net对应的gate和pads
    """

    with open(file_name) as file:
        content = file.read()
    content = content.strip()
    lines = content.split('\n')

    line_0 = lines[0].split() # NumberofGates G and NumberofNets N
    G = int(line_0[0]) # Gates 的数量
    N = int(line_0[1]) # Nets 的数量
    P = int(lines[G+1].split()[0]) # 存入Number of pads P connected to nets
    dia_val = np.array([]) # 存储对角线上的元素

    net_gatepad = np.array([]) # 用net_gate储存每个net对应的gate

    for i in range(N):
        net_gatepad = np.append(net_gatepad, Nets_gatepad.Nets_gatepad(i,[], [])) # 初始化net_gate，其gates和pads都为空
    # 存储gate
    for num_gate in range(G):
        line = lines[num_gate+1].split()
        nets = line[2:]
        for net in nets:
            net_gatepad[int(net)-1].gates = np.append(net_gatepad[int(net)-1].gates, num_gate) # 将gates的信息写入net_gate
    
    # 存储pad

    pin_index = []

    for num_pad in range(P):
        line = lines[G+2+num_pad].split()
        net = line[1]
        net_gatepad[int(net)-1].pads = np.append(net_gatepad[int(net)-1].pads, num_pad) # 将pads的信息写入net_gatepad
        
        pin_index = np.append(pin_index, float(line[2])) # pad的坐标
        pin_index = np.append(pin_index, float(line[3]))

    index_gate_net_pad = [G, N, P]
    pin_index = pin_index.reshape((-1,2)).T
    return index_gate_net_pad, pin_index, net_gatepad