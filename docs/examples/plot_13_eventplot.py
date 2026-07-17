"""
Event plot
==========
"""
import numpy as np
import simpleplot

rng = np.random.default_rng(4)
rows = [np.sort(rng.uniform(0, 10, 40)) for _ in range(6)]
fig, ax = simpleplot.subplots()
ax.eventplot(rows)
ax.set_title("eventplot"); ax.set_xlabel("time")
fig.tight_layout()
