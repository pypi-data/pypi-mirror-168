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
from collections import defaultdict, deque

import jinja2

from sympathy.api import node as synode
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sympathy.platform import migrations
from sympathy.api import exporters


_jinja2_globals = [
    'range',
    'lipsum',
    'dict',
    'cycler',
    'joiner',
    'namespace',
]


def _update_template(template_string):
    def get_names(node):
        if isinstance(node, jinja2.nodes.Name):
            return [node.name]
        res = []
        for child in node.iter_child_nodes():
            res.extend(get_names(child))
        return res

    def walk_ast(node, ctx):
        if isinstance(node, jinja2.nodes.Name):
            replace = False
            if node.ctx == 'load' and node.name not in ctx:
                replace = True
            names_on_lines[(node.name, node.lineno)].append(replace)
        elif isinstance(node, jinja2.nodes.For):
            # We special case for loops since those are the most common case of
            # a local scope within jinja2 templates. This will hopefully cover
            # 90% of real world cases without requiring us to implement too
            # much template-parsing logic.
            walk_ast(node.target, ctx)
            walk_ast(node.iter, ctx)

            # Within the body of the for loop there are new local variables:
            local_ctx = get_names(node.target) + ['loop']
            for child in node.body:
                walk_ast(child, ctx + local_ctx)

            for child in node.else_:
                walk_ast(child, ctx)
        else:
            for child in node.iter_child_nodes():
                walk_ast(child, ctx)

    jinja_env = jinja2.Environment()
    jinja_env.from_string(template_string)

    # We will use this data structure to keep track of all the names that
    # appear on each line and whether it should be replaced. Recording both the
    # names that should be replaced and the ones that should not allows us to
    # match the syntax tree nodes with tokens later on.
    names_on_lines = defaultdict(deque)
    # Recursively walk the abstract syntax tree returned by parse, recording
    # what names to replace and what names to keep as they are on each line.
    walk_ast(jinja_env.parse(template_string), _jinja2_globals + ['arg'])

    # Use the token stream from lex to do the actual replacements in the
    # template.
    pos = 0
    new_template_string = ""
    for lineno, token_type, value in jinja_env.lex(template_string):
        pos += len(value)
        if token_type == 'name':
            try:
                replace = names_on_lines[(value, lineno)].popleft()
            except IndexError:
                replace = False
            if replace:
                value = f"arg['{value}'][0]"
        new_template_string += value

    return new_template_string


class Jinja2TemplateOld300(migrations.UpdateParametersMigration):
    nodeid = 'org.sysess.sympathy.texts.jinja2template'

    def updated_definition(self):
        parameters = synode.parameters()
        jinja_code_editor = synode.editors.code_editor(language="jinja")
        parameters.set_string(
            'template', label="Template", description='Enter template here',
            editor=jinja_code_editor)
        return parameters


class Jinja2TemplateOld400(migrations.NodeMigration):
    nodeid = 'org.sysess.sympathy.texts.jinja2template'
    from_version = migrations.updated_version
    to_version = migrations.updated_version
    name = ['Jinja2 template (deprecated)', 'Jinja2 template']

    def forward_status(self):
        return (
            migrations.Imperfect,
            "This migration attempts to update the template, but cannot do "
            "so successfully for all cases, so please check the result of the "
            "migration to find any places where the template needs to be "
            "updated manually."
        )

    def forward_node(self):
        return dict(
            name='Jinja2 template (deprecated)',
            description=(
                'Create and render a jinja2 template. Use "{{arg}}" for '
                'access to the data.'),
            icon='jinja_template.svg',
            tags=Tags(Tag.DataProcessing.Text),
            author='Magnus Sandén',
            nodeid='org.sysess.sympathy.texts.generic_jinja2template',
            plugins=(exporters.FigureDataExporterBase, ),

            inputs=Ports([Port.Custom('<a>', 'Input', 'in', n=(0, 1, 1))]),
            outputs=Ports([Port.Text('Rendered Template', name='out')]),
        )

    def forward_parameters(self, old_parameters):
        new_parameters = copy.deepcopy(old_parameters)
        new_parameters['template'].value = _update_template(
            old_parameters['template'].value)
        return new_parameters

    def forward_ports(self, old_input_ports, old_output_ports):
        return old_input_ports, old_output_ports
