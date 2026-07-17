"""
Bar chart
=========
"""
import numpy as np
import simpleplot

cats = np.arange(6)
fig, ax = simpleplot.subplots()
ax.bar(cats, [3, 7, 2, 5, 8, 4])
ax.set_xticks(cats); ax.set_title("Bar chart"); ax.set_ylabel("value")
fig.tight_layout()
