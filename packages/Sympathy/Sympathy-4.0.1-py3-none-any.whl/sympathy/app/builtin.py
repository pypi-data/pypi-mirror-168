# This file is part of Sympathy for Data.
# Copyright (c) 2015 Combine Control Systems AB
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
import json
import sys
import collections
import functools
import io

from sympathy.utils.prim import uri_to_path
from sympathy.utils import components, network
from sympathy.types import (sylambda, sylist_set_read_through,
                            sylist_set_write_through,
                            sylist_is_write_through,
                            sylist,
                            )

from sympathy.platform.node import Node
from sympathy.platform import state
from sympathy.platform import message
from sympathy.platform import node_result
from sympathy.platform import exceptions


SocketBundle = collections.namedtuple(
    'SocketBundle', ['socket', 'input_func', 'output_func', 'reader'])


class SendWriter(io.StringIO):
    def __init__(self, msg_type, socket_bundle, node):
        self._socket_bundle = socket_bundle
        self._node = node
        self._msg_type = msg_type
        super().__init__()

    def write(self, s):
        if not s:
            res = 0
        elif self._node and self._socket_bundle:
            network.send_all(
                self._socket_bundle.socket,
                self._socket_bundle.output_func(
                    self._msg_type(
                        [self._node.identifier, s])))
            res = len(s)
        else:
            res = super().write(s)
        return res


def _progress_output_func(org_func, n, ntot, child_full_uuid, locked_top_level,
                          msg):
    if isinstance(msg, message.ProgressMessage):
        if locked_top_level:
            msg = message.ChildNodeProgressMessage([child_full_uuid, msg.data])
        else:
            ntot_max = max(ntot, 1)
            msg = message.ProgressMessage((msg.data + 100.0 * n) / ntot_max)

    return org_func(msg)


def sub_progress_socket_bundle(socket_bundle, n, ntot, child_full_uuid=None,
                               locked_top_level=False):
    if socket_bundle is not None:
        return SocketBundle(
            socket_bundle.socket,
            socket_bundle.input_func,
            functools.partial(
                _progress_output_func, socket_bundle.output_func, n, ntot,
                child_full_uuid, locked_top_level),
            socket_bundle.reader)


def set_write_through(data):
    try:
        # For sylists.
        sylist_set_write_through(data)
        return True
    except AssertionError:
        try:
            # For filelists.
            data.set_write_through()
            return True
        except Exception:
            pass
    return False


def set_read_through(data):
    try:
        sylist_set_read_through(data)
        return True
    except AssertionError:
        try:
            # For filelists.
            data.set_read_through()
            return True
        except Exception:
            pass
    return False


builtin = sys.modules[__name__]


class Lambda(Node):

    name = 'lambda'

    @staticmethod
    def set_from_flowdata(output, flow):
        full_uuid = flow['full_uuid']
        name = flow['name']
        nodes = flow['nodes']
        input_nodes = flow['input_nodes']
        output_nodes = flow['output_nodes']
        node_deps = flow['node_deps']
        input_ports = flow['input_ports']
        output_ports = flow['output_ports']
        bypass_ports = flow['bypass_ports']

        output.set((sylambda.FlowDesc(
            full_uuid,
            name,
            nodes,
            input_nodes,
            output_nodes,
            node_deps,
            input_ports, output_ports, bypass_ports), []))

    def execute(self, node_context):
        flow = json.loads(node_context.parameters['flow'].value)
        self.set_from_flowdata(node_context.output[0], flow)

    def _env_expanded_parameters(self, parameters):
        # should not happen for Flows, they have no "real parameters", normal
        # nodes handle their expansion.
        return parameters


def source_module(source_file):
    if source_file is None:
        return builtin
    else:
        return compile_file(source_file)


def compile_file(source_file):
    """Setup up stdout/stderr, compile a source_file."""
    local_file = uri_to_path(source_file)
    return components.import_file(local_file, add_hash=False)


def capture_stdouterr(context, capture_output=True, socket_bundle=None,
                      state_node=None):
    """Capture stdout/stderr into string buffers."""
    if capture_output:
        stdout_file = SendWriter(
            message.StdoutMessage, socket_bundle, state_node)
        stderr_file = SendWriter(
            message.StderrMessage, socket_bundle, state_node)
        context['stdout'] = sys.stdout
        context['stderr'] = sys.stderr
        sys.stdout = stdout_file
        sys.stderr = stderr_file
        # For logging to be captured.
        # stream_handler = logging.StreamHandler(stderr_file)
        # stream_handler.setLevel(logging.DEBUG)
        # root_logger.addHandler(stream_handler)


def restore_stdouterr(context, capture_output=True):
    """Restore stdout/stderr from the string buffer."""
    if capture_output:
        sys.stdout = context['stdout']
        sys.stderr = context['stderr']


def store_stdouterr(result, context, capture_output=True):
    def decode_if_str(text):
        if isinstance(text, bytes):
            return text.decode(
                sys.getfilesystemencoding(), errors='replace')
        return text

    if capture_output:
        try:
            stdout_value = sys.stdout.getvalue()
        except UnicodeError:
            stdout_value = "Output lost due to encoding issues"
        result.stdout = decode_if_str(stdout_value)
        try:
            stderr_value = sys.stderr.getvalue()
        except UnicodeError:
            stderr_value = "Error messages lost due to encoding issues"
        result.stderr = decode_if_str(stderr_value)
    else:
        result.stdout = ''
        result.stderr = ''

    result.set_done()


class Flow(Node):
    """
    Worker side node implementation for locked subflow.
    """
    name = 'Flow'

    def execute(self, node_context):
        flowinfo = json.loads(
            node_context.definition['parameters']['data']['flow']['value'])
        node_deps = flowinfo['node_deps']
        nodes = flowinfo['nodes']

        # Could be useful to provide better feedback on exception.
        # name = flowinfo['name']

        objects = node_context._objects
        child_results = flow_execute(
            nodes, node_deps, {},
            objects,
            socket_bundle=self.socket_bundle,
            locked_top_level=True)

        if child_results:
            state.node_state().result.child_results = child_results

            for _, child_result in child_results:
                if child_result.has_error():
                    raise exceptions.SyChildError(
                        'Execution failed for some nodes in this subflow.')

    def _env_expanded_parameters(self, parameters):
        # should not happen for Flows, they have no "real parameters", normal
        # nodes handle their expansion.
        return parameters


class SerialNode(object):
    """Provides convenient access to a serialized node."""

    def __init__(self, node_data, typealiases,
                 socket_bundle, trans_map, parent_identifier):
        (self.__source_file,
         self.__class_name,
         self.full_uuid,
         parameters) = node_data[1]
        self.__parameters = parameters
        self.translated_filename_map = trans_map

        self.__typealiases = typealiases
        self.__socket_bundle = socket_bundle
        self.__parent_identifier = parent_identifier
        self.__node_class = None
        self.__context = None

    def _node_class(self):
        if not self.__node_class:
            context = {}
            context['sys'] = __import__('sys', context, context)

            if not self.__class_name:
                # Can happen after extract lambdas with missing nodes.
                # TODO(erik): missing nodes should make extract fail.
                raise exceptions.SyDataError(
                    f'Node: {self.label} is missing')
            mod = source_module(self.__source_file)
            self.__node_class = getattr(
                mod, self.__class_name)()._future__init__(
                    identifier=self.full_uuid,
                    parent_identifier=self.__parent_identifier,
                    definition=self.__parameters,
                    socket_bundle=self.__socket_bundle)

        return self.__node_class

    def execute(self, objects):
        node = self._node_class()
        self.__context = node.build_execute_context(
            node.expanded_parameters(self.__parameters),
            self.__typealiases,
            objects=objects,
            entry_context=False)
        node._execute_with_context(self.__context)

    def __getattr__(self, key):
        self._node_class().__getattribute__(key)

    def _objects(self):
        if self.__context:
            return self.__context._objects
        return {}

    def _close(self):
        if self.__context:
            self.__context.close()

    @property
    def input_files(self):
        return [port['file']
                for port in self.__parameters['ports']['inputs']]

    @property
    def output_files(self):
        return [port['file']
                for port in self.__parameters['ports']['outputs']]

    @property
    def label(self):
        try:
            return self.__parameters['label']
        except Exception:
            return 'Unknown label'


def flow_execute(
        nodes,
        node_deps,
        type_aliases,
        objects=None, exit_func=None,
        socket_bundle=None, locked_top_level=False,
        parent_identifier=None):

    def execute_node(objects):
        if any(d in exec_failed or d in exec_blocked
               for d in flip_deps[uuid]):
            exec_blocked.add(uuid)

        else:
            try:
                node.execute(objects)
                child_result.valid = False
            except Exception:
                if not locked_top_level:
                    raise
                exec_failed.add(uuid)
                child_result.store_current_exception()
            else:
                exec_done.add(uuid)

            child_results.append((uuid, child_result))

    def release(node):
        pass

    def close(port):
        port.close()

    capture_output = state.node_state().attributes.get('capture_output', False)

    exec_failed = set()
    exec_blocked = set()
    exec_done = set()
    child_results = []

    flip_deps = collections.defaultdict(lambda: [])
    for src, dst in node_deps:
        flip_deps[dst].append(src)

    parent_objects = objects
    objects = dict(objects)
    child_lists = {}

    # Ensure that top-level write-through lists are not used in the
    # flow, since they can not be read.
    for k, v in objects.items():
        if sylist_is_write_through(v):
            child_lists[k] = sylist(v.container_type)
    objects.update(child_lists)

    serial_nodes = {}

    ntot = len(nodes)
    translated_filename_map = {}

    for n, node in enumerate(nodes):
        child_full_uuid = node[1][2]
        serial_node = SerialNode(
            node, type_aliases,
            sub_progress_socket_bundle(socket_bundle, n, ntot, child_full_uuid,
                                       locked_top_level),
            translated_filename_map,
            parent_identifier)
        serial_nodes[serial_node.full_uuid] = serial_node

    file_outputs = {}

    for n, (uuid, node) in enumerate(serial_nodes.items()):
        child_result = node_result.NodeResult()

        if locked_top_level and capture_output:
            context = {}
            capture_stdouterr(context, True, socket_bundle, state.Node(uuid))
            try:
                execute_node(objects)
            finally:
                store_stdouterr(child_result, context)
                restore_stdouterr(context)
        else:
            execute_node(objects)

        objects.update(node._objects())

        release(node)
        if socket_bundle:

            if locked_top_level:
                network.send_all(
                    socket_bundle.socket,
                    socket_bundle.output_func(
                        message.ChildNodeDoneMessage(
                            [node.full_uuid, child_result.to_dict()])))

                network.send_all(
                    socket_bundle.socket,
                    socket_bundle.output_func(
                        message.ChildNodeProgressMessage(
                            [node.full_uuid, 100.0])))
            else:
                network.send_all(
                    socket_bundle.socket,
                    socket_bundle.output_func(
                        message.ProgressMessage(100.0 * (n + 1) / ntot)))

    for k, v in child_lists.items():
        parent_objects[k].extend(v)

    if exit_func:
        exit_func()

    for file_output in reversed(file_outputs.values()):
        # Close file outputs to commit the data to disk.
        close(file_output)

    for n, (uuid, node) in enumerate(serial_nodes.items()):
        node._close()
    return child_results


class Propagate(Node):
    """Propagate input to output."""

    author = 'Erik der Hagopian <erik.hagopian@combine.se>'
    copyright = '(C) 2017 Combine Control Systems AB'
    name = 'Propagate'
    description = 'Propagate input to output'
    nodeid = 'org.sysess.builtin.propagate'
    icon = 'empty.svg'
    version = '1.0'

    def execute(self, node_context):
        node_context.output[0].source(node_context.input[0])
