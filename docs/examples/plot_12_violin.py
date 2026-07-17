"""
Violin plot
===========

Kernel-density silhouettes.
"""
import numpy as np
import simpleplot

rng = np.random.default_rng(9)
data = [rng.normal(loc, s, 300) for loc, s in [(0, 1), (1, 0.6), (2, 1.3)]]
fig, ax = simpleplot.subplots()
ax.violinplot(data)
ax.set_title("violinplot")
fig.tight_layout()
