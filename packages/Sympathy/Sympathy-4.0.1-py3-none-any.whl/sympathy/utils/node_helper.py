# This file is part of Sympathy for Data.
# Copyright (c) 2013, Combine Control Systems AB
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
import sys

from .. platform import node as synode
from .. platform import exceptions
from . import port as syport
from sympathy.platform import types as sytypes
from sympathy.types import typefactory


class _ListExecuteMixin(object):

    def _set_child_progress(self, set_parent_progress, parent_value, factor):
        def inner(child_value):
            return set_parent_progress(
                parent_value + (child_value * factor / 100.))
        return inner

    def _key_names(self, keys):
        if isinstance(keys, dict):
            return [value['name'] if 'name' else key in value
                    for key, value in keys.items()]
        return keys

    def _list_group(self, def_group, port_group, list_keys):

        def create_name_lookup():
            name_lookup = {}
            for i, port_def in enumerate(def_group):
                name = port_def.get('name')
                name_lookup[i] = name
                if name:
                    name_lookup[name] = name
            return name_lookup

        def lookup_ports(key, kind_lookup):
            name = kind_lookup.get(key)
            if name:
                return port_group.group(name)
            else:
                return [port_group[key]]

        name_lookup = create_name_lookup()
        list_inputs = [port
                       for key in self._key_names(list_keys)
                       for port in lookup_ports(key, name_lookup)]
        return list_inputs

    def exec_parameter_view(self, node_context):

        inputs = list(node_context.input)
        outputs = list(node_context.output)

        list_inputs = self._list_group(
            node_context.definition['ports']['inputs'],
            node_context.input, self._input_list_keys)
        child_inputs = []

        for i, p in enumerate(inputs):
            if p in list_inputs:
                if p.is_valid() and len(p):
                    child_port = p[0]
                else:
                    sytype = sytypes.from_string(
                        node_context.definition['ports'][
                            'inputs'][i]['type'])[0]
                    child_port = typefactory.from_type(sytype)
            else:
                child_port = p
            child_inputs.append(child_port)

        updated_node_context = self.update_node_context(
            node_context, child_inputs, outputs)

        return super().exec_parameter_view(
            updated_node_context)

    def execute(self, node_context):
        inputs = list(node_context.input)
        outputs = list(node_context.output)

        list_inputs = self._list_group(
            node_context.definition['ports']['inputs'],
            node_context.input, self._input_list_keys)
        list_outputs = self._list_group(
            node_context.definition['ports']['outputs'],
            node_context.output, self._output_list_keys)

        len_list_inputs = len(list_inputs)
        input_indices = {inputs.index(p): i
                         for i, p in enumerate(list_inputs)}
        output_indices = {outputs.index(p): i
                          for i, p in enumerate(list_outputs)}

        n_items = min(len(input) for input in list_inputs)
        res = None
        org_set_progress = self.set_progress

        for i, ports in enumerate(zip(*list_inputs)):
            factor = 100. / n_items
            parent_progress = i * factor
            self.set_progress(parent_progress)
            self.set_progress = self._set_child_progress(
                org_set_progress, parent_progress, factor)
            try:
                output_ports = [o.create() for o in list_outputs]

                input_ports = ports[:len_list_inputs]

                child_inputs = [input_ports[input_indices[j]]
                                if j in input_indices else p
                                for j, p in enumerate(inputs)]

                child_outputs = [output_ports[output_indices[j]]
                                 if j in output_indices else p
                                 for j, p in enumerate(outputs)]

                updated_node_context = self.update_node_context(
                    node_context, child_inputs, child_outputs)

                res = super().execute(
                    updated_node_context)

                for output_port, list_output in zip(output_ports,
                                                    list_outputs):
                    list_output.append(output_port)

            except Exception:
                raise exceptions.SyListIndexError(i, sys.exc_info())
            finally:
                self.set_progress = org_set_progress

        self.set_progress(100)
        return res


def _gen_list_ports(ports, keys):
    list_ports = [ports[key] for key in keys]
    changes = dict.fromkeys(list_ports)
    if isinstance(keys, dict):
        for key, port in zip(keys, list_ports):
            changes[port] = keys[key]

    return syport.Ports([
        syport.make_list_port(p, changes[p]) if p in list_ports else p
        for p in ports])


def _format_key(key):
    if isinstance(key, str):
        return '{}'.format(key)
    else:
        return 'port-index:{}'.format(key)


def _list_docs(input_keys, output_keys, single_node):
    return """
    Auto generated list version of :ref:`{node}`.

    In this version, the following ports from the original nodes have been
    changed to lists which the node loops over:

        :Looped Inputs: {inputs}.
        :Looped Outputs: {outputs}.

    For details see the original node.

    """.format(node=single_node.name,
               inputs=', '.join([_format_key(key) for key in input_keys]),
               outputs=', '.join([_format_key(key) for key in output_keys]))


def list_node_decorator(input_keys, output_keys):
    """
    Use this decorator to automatically create a list version of a node.

    As arguments to the decorator you should supply the input ports and output
    port that should be looped over, either using string keys or numeric
    indices. The new node class should also inherit from the non-list node
    class, overriding nodeid and name. It may also override any other field or
    method that needs to be special cased for the list version of the node.

    The specified ports are automatically changed to lists in the list version
    of the node, and the methods `execute` and `exec_parameter_view` are
    suitably adapted to deal with this. Note that the `adjust_parameters` is
    *not* adapted, but so long as you use the `adjust` function it should work
    for both nodes.
    """

    def inner(cls):
        """
        Dynamically add _ListExecuteMixin as an extra base class and then
        return the modified cls.
        """
        single_node = None
        for base_cls in cls.__bases__:
            if issubclass(base_cls, synode.Node):
                single_node = base_cls
        if single_node is None:
            raise TypeError("list_node_decorator is decorating a class "
                            "which doesn't inherit from synode.Node")

        inputs = _gen_list_ports(cls.inputs, input_keys)
        outputs = _gen_list_ports(cls.outputs, output_keys)
        doc = _list_docs(input_keys, output_keys, single_node)
        related = [single_node.nodeid] + getattr(cls, 'related', [])

        cls_dict = {
            '__doc__': doc,
            'related': related,
            'inputs': inputs,
            'outputs': outputs,
            '_input_list_keys': input_keys,
            '_output_list_keys': output_keys,
        }

        for k, v in cls_dict.items():
            setattr(cls, k, v)

        cls.__bases__ = (_ListExecuteMixin,) + cls.__bases__

        return cls
    return inner
