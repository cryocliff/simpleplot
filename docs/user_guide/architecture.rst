How it works
============

Design in one sentence
----------------------

Artists are data holders; a single pass in ``svg.py`` turns the scene into an
SVG string (with embedded raster only for mesh/image layers). There is no global
state, and the render boundary is where a future Rust backend slots in.

No global state
---------------

Unlike matplotlib, there is no ``pyplot`` layer and no global ``rcParams``. A
:class:`~simpleplot.figure.Figure` owns its axes and its own
:class:`~simpleplot.style.Style`. ``simpleplot.subplots()`` returns a fresh,
fully independent figure.

SVG-first, selectively raster
-----------------------------

Lines, bars, scatter, contours and text are vector ``<path>``/``<text>``. Only
2-D fields (``pcolormesh``, ``imshow``, ``hist2d``, curvilinear contour fill)
are rasterized -- each to a *single* embedded ``<image>``, so a 500x500 grid
costs one DOM node instead of 250,000 rectangles. Scatter markers are
zero-length round-capped strokes, so ``vector-effect: non-scaling-stroke`` keeps
them a constant size under interactive zoom.

Module layout
-------------

============================  ==================================================
Module                        Responsibility
============================  ==================================================
``figure.py``                 ``Figure``, ``subplots()``, layout, save/show
``axes.py``                   ``Axes``: plotting methods, limits, autoscale
``artists.py``                data-only scene primitives
``style.py``                  per-figure ``Style`` (replaces ``rcParams``)
``transform.py``              vectorized data->pixel transforms (linear + log)
``colors.py``                 ``Normalize``, colormap LUTs
``ticker.py``                 "nice number" + log tick locations
``svg.py``                    the renderer: scene -> SVG string
``png.py``                    stdlib-only PNG encoder for image layers
``raster.py``                 Pillow PNG backend; svglib/reportlab PDF
``fonts/``                    bundled Helvetica metrics (layout only)
``_interactive.py``           inlined vanilla JS: toolbar, zoom, pick, sliders
============================  ==================================================

Performance
-----------

Avoiding matplotlib's per-``Artist`` Python overhead makes simpleplot much
faster for **many-axes** figures, and rasterizing meshes to one image makes
``pcolormesh`` dramatically cheaper. A single huge polyline is *not* yet a win --
serializing 100k points to a path string is pure-Python float->string work; that
hot path is the target of the planned Rust backend. See the project ``README``
for benchmark numbers.
