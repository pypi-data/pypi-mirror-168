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
import numpy as np
from sympathy.api import node
from sympathy.api.nodeconfig import Tag, Tags, Port, Ports


class GetEnvironment(node.Node):
    """
    Get selected variables as a table with two columns, `Name` and `Value`.

    Available variables include global variables, workflow variables and
    environment variables from the operating system.

    This node can be used to add some external control to the workflow.
    Each name will only occur once in the output and a separate transpose
    node can be used to get a table with multiple columns instead of rows.
    """
    name = 'Get Environment to Table'
    nodeid = 'org.sysess.sympathy.environment.get'
    author = 'Erik der Hagopian'
    icon = 'environment_table.svg'
    tags = Tags(Tag.Input.Environment)
    outputs = Ports([Port.Table('Variables', name='variables')])
    related = ['org.sysess.sympathy.data.table.transposetablenew']

    parameters = node.parameters()
    parameters.set_list(
        'variables', label='Select variables', description='Select variables.',
        editor=node.editors.multilist_editor(edit=True))

    def adjust_parameters(self, node_context):
        node_context.parameters['variables'].adjust(
            list(node_context.variables))

    def execute(self, node_context):
        variables = dict(node_context.variables)
        output = node_context.output['variables']
        selected = node_context.parameters['variables'].selected_names(
            list(variables))
        names = []
        values = []

        for name in selected:
            names.append(name)
            values.append(variables[name])

        output['Name'] = np.array(names)
        output['Value'] = np.array(values)
