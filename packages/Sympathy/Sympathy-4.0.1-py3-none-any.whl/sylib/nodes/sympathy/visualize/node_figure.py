# This file is part of Sympathy for Data.
# Copyright (c) 2016-2017, Combine Control Systems AB
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
import numpy as np

from sympathy import api
from sympathy.api import node as synode
from sympathy.api import qt2 as qt_compat
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, adjust

from sympathy.utils import preview

from sylib.figure import drawing, gui, mpl_utils

QtCore = qt_compat.QtCore
QtGui = qt_compat.QtGui
qt_compat.backend.use_matplotlib_qt()


_RELATED_NODEIDS = [
    'org.sysess.sympathy.visualize.figure',
    'org.sysess.sympathy.visualize.figures',
    'org.sysess.sympathy.visualize.figuresubplot',
    'org.sysess.sympathy.visualize.figurecompressorgui',
    'org.sysess.sympathy.visualize.bokehfigure',
]


class FigureCompressor(synode.Node):
    """
    Compress a list of Figures into one Figure.
    """

    author = 'Benedikt Ziegler'
    version = '0.3'
    icon = 'figurecompressor.svg'
    name = 'Figure Compressor'
    description = 'Compress a list of Figures to a single Figure'
    nodeid = 'org.sysess.sympathy.visualize.figurecompressorgui'
    tags = Tags(Tag.Visual.Figure)
    related = _RELATED_NODEIDS

    parameters = synode.parameters()
    parameters.set_list(
        'parent_figure', label='Parent figure:',
        description='Specify the figure from which axes parameters '
                    'and legend position are copied.',
        editor=synode.Util.combo_editor())
    parameters.set_boolean(
        'join_legends', value=True, label='Join legends',
        description='Set if legends from different axes should be '
                    'joined into one legend.')
    parameters.set_list(
        'legend_location', value=[0], label='Legend position:',
        plist=list(mpl_utils.LEGEND_LOC.keys()) + mpl_utils.OUTSIDE_LEGEND_LOC,
        description='Defines the position of the joined legend.',
        editor=synode.Util.combo_editor())
    parameters.set_boolean(
        'join_colorbars', value=False, label='Make first colorbar global',
        description='If checked, the colorbar from the first figure becomes '
                    'a global colorbar in the output figure.')
    parameters.set_boolean(
        'auto_recolor', value=False, label='Auto recolor',
        description='Automatically recolor all artists to avoid using a color '
                    'multiple times, if possible.')
    parameters.set_boolean(
        'auto_rescale', value=True, label='Auto rescale axes',
        description='Automatically rescale all axes to fit the visible data.')

    controllers = (
        synode.controller(
            when=synode.field('join_legends', 'checked'),
            action=synode.field('legend_location', 'enabled')))

    inputs = Ports([Port.Figures('List of Figures', name='input')])
    outputs = Ports([Port.Figure(
        'A Figure with the configured axes, lines, labels, etc',
        name='figure')])

    def adjust_parameters(self, node_context):
        adjust(node_context.parameters['parent_figure'],
               node_context.input['input'],
               lists='index')

    def execute(self, node_context):
        input_figures = node_context.input['input']
        output_figure = node_context.output['figure']
        parameters = node_context.parameters

        try:
            parent_figure_number = parameters['parent_figure'].value[0]
        except IndexError:
            parent_figure_number = 0

        input_axes = [figure.get_mpl_figure().axes for figure in input_figures]
        default_output_axes = output_figure.first_subplot().get_mpl_axes()

        axes_colorbars = drawing.compress_axes(
            input_axes, default_output_axes,
            parameters['join_legends'].value,
            parameters['legend_location'].selected,
            int(parent_figure_number),
            auto_recolor=parameters['auto_recolor'].value,
            auto_rescale=parameters['auto_rescale'].value,
            add_colorbars=not parameters['join_colorbars'].value)

        if parameters['join_colorbars'].value:
            drawing.add_global_colorbar(axes_colorbars, output_figure)


class SubplotFigures(synode.Node):
    """
    Layout the Figures in a list of Figures into subplots.

    The number of rows and columns is automatically adjusted to an approximate
    square. Empty axes in a non-empty row will be not shown.
    """

    author = 'Benedikt Ziegler'
    version = '0.2'
    icon = 'figuresubplots.svg'
    name = 'Layout Figures in Subplots'
    description = 'Layout a list of Figures in a Subplot'
    nodeid = 'org.sysess.sympathy.visualize.figuresubplot'
    tags = Tags(Tag.Visual.Figure)
    related = _RELATED_NODEIDS

    inputs = Ports([Port.Figures('List of Figures', name='input')])
    outputs = Ports([Port.Figure(
        'A Figure with several subplot axes', name='figure')])

    parameters = synode.parameters()
    parameters.set_integer(
        'rows', value=0, label='Number of rows',
        description='Specify the number of rows, or 0 for auto.'
                    'If rows and columns are both 0, the node with attempt '
                    'to create an approximately square layout.',
        editor=synode.Util.bounded_spinbox_editor(0, 100, 1))
    parameters.set_integer(
        'columns', value=0, label='Number of columns',
        description='Specify the number of columns, or 0 for auto.'
                    'If rows and columns are both 0, the node with attempt '
                    'to create an approximately square layout.',
        editor=synode.Util.bounded_spinbox_editor(0, 100, 1))
    parameters.set_boolean(
        'recolor', value=False, label='Auto recolor',
        description='Specify if artists should be assigned new colors '
                    'automatically to prevent duplicate colors.')
    # TODO(magnus): Using string here for compat with adjust(lists=index).
    parameters.set_string(
        'parent_figure', value='0', label='Parent figure:',
        description='Specify the figure from which colorbar '
                    'and legend are copied.',
        editor=synode.Util.combo_editor())
    parameters.set_boolean(
        'join_colorbars', value=False, label="Make parent's colorbar global",
        description='If checked, the colorbar from the parent figure is '
                    'placed as a global colorbar for all subplots. '
                    'Note that it is up to you to make sure that the colorbar '
                    'is actually valid for all subplots.')
    parameters.set_boolean(
        'join_legends', value=False, label="Make parent's legend global",
        description='If checked, the legend(s) in the first figure are '
                    'kept as global legends and all other legends are '
                    'discarded. Note that it is up to you to make sure that '
                    'the legend is actually valid for all subplots.')
    parameters.set_string(
        'share_x_axes', value='none', label='Share X axes',
        description='If None, each subplot has an independent X axis. '
                    'Othewise, subplots will share X axis, meaning that '
                    'zooming/panning in one subplot also affects other '
                    'subplots.',
        editor=synode.editors.combo_editor(
            options={'none': 'None',
                     'col': 'Per column',
                     'all': 'All'}))
    parameters.set_string(
        'share_y_axes', value='none', label='Share Y axes',
        description='If None, each subplot has an independent Y axis. '
                    'Othewise, subplots will share Y axis, meaning that '
                    'zooming/panning in one subplot also affects other '
                    'subplots.',
        editor=synode.editors.combo_editor(
            options={'none': 'None',
                     'row': 'Per row',
                     'all': 'All'}))

    def update_parameters(self, params):
        # Removed in 1.6.2:
        if 'remove_internal_ticks' in params:
            del params['remove_internal_ticks']

    def adjust_parameters(self, node_context):
        adjust(node_context.parameters['parent_figure'],
               node_context.input['input'],
               lists='index')

    def execute(self, node_context):
        input_figures = node_context.input['input']
        output_figure = node_context.output['figure']
        parameters = node_context.parameters
        rows = parameters['rows'].value
        cols = parameters['columns'].value
        auto_recolor = parameters['recolor'].value
        parent_figure = int(parameters['parent_figure'].value)
        global_colorbar = parameters['join_colorbars'].value
        global_legend = parameters['join_legends'].value
        sharex = parameters['share_x_axes'].value
        sharey = parameters['share_y_axes'].value

        # calculate the number of rows and columns if any is =0
        nb_input_figures = len(input_figures)
        if rows == 0 and cols == 0:
            rows = int(np.ceil(np.sqrt(nb_input_figures)))
            cols = int(np.ceil(np.sqrt(nb_input_figures)))
            if rows * cols - cols >= nb_input_figures > 0:
                rows -= 1
        elif rows == 0 and cols > 0:
            rows = int(np.ceil(nb_input_figures / float(cols)))
        elif rows > 0 and cols == 0:
            cols = int(np.ceil(nb_input_figures / float(rows)))

        if sharex == 'none' and sharey == 'none':
            auto_rescale = False
        elif sharex == 'none':
            auto_rescale = 'y'
        elif sharey == 'none':
            auto_rescale = 'x'
        else:
            auto_rescale = True

        subplots = np.array(output_figure.subplots(
            rows, cols, sharex=sharex, sharey=sharey)).ravel()

        figure_colorbars = {}

        for i, (subplot, input_figure) in reversed(list(enumerate(
                zip(subplots, input_figures)))):
            default_axes = subplot.get_mpl_axes()
            input_axes = [axes.get_mpl_axes() for axes in input_figure.axes]

            axes_colorbars = drawing.compress_axes(
                [input_axes], default_axes,
                legends_join=False,
                legend_location='best',
                copy_properties_from=0,
                auto_recolor=auto_recolor,
                auto_rescale=auto_rescale,
                add_colorbars=not global_colorbar,
                add_legends=(i == parent_figure or not global_legend))

            figure_colorbars[i] = axes_colorbars

        if global_colorbar and parent_figure in figure_colorbars:
            drawing.add_global_colorbar(
                figure_colorbars[parent_figure], output_figure)

        # don't show empty axes
        if len(subplots) > len(input_figures):
            for ax_to_blank in subplots[len(input_figures):]:
                ax_to_blank.set_axis(False)


MPL_TEMPLATES_DOCS = """
Templates
=========
When opening the configuration for this node for the first time it will
give you a selection of templates for easily getting started with some
common plot configurations.

Clicking on the tools button from the template selection or from inside a
template configuration gui lets you go to the tree view to see the current
configuration and modify it to suit your needs. This is a great way to quickly
create a plot or to learn how to do some specific things in the tree view.

"""


MPL_PLOT_TYPE_DOCS = """
Bar plots and histograms
------------------------
Bar plots and histograms are pretty similar plots. The difference lies in
how their x axis data is structured. The bar plot has distinct labels for
each bin, whereas each bin in a histogram lies between two points on a
continuous line. To get data on the correct format for a histogram plot
you can use the node :ref:`org.sysess.sympathy.dataanalysis.histogramcalc`
as a preprocessing node.

Use a *Bar Container* if you want to combine multiple bar plots by grouping
or stacking them. The bar plots should all have the same *Bar Labels*.
Please note that stacked bar plots are only situationally useful since it's
very difficult to gauge the heights of the individual bar parts.

Use a *Histogram Container* if you want to combine multiple histograms by
stacking them on top of each other. Please note that stacked histograms are
only situationally useful since it can be very difficult to read the
distributions of the individual histograms.

Heatmaps
--------
Heatmaps are two-dimensional histograms. To get data on the correct format
for a heatmap plot you can use the node
:ref:`org.sysess.sympathy.dataanalysis.heatmapcalc` as a preprocessing
node.

Box plots
---------
Box plots are good for comparing different distributions of data. The box
plot is special in that it expects a *list* of arrays as data. It can for
example be specified as ``[arg['Column A'], arg['Column B']]`` or with a
list comprehension ``[arg[col_name] for col_name in arg.column_names()]``.

Pie charts
----------
Pie charts can be used to show parts of a whole, but are generally
considered inferior to e.g. bar plots. If you use a pie chart you will also
want to set the *Aspect ratio* of the *Axes* to 'equal'. Otherwise your pie
chart will be very hard to read accurately.

"""

MPL_LEGEND_OUTSIDE_DOCS = """
It is possible to place the legend outside of the axes, but you might need
to tweak the *Distance from Axes* property to get it to look just right for
your specific plot.

"""

MPL_RELATED_NODES_DOCS = """
This node can not create subplots, but by creating multiple figure objects
you can use the node :ref:`org.sysess.sympathy.visualize.figuresubplot` to
arrange them as subplots.

Use the node :ref:`Export figures` to write the figures you produce to
files.

:ref:`org.sysess.sympathy.visualize.figurecompressorgui` can be used to
combine multiple figures into a single figure.

For creating interactive figures with the bokeh backend see
:ref:`org.sysess.sympathy.visualize.bokehfigure`.
"""


class Figure(synode.Node):
    __doc__ = gui.DOCS.format(
        templates=MPL_TEMPLATES_DOCS,
        extra_plot_types=MPL_PLOT_TYPE_DOCS,
        legend_outside=MPL_LEGEND_OUTSIDE_DOCS,
        related_nodes=MPL_RELATED_NODES_DOCS,
    )

    author = 'Benedikt Ziegler & Magnus Sandén'
    version = '0.1'
    icon = 'figure.svg'
    name = 'Figure'
    description = 'Create a Figure from some data.'
    nodeid = 'org.sysess.sympathy.visualize.figure'
    tags = Tags(Tag.Visual.Figure)
    related = _RELATED_NODEIDS

    parameters = synode.parameters()
    parameters.set_json(
        'parameters', value={},
        description='The full configuration for this figure.')

    inputs = Ports([Port.Custom('<a>', 'Input', name='input')])
    outputs = Ports([
        Port.Figure('Output figure', name='figure', preview=True)])

    def _parameter_view(self, node_context, input_data):
        figure_widget = gui.FigureFromTableWidget(
            input_data, node_context.parameters['parameters'],
            backend=mpl_utils.matplotlib_backend)
        preview_widget = preview.PreviewWidget(
            self, node_context, node_context.parameters)
        widget = preview.ParameterPreviewWidget(
            figure_widget, preview_widget)
        return widget

    def exec_parameter_view(self, node_context):
        input_data = node_context.input['input']
        if not input_data.is_valid():
            input_data = api.table.File()
        return self._parameter_view(node_context, input_data)

    def execute(self, node_context):
        data_table = node_context.input['input']
        figure = node_context.output['figure']

        config_table = node_context.output.group('config')
        if len(config_table) > 0:
            config_table = config_table[0]
        else:
            config_table = None

        parameters = node_context.parameters['parameters'].value
        figure_creator = drawing.CreateFigure(data_table, figure, parameters)
        figure_creator.create_figure()


@node_helper.list_node_decorator(['input'], ['figure'])
class Figures(Figure):
    name = 'Figures'
    nodeid = 'org.sysess.sympathy.visualize.figures'

    def _parameter_view_no_preview(self, node_context, input_data):
        figure_widget = gui.FigureFromTableWidget(
            input_data, node_context.parameters['parameters'],
            backend=mpl_utils.matplotlib_backend)
        preview_widget = preview.NullPreviewWidget(
            '<b>Preview requires non-empty input list</b>')
        preview_widget.setWordWrap(True)
        preview_widget.setAlignment(
            QtCore.Qt.AlignTop)
        widget = preview.ParameterPreviewWidget(
            figure_widget, preview_widget)
        return widget

    def exec_parameter_view(self, node_context):
        input_data = node_context.input['input']
        if input_data.is_valid() and len(input_data):
            return self._parameter_view(node_context, input_data[0])
        else:
            input_data = api.table.File()
            return self._parameter_view_no_preview(node_context, input_data)
