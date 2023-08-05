from tkinter import Pack
import numpy as np
import matplotlib.pyplot as plt
# from mpltools import annotation

# some default font sizes for plots
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Dejavu Sans']


def random_plot(X, Y, labels,
                PATH="./image.png",
                x_label="x labels(need be replaced)",
                y_label="y labels(need be replaced)",
                title="titles",
                ):

    X = np.array(X)
    Y = np.array(Y)

    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(111)
    ax1.margins(0.1)
    ax1.grid(True)

    color = ['k', 'r', 'b', 'g', 'c', 'y']
    shape = ['-', '.']

    for i in range(len(Y)):
        ax1.plot(X, Y[i], '%s%s-' % (color[i % len(color)], shape[i % len(shape)]),
                 label=labels[i])

    ax1.set_xlabel(x_label, fontsize=16)
    ax1.set_ylabel(y_label, fontsize=16)
    ax1.set_title(title, fontsize=16)
    ax1.legend(loc='best', fontsize=14)

    plt.savefig(PATH)
