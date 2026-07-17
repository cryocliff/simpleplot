"""Sphinx configuration for the simpleplot documentation (Read the Docs)."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import simpleplot  # noqa: E402

# -- Project information ------------------------------------------------------
project = "simpleplot"
copyright = "2026, simpleplot contributors"
author = "simpleplot contributors"
release = simpleplot.__version__
version = release

# -- General configuration ----------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_gallery.gen_gallery",
]

autosummary_generate = True
autodoc_member_order = "bysource"
napoleon_numpy_docstring = True
napoleon_google_docstring = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_static_path = ["_static"]

# The sphinx-gallery scraper is a function, so the config can't be pickle-cached
# -- that warning is benign; suppress it so CI can build with -W (warnings as
# errors) and still catch real documentation problems.
suppress_warnings = ["config.cache"]

# -- HTML output (pydata theme, like the matplotlib docs) ---------------------
html_theme = "pydata_sphinx_theme"
html_title = f"simpleplot {version}"
html_theme_options = {
    "show_prev_next": True,
    "navigation_with_keys": True,
    "github_url": "https://github.com/simpleplot/simpleplot",
    "icon_links": [],
}


# -- sphinx-gallery: capture simpleplot Figures as example images -------------
def _simpleplot_scraper(block, block_vars, gallery_conf):
    """Save any new ``simpleplot.Figure`` created by an example to a PNG.

    Mirrors sphinx-gallery's matplotlib scraper, but scans the example's globals
    (simpleplot has no global figure registry) and rasterizes via the built-in
    Pillow backend.
    """
    from sphinx_gallery.scrapers import figure_rst

    it = block_vars["image_path_iterator"]
    seen = block_vars.setdefault("_simpleplot_seen", set())
    paths = []
    for value in list(block_vars["example_globals"].values()):
        if isinstance(value, simpleplot.Figure) and id(value) not in seen:
            seen.add(id(value))
            path = next(it)
            value.save(path, scale=2)      # PNG via simpleplot.raster
            paths.append(path)
    return figure_rst(paths, gallery_conf["src_dir"])


sphinx_gallery_conf = {
    "examples_dirs": "examples",
    "gallery_dirs": "auto_examples",
    # Separator-agnostic so examples execute on Windows and POSIX alike.
    "filename_pattern": r"plot_",
    "image_scrapers": (_simpleplot_scraper,),
    "reset_modules": (),
    "thumbnail_size": (400, 280),
    "remove_config_comments": True,
    "download_all_examples": False,
    "line_numbers": False,
}
