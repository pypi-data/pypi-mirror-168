# This file is part of Sympathy for Data.
# Copyright (c) 2016, 2017, Combine Control Systems AB
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
from sympathy.api import exporters
from sylib.export import base


class ExportFigures(base.ExportMultiple, synode.Node):
    """Export Figures to a selected data format."""

    name = 'Export Figures'
    description = 'Export Figures to image files.'
    icon = 'export_figure.svg'
    tags = Tags(Tag.Output.Export)
    author = 'Benedikt Ziegler'
    nodeid = 'org.sysess.sympathy.export.exportfigures'
    version = '0.2'
    inputs = Ports([Port.Figures('Input figures', name='figures'),
                    Port.Datasources(
                        'External filenames',
                        name='port1', n=(0, 1, 0))])
    plugins = (exporters.FigureDataExporterBase, )
    parameters = base.base_params()
    related = [
        'org.sysess.sympathy.visualize.figure',
        'org.sysess.sympathy.visualize.figures',
    ]
