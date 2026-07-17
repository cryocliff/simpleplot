"""
Error bars
==========
"""
import numpy as np
import simpleplot

rng = np.random.default_rng(7)
x = np.arange(10)
fig, ax = simpleplot.subplots()
ax.errorbar(x, np.sin(x), yerr=rng.uniform(0.1, 0.4, 10), capsize=3)
ax.set_title("errorbar")
fig.tight_layout()
