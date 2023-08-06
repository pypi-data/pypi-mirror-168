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


class SelectTableColumnsRegex300(migrations.UpdateParametersMigration):
    nodeid = 'org.sysess.sympathy.data.table.selecttablecolumnsregex'

    def updated_definition(self):
        parameters = synode.parameters()
        parameters.set_boolean(
            'complement', value=False,
            label="Remove matching columns",
            description=(
                'When enabled, matching columns will be removed. '
                'When disabled, non-matching columns will be removed.'))
        parameters.set_string(
            'regex', label='Search',
            description='Regex search pattern for matching column names.',
            value="")
        return parameters


class SelectTableColumnsRegex400(migrations.Migration):
    nodeid = 'org.sysess.sympathy.data.table.selecttablecolumnsregex'
    from_version = migrations.updated_version
    to_version = '4.0.0'

    def forward_status(self):
        return migrations.Perfect

    def forward_parameters(self, old_parameters):
        old_parameters.set_boolean(
            'full_match', value=True,
            label="Match full column names",
            description=(
                'When enabled, matching pattern in any part of'
                'column name will be found.'
                'When disabled, only matching pattern at the start'
                'of column name will be found.'))
        return old_parameters
