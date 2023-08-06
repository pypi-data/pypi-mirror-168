# This file is part of Sympathy for Data.
# Copyright (c) 2013-2016 Combine Control Systems AB
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
"""
Sympathy worker used to start Sympathy Python worker processes.
"""
import locale
import os
import sys
import json
import cProfile as profile
import copy
import io
import dask
import warnings
import contextlib

from PySide6 import QtCore, QtWidgets
from sympathy.utils.prim import uri_to_path
from sympathy.utils import network
from sympathy.utils import environment
from sympathy.platform import state
from sympathy.platform import node_result
from sympathy.platform import os_support
from sympathy.platform import editor as editor_api
from sympathy.platform import types
from sympathy.platform import message_util
from sympathy.app import builtin
from sympathy.app.config_aggregation import (
    config_aggregation_dialog, clean_flow_info)


pid = os.getpid()
_debug_worker_global = {}


def set_high_dpi_unaware():
    os_support.set_high_dpi_unaware()


def setup_qt_opengl():
    os_support.setup_qt_opengl()


def write_run_config(node_filename, node_class, uuid, run_filename,
                     data_filename, *args):
    def quote(filename):
        return filename.replace('\\', '\\\\')

    with open(data_filename, 'w') as run_data:
        json.dump(args, run_data)

    with open(run_filename, 'w') as run_config:
        run_config.write('''"""
This is a startup file for debugging the following Sympathy for Data node:

    filename = {node_filename}
    class = {node_class}
    uuid = {uuid}

It can be used to run and debug the execute method of this node.

Running this file will run {node_class}.execute() with the input ports that
were available to the node when Debug was activated from Sympathy for Data.
To use breakpoints in the execute method:

    1. Open the filename
    2. Locate the relevant execute method and place a breakpoint
    3. Run _this_ file with debugging

NOTE: The interpreter (Python) must be the same one that was used to run
Sympathy for Data.

This file is valid as long as the input port data is still available. Any
future Debug activations from within Sympathy for Data will replace the content
of this file.
"""
import json
from sympathy.app.tasks.task_worker_subprocess import (
    debug_worker, _debug_worker_global)

with open('{data_filename}') as f:
    arguments = json.load(f)
dnc = debug_node_context = debug_worker(
    _debug_worker_global, *arguments)
'''.format(data_filename=quote(data_filename),
           node_filename=quote(node_filename),
           node_class=node_class,
           uuid=uuid))


def load_typealiases(typealiases):
    if typealiases:
        for key, value in typealiases.items():
            types.manager.add_load_typealias(key, value)
            utilmod = value['util'].split(':')[0]
            __import__(utilmod)
        types.manager.load_typealiases()


def _write_result_close(socket, data):
    network.send_all(socket, data)


class PrintErrorApplication(QtWidgets.QApplication):

    def __init__(self, argv):
        super().__init__(argv)

    # TODO(erik): Overriding notify resulted in hard crash when creating node
    # configuration using QtWebEngineWidgets.QWebEngineView(). Tested on
    # PySide2==5.11.2, MacOS 10.13.6, 2018-09-26.
    # The override may not be needed anymore.
    #
    # def notify(self, obj, evt):
    #     try:
    #         return super().notify(obj, evt)
    #     except:
    #         traceback.print_exc(file=sys.stderr)
    #         return False


def debug_worker(debug_state, source_file, library_dirs, class_name,
                 identifier,
                 json_parameters, typealiases, plugins, action,
                 log_fq_filename, environ, path, python_paths, application_dir,
                 session_dir, working_dir, worker_settings):
    os.chdir(working_dir)
    environment.set_variables(environ)
    opened = debug_state.get('opened', None)
    if opened:
        opened.close()

    with state.state():
        try:
            mod = builtin.source_module(source_file)
            node = getattr(mod, class_name)()
            state.node_state().create(library_dirs=library_dirs,
                                      application_dir=application_dir,
                                      session_dir=session_dir,
                                      support_dirs=python_paths,
                                      plugins=plugins,
                                      worker_settings=worker_settings)

            typealiases = typealiases
            parameters = json.loads(json_parameters)
            load_typealiases(typealiases)

            if action == 'execute':
                node_context = node.build_execute_context(
                    parameters,
                    typealiases,
                    exclude_output=True)
                node._execute_with_context(node_context)
                return node_context
        finally:
            state.node_state().clear()


def _reset_warnings():
    for mod in list(sys.modules.values()):
        try:
            mod.__warningregistry__.clear()
        except AttributeError:
            pass


@contextlib.contextmanager
def nullcontext(obj=None):
    # Startings with Python 3.7 contextlib.nullcontext can be used instead.
    yield obj


def worker(io_bundle, nocapture, action, *args, **kwargs):
    """
    Interface function to switch between different specialized workers.
    """
    try:
        from sklearn.utils import parallel_backend as skl_backend
    except ImportError:
        skl_backend = nullcontext

    state.node_state().set_attributes(capture_output=not nocapture)

    try:
        # Dask >= 0.18.
        dask_config = dask.config.set(scheduler='single-threaded')
    except AttributeError:
        dask_config = dask.set_options(get=dask.local.get_sync)

    _reset_warnings()

    with warnings.catch_warnings(), dask_config, skl_backend('threading'):
        # TODO(erik): unify interfaces so that node worker (or at least one
        # single interface) can be called for both types.
        # This would reduce some setup code duplication.
        if action == 'aggregated_parameter_view':
            return aggregated_parameter_view_worker(
                io_bundle, action, *args, **kwargs)
        else:
            node_worker(
                io_bundle, action, *args, **kwargs)


SocketBundle = builtin.SocketBundle


def setup_socket(iobundle, blocking):
    iobundle.socket.setblocking(blocking)
    return iobundle.socket


def _check_for_unsupported_qt():
    res = None
    for mod in ['PyQt4', 'PyQt4.QtCore',
                'PyQt5', 'PyQt5.QtCore',
                'PySide2', 'PySide2.QtCore',
                'PySide', 'PySide.QtCore']:
        if mod in list(sys.modules):
            res = mod
            break
    return res


def _warn_for_unsupported_qt(unsupported_qt):
    if unsupported_qt is None:
        # We support having both PySide6 and PyQt5 in the same python
        # environment. However, we must ensure that PyQt5 is not loaded in the
        # worker process itself, since this may cause all sorts of
        # problems. Subprocesses can be used work around this limitation to
        # encapsulate PyQt5.
        unsupported_qt = _check_for_unsupported_qt()
        if unsupported_qt:
            print('WARNING: node imported an unsupported Qt framework. This '
                  f'node made use of {unsupported_qt}, but '
                  'only PySide6 is supported, please contact the developer of '
                  'the node or plugin causing this.',
                  file=sys.stderr)


def _execute_node(node, parameters, typealiases, context, result,
                  capture_output):
    node._sys_execute(parameters, typealiases)
    builtin.store_stdouterr(result, context, capture_output)


def node_worker(io_bundle, action, source_file, class_name,
                identifier, json_parameters, typealiases, plugins, working_dir,
                environ,
                library_dirs, path, python_paths,
                application_dir, session_dir,
                worker_settings,
                log_fq_filename):
    """
    Internal function called by the Sympathy platform to start
    Python processes where the node will execute.

    The returned value is a dictionary with the two following keys:
        exception_string = '' if valid is True and a string representation
            of the Exception otherwise.
        exception_trace = [] if valid is True and a list of strings
            containing the exception trace otherwise.
        output = None, on complete failure and otherwise depending on
            action. Every action has a default value and which will
            be used for the result in the exception case.
        stdout = String containing captured stdout.
        stderr = String containing captured stderr.
        valid = True if no unhandled Exception occured False otherwise.
    """
    environment.set_variables(environ)
    sys.path[:] = path
    os.chdir(working_dir)
    had_unsupported_qt = _check_for_unsupported_qt()
    context = {}
    capture_output = state.node_state().attributes['capture_output']
    result = node_result.NodeResult()

    application = None
    reader = None
    if action in ['execute_parameter_view', 'execute_port_viewer']:
        # Must create QApplication before socket to ensure that events
        # can be handled by the Eventloop.
        os_support.set_application_id()
        application = PrintErrorApplication([])  # NOQA
        QtCore.QLocale.setDefault(QtCore.QLocale('C'))
        socket = setup_socket(io_bundle, False)
        reader = message_util.SocketMessageCommunicator(socket)
    else:
        socket = setup_socket(io_bundle, True)

    socket_bundle = SocketBundle(
        socket, io_bundle.input_func, io_bundle.output_func, reader)

    builtin.capture_stdouterr(
        context, capture_output, socket_bundle, state.Node(identifier))
    try:
        state.node_state().create(library_dirs=library_dirs,
                                  application_dir=application_dir,
                                  session_dir=session_dir,
                                  support_dirs=python_paths,
                                  plugins=plugins,
                                  worker_settings=worker_settings)

        result = state.node_state().result
        parameters = json.loads(json_parameters)
        load_typealiases(typealiases)
        mod = builtin.source_module(source_file)
        node = getattr(mod, class_name)()._future__init__(
            identifier=identifier,
            definition=parameters, socket_bundle=socket_bundle)
        # name = node.name

        if action == 'execute':
            _execute_node(node, parameters, typealiases, context, result,
                          capture_output)

            with io.open(log_fq_filename, 'w', encoding='utf8') as out_file:
                out_file.write(result.format_std_output())
        elif action == 'profile':  # => 'execute'
            clean_identifier = ''.join(
                [c for c in identifier if c not in '{}'])
            stat_fq_filename = os.path.join(session_dir, '{}_{}.stat'.format(
                class_name, clean_identifier))
            result.output = ''
            # The code should be the same as performed in the 'execute' case,
            # the reason for not using a function here is to avoid adding an
            # extra level to tracebacks etc (there are already so many before
            # the user's node execute starts).
            prof = profile.Profile()
            prof.runcall(
                _execute_node, node, parameters, typealiases, context, result,
                capture_output)
            prof.dump_stats(stat_fq_filename)
        elif action == 'debug':  # => 'execute'
            clean_identifier = ''.join(
                [c for c in identifier if c not in '{}'])
            run_fq_base = os.path.join(session_dir, 'debug-node')
            log_fq_filename = f'{run_fq_base}.log'
            run_fq_filename = f'{run_fq_base}.py'
            data_fq_filename = f'{run_fq_base}.json'

            write_run_config(
                uri_to_path(source_file),
                class_name,
                identifier,
                run_fq_filename,
                data_fq_filename,
                source_file, library_dirs, class_name, identifier,
                json_parameters,
                typealiases, plugins, 'execute',
                log_fq_filename, environ, path, python_paths, application_dir,
                session_dir, working_dir, worker_settings)

            debug_file = uri_to_path(run_fq_filename)

            if editor_api.debug_file(filename=debug_file) is False:
                # TODO(erik): stdoe and exceptions are not propagated.
                print('Editor plugin which can debug is not installed.')
                print('Wrote debug-node startup file to', debug_file)

        elif action == 'validate_parameters':
            result.output = False
            result.output = node._sys_verify_parameters(
                parameters, typealiases)
        elif action == 'execute_parameter_view':
            result.output = None
            result.output = json.dumps(node._sys_exec_parameter_view(
                parameters, typealiases))
        elif action == 'test_parameter_view':
            result.output = json_parameters
            node._sys_exec_parameter_view(
                parameters, typealiases, return_widget=True)
        elif action == 'execute_port_viewer':
            result.output = True
            node.exec_port_viewer(parameters)
            builtin.store_stdouterr(result, context, capture_output)
        elif action == 'execute_library_creator':
            libraries, temp_dir = parameters
            create_result = node.create(
                libraries, temp_dir, session_dir)
            builtin.store_stdouterr(result, context, capture_output)
            result.output = create_result
        else:
            print('Unsupported node action requested.')

        created_qapplication = QtCore.QCoreApplication.instance()
        if application:
            if application.clipboard().ownsClipboard():
                os_support.flush_clipboard()
        elif created_qapplication:
            print('WARNING: node created a QApplication, this will cause hard '
                  'crashes in worker processes. Please refrain from creating '
                  'QApplications except in separate subprocesses, '
                  'using matplotlib.pyplot in F(x) is a frequent cause.',
                  file=sys.stderr)

        _warn_for_unsupported_qt(had_unsupported_qt)
    except:  # NOQA
        result.valid = False
        result.store_current_exception(source_file)
    finally:
        state.node_state().clear()

    builtin.store_stdouterr(result, context, capture_output)
    builtin.restore_stdouterr(context, capture_output)
    result.stdout_limit = worker_settings.get('max_task_chars')
    result.stderr_limit = worker_settings.get('max_task_chars')
    if log_fq_filename:
        result.limit_footer = 'Wrote full output to: {}.'.format(
            log_fq_filename)

    _write_result_close(socket, io_bundle.result_func(result))


def aggregated_parameter_view_worker(
        io_bundle, action, conf, identifier, json_flow_info, typealiases,
        plugins,
        working_dir, environ,
        library_dirs, path, python_paths,
        application_dir, session_dir,
        worker_settings):

    environment.set_variables(environ)
    os_support.set_application_id()
    sys.path[:] = path
    had_unsupported_qt = _check_for_unsupported_qt()
    os.chdir(working_dir)
    context = {}
    capture_output = state.node_state().attributes['capture_output']
    result = node_result.NodeResult()
    result.output = json_flow_info

    def add_instances(x, socket_bundle):
        for key, value in x.items():
            if key == 'nodes':
                for node_info in value:
                    source_file = node_info['source_file']
                    class_name = node_info['class_name']
                    node_dict = json.loads(node_info['json_node_dict'])
                    identifier = node_info['uuid']
                    # Extra payload fields will not be set for nodes without
                    # source_file like nodes missing in library.
                    if source_file:
                        mod = builtin.source_module(source_file)
                        node_instance = getattr(
                            mod, class_name)()._future__init__(
                                identifier=identifier,
                                definition=node_dict,
                                socket_bundle=socket_bundle)
                        # Extra payload.
                        node_info['library_node_instance'] = node_instance
                        node_info['node_context_traceback'] = None
            elif key == 'flows':
                for flw in value:
                    add_instances(flw, socket_bundle)

    application = PrintErrorApplication([])  # NOQA
    socket = setup_socket(io_bundle, False)
    reader = message_util.SocketMessageCommunicator(socket)
    socket_bundle = SocketBundle(
        socket, io_bundle.input_func, io_bundle.output_func, reader)

    builtin.capture_stdouterr(
        context, capture_output, socket_bundle, state.Node(identifier))

    # TODO: Move to top level when shiboken is no longer being imported.

    try:
        state.node_state().create(library_dirs=library_dirs,
                                  application_dir=application_dir,
                                  session_dir=session_dir,
                                  support_dirs=python_paths,
                                  plugins=plugins,
                                  worker_settings=worker_settings)
        load_typealiases(typealiases)

        flow_info = json.loads(json_flow_info)

        # Store flow info without instances.
        old_flow_info = copy.deepcopy(flow_info)

        # Manage modifications to flow_info automatically.
        # with node_instances(flow_info) as modified_flow_info:
        add_instances(flow_info, socket_bundle)
        accept = config_aggregation_dialog(
            conf,
            socket_bundle,
            flow_info,
            typealiases)
        flow_info = clean_flow_info(flow_info)

        if accept:
            result.output = json.dumps(flow_info)
        else:
            result.valid = False
            result.output = json.dumps(old_flow_info)

        if application.clipboard().ownsClipboard():
            os_support.flush_clipboard()

        _warn_for_unsupported_qt(had_unsupported_qt)
    except:  # NOQA
        result.valid = False
        result.store_current_exception()
    finally:
        state.node_state().clear()

    builtin.store_stdouterr(result, context, capture_output)
    builtin.restore_stdouterr(context, capture_output)

    result.stdout_limit = worker_settings.get('max_task_chars')
    result.stderr_limit = worker_settings.get('max_task_chars')
    _write_result_close(socket, io_bundle.result_func(result))


def main():
    json_parent_context = sys.argv[-1]
    parent_context = json.loads(json_parent_context)
    os.environ.update(parent_context['environ'])
    sys.path[:] = parent_context['sys.path']
    result = worker(*sys.argv[1:-1])
    sys.stdout.write(json.dumps(result,
                                encoding=locale.getpreferredencoding()))


if __name__ == '__main__':
    main()
