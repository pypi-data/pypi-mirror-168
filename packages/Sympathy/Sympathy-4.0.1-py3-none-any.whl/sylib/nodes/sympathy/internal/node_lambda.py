# This file is part of Sympathy for Data.
# Copyright (c) 2015-2016 Combine Control Systems AB
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
import base64
import copy
import re
import sys
import os
import subprocess
import uuid as uuidgen

from sympathy.api.nodeconfig import Tag, Tags, Port, Ports
from sympathy.platform.node import Node
from sympathy.platform.node import parameters as sy_parameters
from sympathy.types import exception as syexc
from sympathy.types import sylambda
from sympathy.app import builtin
from sympathy.platform.node import Util
from sympathy.api import ParameterView
from sympathy.api import exceptions
from sympathy.platform import types
from sympathy.platform import os_support
from sympathy.platform import version_support as vs
from sympathy.platform import qt_compat2
QtGui = qt_compat2.import_module('QtGui')
QtWidgets = qt_compat2.import_module('QtWidgets')


list_failure_strategies = dict(
    [('Error', 0), ('Create Empty Item', 1), ('Skip Item', 2)])

list_re = re.compile(r'^\[(.*)\]$')


class Apply(Node):
    """
    Apply Lambda function to Argument.

    When the Lambda function has multiple input arguments Apply will do a
    partial application producing a new Lambda function with with the argument
    bound as the value for the first argument.

    When the Lambda function has a single input argument Apply will evaluate
    the function to produce a result, taking into account any arguments
    previously bound.
    """

    name = 'Apply'
    description = 'Apply Lambda function to Argument'
    nodeid = 'org.sysess.builtin.apply'
    author = 'Erik der Hagopian <erik.hagopian@combine.se>'
    copyright = '(C) 2015-2016 Combine Control Systems AB'
    version = '1.0'
    icon = 'apply.svg'

    inputs = Ports([Port.Custom('<a> -> <b>', 'Lambda Function to Apply',
                                name='Function'),
                    Port.Custom('<a>', 'Argument', name='Argument')])
    outputs = Ports([Port.Custom('<b>', 'Output', name='Output')])

    tags = Tags(Tag.Generic.Lambda)

    @staticmethod
    def apply_eval(function, output, argument, portdict, writeback, objects,
                   socket_bundle=None, parent_identifier=None):
        def port_assign(port0, port1):
            port0['type'] = port1['type']
            port0['file'] = port1['file']

        flowdesc, ports = function.get()
        nodes = flowdesc.nodes
        node_deps = flowdesc.node_deps
        input_ports = flowdesc.input_ports
        output_ports = flowdesc.output_ports
        bypass_ports = flowdesc.bypass_ports

        input_assign = [port.data for port in ports]
        input_assign.append(portdict['inputs'][1])
        output_assign = [portdict['outputs'][0]]

        objects = {} if objects is None else objects
        objects[output_assign[0]['file']] = output
        objects[input_assign[-1]['file']] = argument
        input_assign_map = {}

        # Assigned input ports need to have their port description replaced.
        for ports, assign in zip(input_ports, input_assign or []):
            for port in ports:
                input_assign_map[port] = assign

        output_assign_map = dict(zip(output_ports, output_assign or []))

        if bypass_ports:
            bypass_port = int(bypass_ports[0])
            node_parameters = {
                'ports': {'inputs': [input_assign[bypass_port]],
                          'outputs': [output_assign[0]]},
                'parameters': {'data': {'type': 'group'}, 'type': 'json'},
                'id': 'org.sysess.builtin.propagate'
            }
            node = [None, [None, 'Propagate', f'{{{uuidgen.uuid4()}}}',
                           node_parameters]]
            nodes.append(node)

        output_filename_map = {}
        input_filename_map = {}
        filenames_set = set()

        for node_data in nodes:
            node_parameters = node_data[1][3]
            for portmap, filemap, group in [
                    (input_assign_map, input_filename_map, 'inputs'),
                    (output_assign_map, output_filename_map, 'outputs')
            ]:
                for port0 in node_parameters['ports'][group]:
                    port1 = portmap.get(port0['uuid'])
                    if port1:
                        filemap[port0['file']] = port1['file']
                        port_assign(port0, port1)

                    filenames_set.add(port0['file'])

        prefix = uuidgen.uuid4()
        filenames = list(sorted(filenames_set))
        filenames_index = {f: i for i, f in enumerate(filenames)}
        external_files = set()
        for portlist in [input_assign, output_assign]:
            external_files.update(p['file'] for p in portlist)

        for node_data in nodes:
            # For each assigned output port, any connected inputs also need
            # to be assigned.
            # Do not replace empty filename as these indicate a removed
            # optional port.
            node_parameters = node_data[1][3]
            for port0 in node_parameters['ports']['inputs']:
                filename = port0['file']
                if filename and filename in output_filename_map:
                    port0['file'] = output_filename_map[filename]

            for group in ['inputs', 'outputs']:
                for port0 in node_parameters['ports'][group]:
                    filename = port0['file']
                    # Replace internal filenames with generated non-existing
                    # filenames.
                    if filename and filename not in external_files:
                        port0['file'] = (
                            f'{{{prefix}}}.{{{filenames_index[filename]}}}')

        builtin.flow_execute(
            nodes, node_deps, {},
            objects, writeback, socket_bundle,
            parent_identifier=parent_identifier)

    @staticmethod
    def apply(function, output, portdict):
        port = portdict['inputs'][1]
        function.apply(
            sylambda.PortDesc(port))
        output.source(function)

    def execute(self, node_context):
        def writeback(output):
            def inner():
                try:
                    output.close()
                except ValueError:
                    # TODO (Erik): Fix proper handling with custom exception.
                    pass
                except syexc.WritebackReadOnlyError:
                    pass

            return inner

        function = node_context.input['Function']
        output = node_context.output['Output']
        writeback_fn = None

        ports = node_context.definition['ports']
        nargs = len(function.arguments())

        if nargs == 0:
            assert(False)
        if nargs == 1:
            argument = node_context.input['Argument']

            self.apply_eval(
                function, output, argument, ports,
                writeback_fn, node_context._objects, self.socket_bundle,
                self._parent_identifier or self._identifier)
        elif nargs > 1:
            self.apply(function, output, ports)


class Map(Node):
    """
    Map Lambda function over each element in argument list.

    Output list contains the result of element-wise application of the Lambda
    function on each input element.
    In contrast with Apply, partial application is not supported.
    """

    name = 'Map'
    description = 'Map Lambda function over each element in argument list'
    nodeid = 'org.sysess.builtin.map'
    author = 'Erik der Hagopian <erik.hagopian@combine.se>'
    copyright = '(C) 2015-2016 Combine Control Systems AB'
    version = '1.0'
    icon = 'map.svg'

    parameters = sy_parameters()
    parameters.set_list(
        'fail_strategy', label='Action on exception',
        list=list_failure_strategies.keys(), value=[0],
        description='Decide how failure to process an item should be handled.',
        editor=Util.combo_editor().value())

    inputs = Ports([Port.Custom('<a> -> <b>', 'Lambda Function to Map',
                                name='Function'),
                    Port.Custom('[<a>]', 'Argument List', name='List')])
    outputs = Ports([Port.Custom('[<b>]', 'Output List', name='List')])

    tags = Tags(Tag.Generic.Lambda)

    @staticmethod
    def apply_eval(function, output_list, argument_list, portdict,
                   objects, progress=None, fail_strategy=0,
                   socket_bundle=None, parent_identifier=None):
        def writeback(output):
            def inner():
                output_list.append(output)
            return inner

        objects = {} if objects is None else objects

        iter_portdict = copy.deepcopy(portdict)
        out_list_port = iter_portdict['inputs'][1]
        arg_list_port = iter_portdict['outputs'][0]

        # Peal of the list from the type for the invoked lambda.
        for list_port in [out_list_port, arg_list_port]:
            match = list_re.match(list_port['type'])
            if match is not None:
                list_port['type'] = match.groups()[0]

        nargs = len(argument_list)

        for i, argument in enumerate(argument_list):
            if progress is not None:
                progress(100.0 * i / nargs)
            output = output_list.create()

            try:
                Apply.apply_eval(function, output, argument, iter_portdict,
                                 writeback(output), dict(objects),
                                 builtin.sub_progress_socket_bundle(
                                     socket_bundle, i, nargs),
                                 parent_identifier=parent_identifier)

            except Exception:
                if fail_strategy == list_failure_strategies['Error']:
                    raise exceptions.SyListIndexError(i, sys.exc_info())
                elif fail_strategy == list_failure_strategies[
                        'Create Empty Item']:
                    output_list.append(output_list.create())
                    print('Encountered an error for item {}. '
                          'Creating empty item.'.format(i))
                else:
                    print('Encountered an error for item {}. '
                          'Skipping item.'.format(i))

        if progress is not None:
            progress(100.0)

    def update_parameters(self, parameter_root):
        if ('fail_strategy' in parameter_root and
                parameter_root['fail_strategy'].selected == 'Skip File'):
            parameter_root['fail_strategy'].selected = 'Skip Item'
            # .list and .value will be updated automatically to match
            # .value_names in the default update_parameters.

    def execute(self, node_context):
        own_objects = node_context._own_objects
        parameters = node_context.parameters
        function = node_context.input['Function']
        argument = node_context.input['List']

        if id(argument) in own_objects:
            builtin.set_read_through(argument)

        output = node_context.output['List']
        ports = node_context.definition['ports']
        nargs = len(function.arguments())

        if nargs == 0:
            assert(False)
        if nargs >= 1:
            self.apply_eval(
                function, output, argument, ports,
                node_context._objects, self.set_progress,
                parameters['fail_strategy'].value[0],
                self.socket_bundle,
                self._parent_identifier or self._identifier)
        elif nargs > 1:
            raise NotImplementedError(
                'Partial map application is not supported.')


class TypeEditorParameterView(ParameterView):
    def __init__(self, node_context, parent=None):
        super().__init__(parent=parent)
        self._parameters = node_context.parameters
        data_type = self._parameters['datatype'].gui()
        data_type.valueChanged.connect(self.status_changed)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(data_type)
        self.setLayout(layout)

    @property
    def valid(self):
        try:
            types.from_type_expand(
                types.from_string(self._parameters['datatype'].value))
        except Exception:
            return False
        return True


class ExtractParameterView(TypeEditorParameterView):
    def __init__(self, node_context, parent=None):
        super().__init__(node_context, parent=parent)
        ExtractLambdasHelper.add_fail_strategy(self._parameters)
        fail_strategy = self._parameters['fail_strategy'].gui()
        self.layout().addWidget(fail_strategy)


class ExtractLambdasHelper(object):
    @staticmethod
    def add_fail_strategy(parameters):
        if 'fail_strategy' not in parameters:
            error_handling = dict([
                ('error', 'Error'),
                ('skip', 'Skip item'),
            ])

            parameters.set_string(
                'fail_strategy',
                label='Strategy for handling extraction issues',
                description='How should the node handle the situation when '
                'the extract fails?',
                value='skip',
                editor=Util.combo_editor(
                    options=error_handling))


class ExtractLambdas(Node):
    """
    Extract top level Lambda functions matching datatype in flows.

    Lambda functions will change its type to reflect the choosen datatype
    as long as it is a non-generic function type and can be matched against
    connected nodes. Datatypes configured that fail to satisfy the above
    are simply be ignored.
    """

    name = 'Extract Lambdas'
    description = 'Extract Lambda functions matching datatype in workflows'
    nodeid = 'org.sysess.builtin.extractlambdas'
    author = 'Erik der Hagopian <erik.hagopian@combine.se>'
    copyright = '(C) 2015-2016 Combine Control Systems AB'
    version = '1.0'
    icon = 'extract.svg'

    inputs = Ports([Port.Datasources(
        'Flow filenames containing Lambdas', name='Filenames')])

    outputs = Ports([Port.Custom(
        '[() -> ()]', 'Lambda functions', name='Functions')])

    parameters = sy_parameters()
    parameters.set_string(
        'datatype', label='Datatype',
        description='Non-generic datatype to match against lambda functions '
        ' in input', value='() -> ()')
    ExtractLambdasHelper.add_fail_strategy(parameters)
    tags = Tags(Tag.Generic.Lambda)

    _marker = b'__SY_EXTRACT_OUTPUT_MARKER__'
    _subprocess_cls = 'ExtractLambdaSubprocess'
    _script = """
import os
import sys
import base64
import json
import ast
import argparse
import logging

eparams = sys.stdin.read()
params = json.loads(base64.b64decode(eparams.encode('ascii')).decode('ascii'))
sys.path[:] = ast.literal_eval(params['sys_path'])
os.chdir(params['cwd'])

parser = argparse.ArgumentParser()
parser.add_argument('cls', type=str)
parsed = parser.parse_args()

logging.basicConfig()
from sylib.internal import lambda_util
extract = getattr(lambda_util, parsed.cls)()
extract.execute(**params)"""

    def exec_parameter_view(self, node_context):
        return ExtractParameterView(node_context)

    def execute_subprocess_entrypoint(self):
        kwargs = {}
        return os_support.Popen_no_console(
            [sys.executable, '-c', self._script, self._subprocess_cls],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **kwargs)

    def execute(self, node_context):
        output_list = node_context.output[0]
        filenames = []
        for ds in node_context.input['Filenames']:
            filename = ds.decode_path()
            if filename:
                filenames.append(os.path.abspath(filename))
        strategy = node_context.parameters['fail_strategy'].value
        datatype = node_context.parameters['datatype'].value
        json_data = node_context.parameters['json-data'].value

        params = {'json_data': json_data,
                  'datatype': datatype,
                  'filenames': filenames,
                  'sys_path': repr(sys.path),
                  'cwd': os.getcwd()}

        p = self.execute_subprocess_entrypoint()
        stdout, stderr = p.communicate(
            input=base64.b64encode(json.dumps(params).encode('ascii')))
        if stderr:
            print(vs.fs_decode(vs.fs_decode(stderr)), file=sys.stderr, end='')
        pos = stdout.find(self._marker)
        print(vs.fs_decode(stdout[:pos]), end='')
        extract_results = json.loads(
            base64.b64decode(stdout[pos + len(self._marker):]).decode('ascii'))

        for extract_result in extract_results:
            filename, filename_result = extract_result
            status, flowdatas_or_error = filename_result
            if status:
                flowdatas = flowdatas_or_error
                status = self._extract_ok(flowdatas)
                if not status:
                    flowdatas_or_error = self._extract_failure_msg

            if status:
                flowdatas = flowdatas_or_error
                for flowdata in flowdatas:
                    try:
                        output = output_list.create()
                        builtin.Lambda.set_from_flowdata(output, flowdata)
                        output_list.append(output)
                    except Exception:
                        if strategy == 'error':
                            raise exceptions.SyDataError(
                                'Failed to build extracted lambda from: {}'
                                .format(filename))
                        elif strategy == 'skip':
                            pass

            elif strategy == 'error':
                raise exceptions.SyDataError(
                    'Failed to extract: {}, due to: {}'.format(
                        filename,
                        flowdatas_or_error))
            elif strategy == 'skip':
                pass

    _extract_failure_msg = 'Cannot extract flow'

    def _extract_ok(self, flows):
        return True


class ExtractFlowsLambdas(ExtractLambdas):
    """
    Extract top level Flows as Lambda functions matching datatype in flows.

    Lambda functions will change its type to reflect the choosen datatype
    as long as it is a non-generic function type and can be matched against
    connected nodes. Datatypes configured that fail to satisfy the above
    are simply be ignored.
    """

    name = 'Extract Flows as Lambdas'
    description = ('Extract top level Flows as Lambda functions matching '
                   'datatype in flows')
    nodeid = 'org.sysess.builtin.extractflowslambdas'
    author = 'Erik der Hagopian <erik.hagopian@combine.se>'
    copyright = '(C) 2016 Combine Control Systems AB'
    version = '1.0'
    icon = 'extract_one_to_one.svg'

    _subprocess_cls = 'ExtractFlowSubprocess'
    _extract_failure_msg = 'Cannot extract flow of suitable type'

    def _extract_ok(self, flows):
        if len(flows) == 1:
            return True
        return False


class Empty(Node):
    """
    This node can only run successfully if it the output port has a concrete
    type. This can be acheived either by connecting the output port to other
    nodes so that the type becomes concrete or by specifying the type in the
    configuration. For syntax and examples of how to specify port types in the
    configuration, see :ref:`custom_ports`.
    """

    author = ('Erik der Hagopian <erik.hagopian@combine.se>, '
              'Benedikt Ziegler <benedikt.ziegler@combine.se>')
    copyright = '(C) 2016 Combine Control Systems AB'
    name = 'Empty'
    description = 'Generate empty data of inferred or specified type'
    nodeid = 'org.sysess.builtin.empty'
    icon = 'empty.svg'
    version = '1.1'
    tags = Tags(Tag.Input.Generate)

    inputs = Ports([])
    outputs = Ports([Port.Custom(
        '<a>',
        'Output port containing empty data (must be connected or specified)')])

    parameters = sy_parameters()
    parameters.set_string(
        'datatype', label='Datatype',
        description='Define the datatype of the output port.', value='<a>')

    def exec_parameter_view(self, node_context):
        return TypeEditorParameterView(node_context)

    def execute(self, node_context):
        str_type = node_context.definition['ports']['outputs'][0]['type']
        arg_type = types.from_string(str_type)
        if types.generics(arg_type):
            raise exceptions.SyDataError(
                'Output port must be connected and non-generic')


class Propagate(Node):
    """Propagate input to output."""

    author = 'Erik der Hagopian <erik.hagopian@combine.se>'
    copyright = '(C) 2017 Combine Control Systems AB'
    name = 'Propagate'
    description = 'Propagate input to output'
    nodeid = 'org.sysess.builtin.propagate'
    icon = 'empty.svg'
    version = '1.0'
    tags = Tags(Tag.Hidden.Internal)

    inputs = Ports([Port.Custom('<a>', 'Input')])
    outputs = Ports([Port.Custom('<a>', 'Output')])
    parameters = sy_parameters()

    def execute(self, node_context):
        node_context.output[0].source(node_context.input[0])
