Usage
=====

Figures, not globals
--------------------

Everything hangs off a :class:`~simpleplot.Figure`. ``simpleplot.subplots()``
returns ``(fig, axes)`` just like matplotlib's ``plt.subplots()`` -- but there is
no global "current figure/axes" and no global ``rcParams``.

.. code-block:: python

   import simpleplot
   import numpy as np

   fig, axes = simpleplot.subplots(1, 2, figsize=(10, 4))
   x = np.linspace(0, 10, 200)
   axes[0].plot(x, np.sin(x)); axes[0].set_title("sin")
   axes[1].scatter(x, np.cos(x), s=8); axes[1].set_title("cos")
   fig.tight_layout()

Output surfaces
---------------

One scene, many targets:

============================================  ==================================
Call                                          Result
============================================  ==================================
``fig.save("x.svg")``                         static vector SVG
``fig.save("x.png")`` / ``fig.savefig(...)``  raster PNG
``fig.save("x.pdf")``                          vector PDF
``fig.save("x.html", interactive=True)``       interactive HTML (JS toolbar)
``fig._repr_svg_()``                           inline SVG in Jupyter
``fig.show()``                                 native pop-up window (``[gui]``)
============================================  ==================================

Interactive figures
--------------------

Interactive HTML and pop-up output carry a self-contained JavaScript toolbar
(no external requests -- works under strict CSPs like Jupyter). Nothing is
active until a tool is selected:

* **Span** -- drag to pan a single plot's data window.
* **Zoom** -- wheel or box-drag to zoom *one* axes in data space (ticks recompute).
* **Point Pick** -- click to read the nearest data value; arrow keys step along
  the series; right-click deletes. Reports extra dims (``z``, ``c``, ...).
* **Annotate** -- click to drop a text note anchored to the data.
* **Reset** / **Extract** -- restore the view, or copy/download all markers and
  annotations as CSV/JSON (or hand them back to the kernel with
  ``fig.show(wait_for_extract=True)``).

3-D data via ``ax.plot_frames(...)`` adds a play/pause/step **slider** over the
extra dimension.

Log scales, aspect, layout
--------------------------

.. code-block:: python

   ax.set_xscale("log"); ax.set_yscale("log")   # or ax.loglog(x, y)
   ax.set_aspect("equal")                        # circles look circular
   fig.tight_layout()                            # auto-margins, no overflow
   ax.annotate("peak", xy=(x0, y0), xytext=(x1, y1), arrowprops={})
   fig.suptitle("Overview")
