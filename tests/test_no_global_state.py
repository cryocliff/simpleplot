"""simpleplot's defining property: no global state. Figures are fully independent."""

import simpleplot


def test_no_pyplot_or_current_figure():
    # There must be no global "current figure/axes" or global rcParams.
    assert not hasattr(simpleplot, "pyplot")
    assert not hasattr(simpleplot, "gcf")
    assert not hasattr(simpleplot, "gca")
    assert not hasattr(simpleplot, "rcParams")


def test_two_figures_are_independent():
    f1, a1 = simpleplot.subplots()
    f2, a2 = simpleplot.subplots()
    a1.plot([0, 1, 2], [0, 1, 2])
    assert len(a1.artists) == 1
    assert len(a2.artists) == 0  # f2 untouched by drawing on f1


def test_style_is_per_figure():
    f1 = simpleplot.Figure()
    f2 = simpleplot.Figure()
    f1.style.line_width = 99.0
    assert f2.style.line_width != 99.0  # styles are not shared


def test_style_copy_does_not_mutate_source():
    base = simpleplot.Style()
    variant = base.copy(line_width=42.0)
    assert base.line_width != 42.0
    assert variant.line_width == 42.0
    # Color cycle must be a distinct list, not a shared reference.
    variant.color_cycle.append("#000000")
    assert "#000000" not in base.color_cycle


def test_color_cycle_is_per_axes():
    _, ax = simpleplot.subplots()
    l1 = ax.plot([0, 1], [0, 1])
    l2 = ax.plot([0, 1], [1, 2])
    assert l1.color != l2.color  # cycle advances
