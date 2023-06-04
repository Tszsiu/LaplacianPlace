import matplotlib.pyplot as plt

def plot_gate_pin(pin_index, gate_index):
    x_pin = pin_index[0]
    y_pin = pin_index[1]
    x_gate = gate_index[0]
    y_gate = gate_index[1]

    plt.figure(figsize=(6,6))
    plt.scatter(x_gate, y_gate, s=20)
    plt.scatter(x_pin, y_pin, marker='s', s=300)

    plt.xlim(0,100)
    plt.ylim(0,100)

    plt.grid()
    plt.show()