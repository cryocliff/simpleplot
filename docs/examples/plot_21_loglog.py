"""
Log-log axes
============
"""
import numpy as np
import simpleplot

x = np.logspace(0, 4, 60)
fig, ax = simpleplot.subplots()
ax.loglog(x, x ** 2, label="x^2")
ax.loglog(x, x ** 1.5, linestyle="--", label="x^1.5")
ax.set_title("loglog"); ax.grid(True); ax.legend()
fig.tight_layout()
