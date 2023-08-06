#!/usr/bin/env python3

# formal lib
from itertools import cycle
from matplotlib import colors as mc
import matplotlib.pyplot as plt

# color cycle
CMAP20 = plt.cm.get_cmap("tab20")
CMAP20_CYCLE = cycle(CMAP20.colors)
LINES_LIST = ["solid", "dashed", "dashdot", "dotted"]
LINES_CYCLE = cycle(LINES_LIST)

def gene_20color_4lstyle():
    col_20cycle = cycle(CMAP20.colors)
    line_cycle = cycle(LINES_LIST)
    for col, lstyle in zip(col_20cycle, line_cycle):
        yield col, lstyle
