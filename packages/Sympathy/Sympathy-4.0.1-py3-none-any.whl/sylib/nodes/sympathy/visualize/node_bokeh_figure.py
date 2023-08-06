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
import numpy as np
from bokeh import layouts

from sympathy import api
from sympathy.api import node as synode
from sympathy.api import qt2 as qt_compat
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags

from sympathy.utils import preview

from sylib.bokeh import drawing, backend
from sylib.figure import gui

QtCore = qt_compat.QtCore
QtGui = qt_compat.QtGui
QtWidgets = qt_compat.QtWidgets


_RELATED_NODEIDS = [
    'org.sysess.sympathy.visualize.bokehfigure',
    'org.sysess.sympathy.visualize.bokehfiguresubplot',
    'org.sysess.sympathy.export.exportbokehfigures',
    'org.sysess.sympathy.visualize.figure',
]


BOKEH_RELATED_NODES_DOCS = """
This node can not create subplots, but by creating multiple figure objects
you can use the node
:ref:`org.sysess.sympathy.visualize.bokehfiguresubplot` to arrange them as
subplots.

Use the node :ref:`org.sysess.sympathy.export.exportbokehfigures` to write
the figures you produce to files.

For creating non-interactive figures using the matplotlib backend see
:ref:`org.sysess.sympathy.visualize.figure`.
"""


class BokehFigure(synode.Node):
    __doc__ = gui.DOCS.format(
        templates='',
        extra_plot_types='',
        legend_outside='',
        related_nodes=BOKEH_RELATED_NODES_DOCS,
    )

    author = 'Magnus Sandén'
    icon = 'figure.svg'
    name = 'Bokeh Figure'
    description = 'Create a Bokeh Figure from some data.'
    nodeid = 'org.sysess.sympathy.visualize.bokehfigure'
    tags = Tags(Tag.Visual.Figure)
    related = _RELATED_NODEIDS

    parameters = synode.parameters()
    parameters.set_json(
        'parameters', value={},
        description='The full configuration for this figure.')

    inputs = Ports([Port.Custom('<a>', 'Input', name='input')])
    outputs = Ports([
        Port.Custom('bokeh', 'Output figure', name='figure', preview=True)])

    def _parameter_view(self, node_context, input_data):
        figure_widget = gui.FigureFromTableWidget(
            input_data, node_context.parameters['parameters'],
            backend.bokeh_backend)
        try:
            preview_widget = preview.PreviewWidget(
                self, node_context, node_context.parameters)
        except ImportError as e:
            # QtWebEngineWidgets will fail import when running tests
            # on windows/servercore image.
            widget = QtWidgets.QLabel(f'Failed to load due to: {e}')
        else:
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
        output_figure = node_context.output['figure']

        parameters = node_context.parameters['parameters'].value
        figure = drawing.create_figure(data_table, parameters)
        output_figure.set_figure(figure)


class SubplotBokehFigures(synode.Node):
    """
    Layout the Figures in a list of Figures into subplots.

    Unless specified the number of rows and columns is automatically adjusted
    to an approximate square. Empty axes in a non-empty row will be not shown.
    """

    author = 'Magnus Sandén'
    icon = 'figuresubplots.svg'
    name = 'Layout Bokeh Figures in Subplots'
    description = 'Layout a list of Bokeh Figures in a Subplot'
    nodeid = 'org.sysess.sympathy.visualize.bokehfiguresubplot'
    tags = Tags(Tag.Visual.Figure)
    related = ['org.sysess.sympathy.visualize.bokehfigure']

    inputs = Ports([Port.Custom('[bokeh]', 'List of Figures', name='input')])
    outputs = Ports([Port.Custom(
        'bokeh', 'A Figure with several subplot axes', name='figure')])

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

    def execute(self, node_context):
        input_figures = node_context.input['input']
        output_figure = node_context.output['figure']
        parameters = node_context.parameters
        rows = parameters['rows'].value
        cols = parameters['columns'].value

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

        bokeh_figures = [f.get_figure() for f in input_figures]
        grid = layouts.grid(bokeh_figures, nrows=rows, ncols=cols)

        output_figure.set_figure(grid)
