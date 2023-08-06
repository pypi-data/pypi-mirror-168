# This file is part of Sympathy for Data.
# Copyright (c) 2022 Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.

from bokeh.models import (
    Plot,
    ColumnDataSource,
    Scatter,
    GlyphRenderer,
    Range1d,
    DataRange1d,
    FactorRange,
    LinearAxis,
    LogAxis,
    CategoricalAxis,
    LinearScale,
    LogScale,
    CategoricalScale,
    BoxZoomTool,
    ResetTool,
)
from bokeh.plotting import show, figure


data = {
    'x': [1, 2, 3],
    'y1': [2, 1, 4],
    'y2': [10, 20, 30],
}


def with_models():
    """Attempt to create a plot with two y axes using bokeh.models API."""
    source = ColumnDataSource(data)
    p = Plot()

    s1 = Scatter(x='x', y='y1', size=10)
    r1 = GlyphRenderer(glyph=s1, data_source=source, y_range_name='left')
    p.renderers.append(r1)

    s2 = Scatter(x='x', y='y2', size=10, fill_color='#ff0000')
    r2 = GlyphRenderer(glyph=s2, data_source=source, y_range_name='right')
    p.renderers.append(r2)

    p.x_range = DataRange1d()
    # p.y_range = DataRange1d()
    # p.y_range.renderers = [r1]
    p.extra_y_ranges = {'left': DataRange1d(), 'right': DataRange1d()}
    p.extra_y_ranges['left'].renderers = [r1]
    p.extra_y_ranges['right'].renderers = [r2]

    p.add_layout(LinearAxis(x_range_name='default'), 'below')
    p.add_layout(LinearAxis(y_range_name='left'), 'left')
    p.add_layout(LinearAxis(y_range_name='right'), 'right')

    p.extra_y_scales = {'left': DataRange1d(), 'right': DataRange1d()}

    p.add_tools(BoxZoomTool(), ResetTool())

    show(p)


def with_plotting():
    """Attempt to create a plot with two y axes using bokeh.plotting API."""
    p = figure(x_axis_type=None, y_axis_type=None)

    r1 = p.scatter(x=[1, 2, 3], y=[2, 1, 4], size=10,
                   x_range_name='bottom', y_range_name='left')
    r2 = p.scatter(x=[1, 2, 3], y=[10, 150, 100], size=10, color='#ff0000',
                   x_range_name='bottom', y_range_name='right')

    p.extra_x_ranges = {'bottom': DataRange1d()}
    p.extra_y_ranges = {'right': DataRange1d()}
    p.extra_x_ranges['bottom'].renderers = [r1, r2]
    p.extra_y_ranges['left'].renderers = [r1]
    p.extra_y_ranges['right'].renderers = [r2]

    p.add_layout(LinearAxis(x_range_name='default'), 'below')
    p.add_layout(LinearAxis(x_range_name='left'), 'left')
    p.add_layout(LinearAxis(y_range_name='right'), 'right')

    show(p)


def repro_logaxis_bug():
    source = {
        "t": [0,  1,   2,    3,     4],
        "v": [1, 10, 100, 1000, 10000],
    }

    f = figure(y_axis_type="log")

    f.yaxis.axis_label = "Log"
    f.yaxis.axis_label_text_color = "blue"

    f.extra_y_ranges = {"linear": DataRange1d()}
    f.extra_y_scales = {"linear": LinearScale()}

    ax = LinearAxis(y_range_name="linear", axis_label="Linear",
                    axis_label_text_color="red")
    f.add_layout(ax, "right")

    f.line(x="t", y="v", line_width=2, source=source, color="blue")
    f.circle(x="t", y="v", size=5, line_width=2, source=source, color="blue")

    f.line(x="t", y="v", line_width=2, source=source,
           y_range_name="linear", color="red")
    f.circle(x="t", y="v", size=5, line_width=2, source=source,
             y_range_name="linear", color="red")

    show(f)


def repro_logaxis_bug2():
    source = {
        "t": [0,  1,   2,    3,     4],
        "v": [1, 10, 100, 1000, 10000],
    }

    f = figure(y_axis_type="linear")

    f.yaxis.axis_label = "Linear"
    f.yaxis.axis_label_text_color = "blue"

    f.extra_y_ranges = {"log": Range1d(1, 20000)}
    f.extra_y_scales = {"log": LogScale()}

    ax = LogAxis(y_range_name="log", axis_label="Log",
                 axis_label_text_color="red")
    f.add_layout(ax, "right")

    f.line(x="t", y="v", line_width=2, source=source, color="blue")
    f.circle(x="t", y="v", size=5, line_width=2, source=source, color="blue")

    f.line(x="t", y="v", line_width=2, source=source,
           y_range_name="log", color="red")
    f.circle(x="t", y="v", size=5, line_width=2, source=source,
             y_range_name="log", color="red")

    show(f)


def repro_logaxis_bug3():
    source = {
        "t": [0,  1,   2,    3,     4],
        "v": [1, 10, 100, 1000, 10000],
    }

    f = figure(y_axis_type=None)

    # f.yaxis.axis_label = "Linear"
    # f.yaxis.axis_label_text_color = "blue"

    f.extra_y_ranges = {"linear": DataRange1d(),
                        "log": DataRange1d()}
    f.extra_y_scales = {"linear": LinearScale(),
                        "log": LogScale()}

    ax = LinearAxis(y_range_name="linear", axis_label="Linear",
                    axis_label_text_color="red")
    f.add_layout(ax, "left")
    ax = LogAxis(y_range_name="log", axis_label="Log",
                 axis_label_text_color="blue")
    f.add_layout(ax, "right")
    f.extra_y_ranges["log"].start = 1
    # f.extra_y_ranges["log"].end = 20000

    f.line(x="t", y="v", line_width=2, source=source, y_range_name="linear",
           color="red")
    f.circle(x="t", y="v", size=5, line_width=2, source=source,
             y_range_name="linear", color="red")

    f.line(x="t", y="v", line_width=2, source=source, y_range_name="log",
           color="blue")
    f.circle(x="t", y="v", size=5, line_width=2, source=source,
             y_range_name="log", color="blue")

    show(f)


def extra_factor_range():
    source = {
        "t": ["a", "b", "c", "d", "e"],
        "v": [1, 10, 100, 1000, 10000],
        "v2": [2, 20, 200, 200, 2000],
    }

    f = figure(x_axis_type=None)

    f.extra_x_ranges = {"above": FactorRange(factors=source["t"]),
                        "below": FactorRange(factors=source["t"])}
    f.extra_x_scales = {"above": CategoricalScale(),
                        "below": CategoricalScale()}
    f.x_range = FactorRange(factors=source["t"])
    f.x_scale = CategoricalScale()

    ax = CategoricalAxis(x_range_name="above", axis_label="Above")
    f.add_layout(ax, "above")
    ax = CategoricalAxis(x_range_name="below", axis_label="Below")
    f.add_layout(ax, "below")

    f.circle(x="t", y="v", size=5, line_width=2, source=source,
             x_range_name="above")
    f.circle(x="t", y="v2", size=5, line_width=2, source=source,
             x_range_name="below")
    show(f)


if __name__ == "__main__":
    # with_models()
    # with_plotting()
    # repro_logaxis_bug()
    # repro_logaxis_bug2()
    # repro_logaxis_bug3()
    extra_factor_range()
