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
from sympathy.platform import migrations


CONVERSION_OLD_TYPES_NEW_TYPES = {
    'bool': 'b',
    'float': 'f',
    'int': 'i',
    'str': 'S',
    'unicode': 'U',
    'datetime': 'Mu',
}

TYPE_NAMES = {
    'b': 'bool',
    'f': 'float',
    'i': 'integer',
    'S': 'binary',
    'U': 'text',
    'Mu': 'datetime (UTC)',
    'Mn': 'datetime (naive)',
}


class ConvertTableColumns300(migrations.UpdateParametersMigration):
    nodeid = 'org.sysess.sympathy.data.table.converttablecolumns'

    def updated_definition(self):
        parameters = synode.parameters()
        editor = synode.editors.multilist_editor(edit=True, mode=False)
        parameters.set_list(
            'in_column_list', label='Select columns',
            description='Select the columns to use', value=[],
            editor=editor)
        parameters.set_list(
            'in_type_list', label='Select type',
            description='Select the type to use', value=[],
            editor=synode.editors.combo_editor(edit=False))
        parameters.set_list(
            'out_column_list', label='Convert columns',
            description='Selected columns to convert', value=[],
            editor=synode.editors.multilist_editor(),
            _old_list_storage=True)
        parameters.set_list(
            'out_type_list', label='Convert types',
            description='Selected types to use', value=[],
            editor=synode.editors.multilist_editor(),
            _old_list_storage=True)
        return parameters

    def forward_parameters_dict(self, old_params):
        # Move list configurations from .value to .list to better conform with
        # current best practice.
        for pname in ('out_type_list', 'out_column_list'):
            parameter = old_params[pname]
            if parameter['value']:
                parameter['list'] = parameter['value']
                parameter['value'] = []
        return old_params

    def update_parameters(self, old_params):
        old_params['out_type_list'].list = [
            CONVERSION_OLD_TYPES_NEW_TYPES.get(v, v)
            for v in old_params['out_type_list'].list]


class ConvertTablesColumns300(ConvertTableColumns300):
    nodeid = 'org.sysess.sympathy.data.table.converttablescolumns'


class ConvertSpecificColumnsTable(migrations.NodeMigration):
    nodeid = 'org.sysess.sympathy.data.table.converttablecolumns'
    from_version = migrations.updated_version
    to_version = migrations.updated_version
    name = ['Convert specific columns in Table', 'Convert columns in Table']

    def forward_status(self):
        old_parameters = self.get_parameters()
        out_types = old_parameters['out_type_list'].list
        if len(set(out_types)) <= 1:
            return migrations.Perfect
        return (migrations.NotAvailable,
                'The new node "Convert columns in Table" intended to replace '
                'this node does not support converting to multiple different '
                'column types in one node. To support that case you can '
                'manually add multiple copies of "Convert columns in Table" '
                'in series.')

    def forward_node(self):
        return dict(
            author="Erik der Hagopian",
            description='Convert selected columns to specified data type',
            icon='select_table_columns.svg',
            name='Convert columns in Table',
            nodeid='org.sysess.sympathy.data.table.convertcolumnstable',
            tags=Tags(Tag.DataProcessing.TransformData),

            inputs=Ports([Port.Table('Input')]),
            outputs=Ports([Port.Table('Output')]),
        )

    def forward_parameters(self, old_parameters):
        parameters = synode.parameters()
        editor = synode.editors.multilist_editor(edit=True)
        parameters.set_list(
            'columns', label='Columns',
            description='Columns that should be converted.',
            value=[], editor=editor)
        editor = synode.editors.combo_editor()
        parameters.set_list(
            'types', label='Target type',
            description='The type that these columns should be converted to.',
            list=list(sorted(TYPE_NAMES.values())),
            value_names=['text'],
            editor=editor)

        # Move old configuration to new parameters
        parameters['columns'].value_names = (
            old_parameters['out_column_list'].list)
        parameters['columns'].multiselect_mode = 'selected_exists'
        types = [TYPE_NAMES[k] for k in old_parameters['out_type_list'].list]
        if not types:
            types = ['text']
        parameters['types'].value_names = types

        return parameters

    def forward_ports(self, old_input_ports, old_output_ports):
        new_input_ports = [('', 0)]
        new_output_ports = [('', 0)]
        return new_input_ports, new_output_ports


class ConvertSpecificColumnsTables(ConvertSpecificColumnsTable):
    nodeid = 'org.sysess.sympathy.data.table.converttablescolumns'
    name = ['Convert specific columns in Tables', 'Convert columns in Tables']

    def forward_node(self):
        return dict(
            author="Erik der Hagopian",
            description='Convert selected columns to specified data type',
            icon='select_table_columns.svg',
            name='Convert columns in Tables',
            nodeid='org.sysess.sympathy.data.table.convertcolumnstables',
            tags=Tags(Tag.DataProcessing.TransformData),

            inputs=Ports([Port.Tables('Input')]),
            outputs=Ports([Port.Tables('Output')]),
        )


class ConvertColumnsTable300(migrations.UpdateParametersMigration):
    nodeid = 'org.sysess.sympathy.data.table.convertcolumnstable'

    def updated_definition(self):
        parameters = synode.parameters()
        editor = synode.Util.multilist_editor(edit=True)
        parameters.set_list(
            'columns', label='Columns',
            description='Columns that should be converted.',
            value=[], editor=editor)
        editor = synode.Util.combo_editor()
        parameters.set_list(
            'types', label='Target type',
            description='The type that these columns should be converted to.',
            list=list(sorted(TYPE_NAMES.values())),
            value_names=['text'],
            editor=editor)
        return parameters


class ConvertColumnsTables300(ConvertColumnsTable300):
    nodeid = 'org.sysess.sympathy.data.table.convertcolumnstables'
