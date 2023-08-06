# This file is part of Sympathy for Data.
# Copyright (c) 2022, Combine Control Systems AB
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
import copy
from collections import defaultdict

import numpy as np
from bokeh.models import (
    Legend, Grid,
    DataRange1d, FactorRange,
    LinearScale, LogScale, CategoricalScale,
    LinearAxis, LogAxis, DatetimeAxis, CategoricalAxis
)

from sylib.figure import colors, models
from sylib.bokeh import bokeh, backend


def _draw_figure_legend(figure, items, params):
    """
    Draw one joined legend for all axes in the figure.

    Adds arrows to labels to denote which axes the artist is part of.

    Parameters
    ----------
    figure: bokeh Plot
        The plot where the legend will be drawn.
    params: dict
        Properties dictionary for the figure legend.
    """
    if not params.get('show', True):
        return

    location = params.get('loc', 'upper right')
    if location.startswith('outside'):
        layout_location = (location
                           .replace('outside ', '')
                           .replace('upper', 'above')
                           .replace('lower', 'below'))
        location = 'center'
    else:
        location = (location
                    .replace('upper', 'top')
                    .replace('lower', 'bottom')
                    .replace(' ', '_'))
        layout_location = 'center'
    legend = Legend(items=items, location=location)
    figure.add_layout(legend, layout_location)

    fontsize = params.pop('fonsize', None)
    if fontsize is not None:
        legend.label_text_font_size = fontsize

    orientation = params.pop('orientation', 'vertical').lower()
    legend.orientation = orientation

    legend.title = params.get('title', None)

    if not params.get('frameon', True):
        figure.legend.border_line_width = 0


def is_numeric_ndarray(arr):
    return isinstance(arr, np.ndarray) and arr.dtype.kind in 'fuiMm'


def create_figure(data_table, params):
    figure_creator = FigureCreator(data_table, params)
    figure_creator.create_figure()
    return figure_creator.figure


class FigureCreator:
    """
    Used to create and populate a ``bokeh`` figure with data from `data_table`
    as defined in `param`.
    """
    def __init__(self, data_table, params):
        self.data_table = data_table
        self.figure = bokeh.new_bokeh_figure(
            x_axis_type=None, y_axis_type=None)
        self.ranges = {}

        root = models.Root(
            copy.deepcopy(params), backend=backend.bokeh_backend)
        root.set_data_table(data_table)
        self.parsed_param = root.export_config(eval=True)

        self._ranges = {}
        self._axis = {}
        self._legend_items = []
        self._axes_renderers = defaultdict(list)
        self.global_legend_properties = None

    def _translate(self, params, mpl_translations, nyi_properties=None):
        nyi_properties = nyi_properties or []
        return {
            mpl_translations.get(k, k): v
            for k, v in params.items()
            if k not in nyi_properties
        }

    def create_figure(self):
        fig_param = self.parsed_param
        self.apply_figure_parameters(fig_param)
        ax_params = fig_param.get('axes', [])

        for axes_param in ax_params:
            xaxis = axes_param.get('xaxis', {})
            yaxis = axes_param.get('yaxis', {})
            xaxis_pos = xaxis.get('position', 'bottom')
            yaxis_pos = yaxis.get('position', 'left')
            axes = (xaxis_pos, yaxis_pos)
            plots = axes_param.get('plots', [])
            for plot_param in plots:
                plot_type = plot_param.pop('type')
                if not plot_param.pop('show', True):
                    continue
                if plot_type == 'line':
                    self.add_lineplot(axes, plot_param)
                elif plot_type == 'scatter':
                    self.add_scatter(axes, plot_param)
                elif plot_type == 'bar':
                    self.add_bars(axes, plot_param)

        self.create_ranges_and_axes(ax_params)
        self.apply_axes_parameters(ax_params)
        self.draw_legends()

        return self.figure

    def _check_datetime_axes(self, axes, data):
        for a, d in zip(axes, data):
            if not isinstance(d, np.ndarray):
                d = np.array(d)
            if d.dtype.kind == 'M':
                self._axis[a] = DatetimeAxis()

    def _add_renderers(self, axes, renderers, label=None):
        for axis in axes:
            self._axes_renderers[axis].extend(renderers)
        if label is not None:
            self._legend_items.append((label, renderers))

    def bokeh_pos(self, range_name: str):
        if range_name == 'bottom':
            return 'below'
        elif range_name == 'top':
            return 'above'
        else:
            return range_name

    def create_ranges_and_axes(self, parameters):
        dims = [('x', 'bottom'),
                ('y', 'left')]

        for dim, default in dims:
            extra_ranges = {}
            extra_scales = {}
            for axes_params in parameters:
                axis_params = axes_params.get(f'{dim}axis', {})
                range_name = axis_params.get('position', default)
                scale_param = axis_params.get('scale', 'linear')

                # If the range has not been created by a plot, we create a
                # default range.
                range_ = self._ranges.setdefault(range_name, DataRange1d())
                if isinstance(range_, DataRange1d):
                    # Only let renderers from the current axes affect the
                    # automatic range calculation.
                    range_.renderers = self._axes_renderers[range_name]
                elif isinstance(range_, FactorRange):
                    # Workaround for the fact that Bokeh will look at the
                    # default range/scale and become confused if it is
                    # incompatible.
                    setattr(self.figure, f"{dim}_range",
                            FactorRange(factors=range_.factors))
                extra_ranges[range_name] = range_

                # Add a matching scale for this range, also considering the
                # users choice of scale for this axis.
                Scale = LinearScale
                if isinstance(range_, FactorRange):
                    Scale = CategoricalScale
                    # Workaround for the fact that Bokeh will look at the
                    # default range/scale and become confused if it is
                    # incompatible.
                    setattr(self.figure, f"{dim}_scale", CategoricalScale())
                elif scale_param == 'log':
                    Scale = LogScale
                extra_scales[range_name] = Scale()

            # We only use named "extra" ranges and never the default ranges
            setattr(self.figure, f'extra_{dim}_ranges', extra_ranges)
            setattr(self.figure, f'extra_{dim}_scales', extra_scales)

            # Add Axis depending on the type of the range and scale
            for range_name, scale in extra_scales.items():
                Axis = LinearAxis
                if isinstance(scale, CategoricalScale):
                    Axis = CategoricalAxis
                elif isinstance(scale, LogScale):
                    Axis = LogAxis
                axis_kwargs = {f'{dim}_range_name': range_name}
                self._axis.setdefault(range_name, Axis(**axis_kwargs))
                self.figure.add_layout(
                    self._axis[range_name], self.bokeh_pos(range_name))

    def apply_axes_parameters(self, parameters):
        for axes_params in parameters:
            axes_params = copy.deepcopy(axes_params)

            xaxis = axes_params.pop('xaxis', {})
            yaxis = axes_params.pop('yaxis', {})

            x_range_name = xaxis.get('position', 'bottom')
            y_range_name = yaxis.get('position', 'left')

            grid_params = axes_params.pop('grid', None)
            if grid_params is not None:
                grid_axis = grid_params.get('axis', 'both')
                grids = {}
                if grid_axis in ['both', 'x']:
                    grids[x_range_name] = Grid(dimension=0)
                if grid_axis in ['both', 'y']:
                    grids[y_range_name] = Grid(dimension=1)
                for range_name, grid in grids.items():
                    linecolor = grid_params.get('color', '#e5e5e5')
                    which = grid_params.get('which', 'both')
                    grid.minor_grid_line_color = (
                        linecolor if which in ['minor', 'both'] else None)
                    grid.grid_line_color = (
                        linecolor if which in ['major', 'both'] else None)

                    grid.axis = self._axis[range_name]
                    grid.grid_line_dash = grid_params.get(
                        'linestyle', 'solid')
                    grid.minor_grid_line_dash = grid_params.get(
                        'linestyle', 'solid')
                    grid.grid_line_width = grid_params.get(
                        'linewidth', 1)
                    grid.minor_grid_line_width = grid_params.get(
                        'linewidth', 1)
                    self.figure.add_layout(grid, 'center')

            xlabel = xaxis.pop('label', None)
            ylabel = yaxis.pop('label', None)

            color = axes_params.pop('color', None)
            if color is not None:
                self.figure.background_fill_color = color

            rot_tick_labels = xaxis.get("rot_tick_labels")
            rot = 'horizontal'
            if rot_tick_labels == 'Clockwise':
                rot = -np.pi/6
            elif rot_tick_labels == 'Vertical':
                rot = 'vertical'
            elif rot_tick_labels == 'Counter clockwise':
                rot = np.pi/6
            self._axis[x_range_name].major_label_orientation = rot

            x_range = self._ranges[x_range_name]
            xmin = xaxis.get('min')
            if xmin is not None:
                x_range.start = xmin
            xmax = xaxis.get('max')
            if xmax is not None:
                x_range.end = xmax
            y_range = self._ranges[y_range_name]
            ymin = yaxis.get('min')
            if ymin is not None:
                y_range.start = ymin
            ymax = yaxis.get('max')
            if ymax is not None:
                y_range.end = ymax

            if xaxis.get('inverted', False):
                x_range.flipped = True
                x_range.start, x_range.end = x_range.end, x_range.start
            if yaxis.get('inverted', False):
                y_range.flipped = True
                y_range.start, y_range.end = y_range.end, y_range.start

            if xlabel is not None:
                self._axis[x_range_name].axis_label = xlabel
            if ylabel is not None:
                self._axis[y_range_name].axis_label = ylabel

            # TODO: May need to tell the ZoomBoxTool to maintain aspect ratio
            aspect_ratio = axes_params.get('aspect', None)
            if aspect_ratio is not None:
                if aspect_ratio == 'equal':
                    aspect_ratio = 1
                elif aspect_ratio != 'auto':
                    aspect_ratio = float(aspect_ratio)
                self.figure.aspect_ratio = aspect_ratio

            self._axis[x_range_name].visible = xaxis.get('visible', True)
            self._axis[y_range_name].visible = yaxis.get('visible', True)

            if not axes_params.pop('frameon', True):
                self.figure.outline_line_color = None

    def add_bars(self, axes, params):
        ydata = params.pop('ydata')
        label = params.pop('label', None)

        mpl_translations = {
            'color': 'fill_color',
            'linewidth': 'line_width',
            'linestyle': 'line_dash',
            'edgecolor': 'line_color',
        }

        params = self._translate(params, mpl_translations)

        bin_labels = params.pop('bin_labels', None)
        renderers = self._bar_plot(
            axes, ydata, bin_labels, **params)

        self._check_datetime_axes(axes[1:], [ydata])
        self._add_renderers(axes, renderers, label=label)

    def _bar_plot(self, axes, values, labels=None, rwidth=0.8, bar_labels=None,
                  bar_labels_valign='center', bar_labels_font=None,
                  group=None, y0=0, capsize=10, xerr=None, yerr=None,
                  **kwargs):
        """Make a bar plot the way you want it."""
        if not isinstance(values, np.ndarray):
            values = np.array(values)
        if labels is None:
            labels = np.arange(len(values)).astype(str)
        bar_orientation = kwargs.pop('orientation', 'Vertical')

        x_data = np.arange(len(values))
        width = rwidth

        # Assume unity bin width
        left = x_data + 0.5
        if bar_orientation == 'Vertical':
            bar = self.figure.vbar
        else:
            bar = self.figure.hbar

        renderer = bar(
            left, width, values, y0,
            x_range_name=axes[0], y_range_name=axes[1], **kwargs)

        # Label the bins on the x axis.
        if bar_orientation == 'Vertical':
            self._ranges[axes[0]] = FactorRange(factors=labels)
            self._ranges[axes[1]] = DataRange1d()
            self._ranges[axes[1]].start = 0
        else:
            self._ranges[axes[1]] = FactorRange(factors=labels)
            self._ranges[axes[0]] = DataRange1d()
            self._ranges[axes[0]].start = 0

        return [renderer]

    def add_lineplot(self, axes, params):
        xdata = params.pop('xdata')
        ydata = params.pop('ydata')
        label = params.pop('label', None)

        marker_properties = [
            'marker',
            'markersize',
            'markerfacecolor',
            'markeredgecolor',
            'markeredgewidth',
        ]

        marker_params = {
            k: v for k, v in params.items() if k in marker_properties
        }

        mpl_translations = {
            'linewidth': 'line_width',
            'linestyle': 'line_dash',
            'edgecolor': 'line_color',
        }

        nyi_properties = [
            'drawstyle',
            *marker_params,
        ]

        params = self._translate(params, mpl_translations, nyi_properties)

        line_renderer = self.figure.line(
            xdata, ydata, x_range_name=axes[0], y_range_name=axes[1], **params)
        renderers = [line_renderer]

        if marker_params:
            mpl_translations = {
                'markersize': 'size',
                'markerfacecolor': 'fill_color',
                'markeredgewidth': 'line_width',
                'markeredgecolor': 'line_color',
            }
            marker_params = self._translate(marker_params, mpl_translations)
            scatter_renderer = self.figure.scatter(
                xdata, ydata, x_range_name=axes[0], y_range_name=axes[1],
                **marker_params)
            renderers.append(scatter_renderer)

        self._check_datetime_axes(axes, [xdata, ydata])
        self._add_renderers(axes, renderers, label=label)

    def add_scatter(self, axes, params):
        xdata = params.pop('xdata')
        ydata = params.pop('ydata')
        label = params.pop('label', None)

        mpl_translations = {
            's': 'size',
            'linewidths': 'line_width',
            'edgecolors': 'line_color',
        }

        nyi_properties = [
            'vmin',
            'vmax',
            'cmap',
            'colorbar',
            'errorbar',
        ]

        params = self._translate(params, mpl_translations, nyi_properties)

        # make sure color values are given in correct format
        vmin = params.get('vmin')
        vmax = params.get('vmax')

        if 'color' in params:
            color = params.pop('color')
            if isinstance(color, np.ndarray):
                # Set up colormap
                colormap = colors.COLORMAPS[params.get('cmap', 'auto')]
                if colormap is None:
                    # Use sequential colormap 'magma' by default
                    colormap = 'magma'
                    try:
                        if np.any(color < 0) and np.any(color > 0):
                            # Use diverging colormap
                            colormap = 'BrBG'
                    except TypeError:
                        pass

                if colormap in list(colors.DIVERGING_COLORMAPS.values()):
                    c_abs_max = max(abs(min(color)),
                                    abs(max(color)))
                    if vmin is None:
                        vmin = -c_abs_max
                    if vmax is None:
                        vmax = c_abs_max
                else:
                    if vmin is None:
                        vmin = min(color)
                    if vmax is None:
                        vmax = max(color)
                params['vmin'] = vmin
                params['vmax'] = vmax
                params['cmap'] = colormap
            params['color'] = color

        # plot scatter
        renderer = self.figure.scatter(
            xdata, ydata,
            x_range_name=axes[0], y_range_name=axes[1],
            **params)

        self._check_datetime_axes(axes, [xdata, ydata])
        self._add_renderers(axes, [renderer], label=label)

    def draw_legends(self):
        if self.global_legend_properties is not None:
            _draw_figure_legend(
                self.figure, self._legend_items, self.global_legend_properties)

    def apply_figure_parameters(self, params):
        self.figure.title = params.get('title', None)
        self.global_legend_properties = params.get('legend', {'show': False})
