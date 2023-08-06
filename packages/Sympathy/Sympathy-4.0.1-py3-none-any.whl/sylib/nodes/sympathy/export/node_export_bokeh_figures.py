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
from sympathy.api import node as synode
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags

from sylib.bokeh.exporter import BokehFigureDataExporterBase
from sylib.export import base


class ExportBokehFigures(base.ExportMultiple, synode.Node):
    """Export Bokeh Figures to a selected data format."""

    name = 'Export Bokeh Figures'
    description = 'Export Bokeh Figures to html files.'
    icon = 'export_figure.svg'
    tags = Tags(Tag.Output.Export)
    author = 'Magnus Sandén'
    nodeid = 'org.sysess.sympathy.export.exportbokehfigures'
    inputs = Ports([Port.Custom('[bokeh]', 'Input figures', name='figures'),
                    Port.Datasources(
                        'External filenames',
                        name='port1', n=(0, 1, 0))])
    plugins = (BokehFigureDataExporterBase, )
    parameters = base.base_params()
    related = [
        'org.sysess.sympathy.visualize.bokehfigure',
        'org.sysess.sympathy.visualize.bokehfiguresubplot',
        'org.sysess.sympathy.export.exportbokehfigures']
