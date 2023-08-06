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
from sympathy.platform import migrations


_sort_options = {'Ascending': 'Standard',
                 'Descending': 'Reverse'}


class SortColumnsInTable300(migrations.UpdateParametersMigration):
    nodeid = 'org.sysess.sympathy.data.table.sortcolumns'

    def updated_definition(self):
        parameters = synode.parameters()
        parameters.set_list(
            'sort_order', label='Sort order',
            list=['Ascending', 'Descending'],
            value=[0],
            description='Sort order',
            editor=synode.editors.combo_editor())
        return parameters


class SortColumnsInTable400(migrations.Migration):
    nodeid = 'org.sysess.sympathy.data.table.sortcolumns'
    from_version = migrations.updated_version
    to_version = '4.0.0'

    def forward_status(self):
        return migrations.Perfect

    def forward_parameters(self, old_parameters):
        old_so = old_parameters['sort_order'].selected
        del old_parameters['sort_order']
        old_parameters.set_list(
            'sort_order', label='Sort order',
            list=['Ascending', 'Descending'],
            value_names=[old_so],
            description='Sort order',
            editor=synode.editors.combo_editor(_sort_options))
        return old_parameters
