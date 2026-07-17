"""
Quiver
======

A field of arrows.
"""
import numpy as np
import simpleplot

g = np.linspace(-2, 2, 16)
X, Y = np.meshgrid(g, g)
U, V = -Y, X
fig, ax = simpleplot.subplots()
ax.quiver(X, Y, U, V)
ax.set_aspect("equal"); ax.set_title("quiver")
fig.tight_layout()
