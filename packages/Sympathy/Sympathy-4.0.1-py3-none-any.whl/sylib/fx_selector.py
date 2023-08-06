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
"""Apply function(s) on input."""
import sys
import os.path
import html
import tempfile
from typing import Optional

from sympathy.api import fx_wrapper, ParameterView
from sympathy.utils import components
from sympathy.platform import types
from sympathy.api import qt2 as qt_compat
from sympathy.platform import os_support as oss
from sympathy.platform.version_support import format_exception
from sympathy.utils import filebase
from sympathy.api import exceptions
from sympathy.api import node


QtGui = qt_compat.import_module('QtGui')  # noqa
QtWidgets = qt_compat.import_module('QtWidgets')  # noqa
QtCore = qt_compat.QtCore  # noqa


def _datasource_filename(datasource):
    """Returns file datasource filename."""
    path = datasource.decode_path()
    if path:
        return os.path.abspath(path)


def _existing_filename(filename):
    return filename and os.path.isfile(filename)


def _datatype(node_context):
    for port in node_context.definition['ports']['inputs']:
        if port['name'] == 'port2':
            return port['type']
    assert False, 'Required port name "port2" does not exist'


def match_cls(cls, arg_type, multi):
    if multi:
        try:
            arg_type = arg_type[0]
        except Exception:
            return False

    return any([types.match(types.from_string(arg_type_, False), arg_type)
                for arg_type_ in cls.arg_types])


class PyfileWrapper:
    """Extract classes that extend a given base class (functions) from a
    python file. Used to extract function names for node_function_selector.
    """

    def __init__(self, env, arg_type, multi):
        arg_type = types.from_string(arg_type)
        if types.generics(arg_type):
            self._classes = {}
        elif env:
            self._classes = components.get_subclasses_env(
                env, fx_wrapper.Fx)
            self._classes = {
                k: v for k, v in self._classes.items()
                if match_cls(v, arg_type, multi)}
        else:
            self._classes = {}

    def get_class(self, class_name):
        """Retrieve a single class from the supplied python file.
        Raises NameError if the class doesn't exist.
        """
        try:
            return self._classes[class_name]
        except KeyError:
            raise NameError

    def function_names(self):
        """Extract the names of classes that extend the base class in the
        supplied python file.
        """
        # Only select classes that extend the base class
        return list(self._classes.keys())


def _tempwrite(filename, content, **kwargs):
    """
    Write content to filename via a replacement temporary file
    generated in the same dir to ensure that the file will be
    replaced completely or not modified, in case of error.

    `kwargs` are passed to NamedTemporaryFile.
    """
    dirname = os.path.dirname(filename)
    tmp = None
    with tempfile.NamedTemporaryFile(
            dir=dirname,
            delete=False,
            mode='w',
            **kwargs) as f:
        tmp = f.name
        f.write(content)
    try:
        os.replace(tmp, filename)
    except Exception:
        try:
            os.remove(tmp)
        except Exception:
            raise
    if tmp and os.path.isfile(tmp):
        raise Exception(f'Temp file: {tmp} was not removed.')


class FxSelectorGui(ParameterView):
    def __init__(self, node_context, get_function_names, parent=None):
        super().__init__(parent=parent)
        self._node_context = node_context
        self._get_function_names = get_function_names
        self._parameters = node_context.parameters
        layout = QtWidgets.QVBoxLayout()

        datasources = self._node_context.input.group('port1')
        self._copy_input = self._parameters['copy_input'].gui()
        layout.addWidget(self._copy_input)

        if datasources:
            datasource = datasources[0]
            enabled = datasource.is_valid()
            filename = ''
            self._functions = self._parameters['selected_functions'].gui()
            self._edit = QtWidgets.QLabel(
                '<html>Click to edit source file in an '
                '<a href="#internal">internal</a> '
                'or '
                '<a href="#external">external</a> '
                'editor.</html>')
            self._edit.setWordWrap(True)
            if enabled:
                filename = _datasource_filename(datasource)
                if not _existing_filename(filename):
                    enabled = False

            if enabled:
                tooltip = (
                    f'Edit source file, <i>{html.escape(filename)}</i>, '
                    'using <b>external</b> editor brings it up in the '
                    'system default editor and <b>internal</b> uses an '
                    'internal editor.'
                )
            else:
                self._edit.setText(
                    '<html>'
                    'Source file was unavailable when the '
                    'configuration loaded.'
                    '</html>')
                tooltip = (
                    '<html>'
                    'Edit source file requires that the input datasource port '
                    'holds the filename of an existing file.'
                    '</html>')
            self._edit.setToolTip(tooltip)
            self._edit.setEnabled(enabled)

            layout.addWidget(self._functions)
            layout.addWidget(self._edit)
            self._edit.linkActivated.connect(self._handle_edit_link_activated)

        else:
            layout.addWidget(self._parameters['code'].gui())

        self.setLayout(layout)

    def _edit_with_internal_dialog(
            self, title: str, content: str) -> Optional[str]:
        dialog = QtWidgets.QDialog()
        dialog.setWindowFlags(QtCore.Qt.Window |
                              QtCore.Qt.WindowCloseButtonHint |
                              QtCore.Qt.WindowMaximizeButtonHint)
        dialog.setWindowTitle(title)
        parameters = node.parameters()
        parameters.set_string(
            'editor', value=content,
            editor=node.editors.code_editor(language='python'))
        editor_parameter = parameters['editor']
        editor_gui = editor_parameter.gui()
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel)

        layout = QtWidgets.QVBoxLayout()
        dialog.setLayout(layout)
        layout.addWidget(editor_gui)
        layout.addWidget(button_box)

        ok_button = button_box.button(
            QtWidgets.QDialogButtonBox.Ok)
        ok_button.setText('Save')
        cancel_button = button_box.button(
            QtWidgets.QDialogButtonBox.Cancel)

        dialog.setMinimumWidth(800)
        dialog.setMinimumHeight(600)

        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        return (editor_parameter.value
                if dialog.exec_() == QtWidgets.QDialog.Accepted else None)

    def _handle_edit_link_activated(self, link):
        if link == '#internal':
            self._edit_source_internal()
        elif link == '#external':
            self._edit_source_external()

    def _edit_source_external(self):
        filename = _datasource_filename(self._node_context.input['port1'])
        oss.run_editor(filename)

    def _edit_source_internal(self):
        filename = _datasource_filename(self._node_context.input['port1'])
        basename = os.path.basename(filename)
        content = ''
        with open(filename) as f:
            content = f.read()

        new_content = self._edit_with_internal_dialog(
            f'Edit {basename}', content)

        if new_content is not None:
            prefix = f'{basename}.fx.'
            try:
                if new_content != content:
                    _tempwrite(filename, new_content, prefix=prefix)
                    fns = self._get_function_names(
                        self._node_context, reload=True)
                    old_fns = self._parameters['selected_functions'].list
                    if fns != old_fns:
                        # Tentative api.
                        self._functions.editor()._set_items(fns)
            except Exception as e:
                exceptions.sywarn(
                    f'Failure occured when saving the changes: {e}')


class FxSelector:

    def __init__(self):
        self._multi = False

    def exec_parameter_view(self, node_context):
        return FxSelectorGui(
            node_context, self._available_function_names)

    def adjust_parameters(self, node_context):
        parameters = node_context.parameters
        datasources = node_context.input.group('port1')
        if datasources:
            function_names = self._available_function_names(node_context)
            parameters['selected_functions'].adjust(function_names)

    def execute(self, node_context, set_progress):
        in_datafile = node_context.input['port2']
        parameters = node_context.parameters
        copy_input = parameters['copy_input'].value
        out_datafile = node_context.output['port3']
        functions = self._selected_functions(node_context)
        calc_count = len(functions)
        if not functions:
            exceptions.sywarn('No calculations selected.')

        tmp_datafile = filebase.empty_from_type(
            in_datafile.container_type)

        if copy_input:
            tmp_datafile.source(in_datafile)

        for i, function in enumerate(functions):
            set_progress(100.0 * i / calc_count)
            _execute(function, in_datafile, tmp_datafile)

        out_datafile.source(tmp_datafile)

    def _available_function_names(self, node_context, reload=False):
        res = []
        try:
            wrapper = self._get_wrapper(node_context, reload=reload)
            if wrapper:
                res = wrapper.function_names()
        except Exception:
            exceptions.sywarn('Unable to find available functions.')
        return res

    def _get_wrapper(self, node_context, reload=False):
        datasources = node_context.input.group('port1')
        if datasources:
            if not datasources[0].is_valid():
                return
            filename = _datasource_filename(datasources[0])
            if not _existing_filename(filename):
                return
            env = components.get_file_env(filename, reload=reload)
        else:
            env = components.get_text_env(
                node_context.parameters['code'].value)
        wrapper = PyfileWrapper(
            env,
            arg_type=_datatype(node_context), multi=self._multi)
        return wrapper

    def _selected_functions(self, node_context):
        parameters = node_context.parameters
        wrapper = self._get_wrapper(node_context)
        res = []
        if wrapper:
            available_functions = self._available_function_names(node_context)
            function_names = available_functions

            if node_context.input.group('port1'):
                function_names = (
                    parameters['selected_functions'].selected_names(
                        available_functions))

            res = [wrapper.get_class(f) for f in function_names]
        return res


def _execute(function, in_data, out_data):
    try:
        instance = function(in_data, out_data)
        instance.execute()
    except exceptions.SyUserCodeError:
        raise
    except Exception as e:
        # Remove extra rows because of the execute wrapper.
        rows = format_exception(e)
        rows[1:2] = []
        details = ''.join(rows)
        raise exceptions.SyUserCodeError(details=details)


class FxSelectorList(FxSelector):

    def __init__(self):
        super().__init__()
        self._multi = True

    def execute(self, node_context, set_progress):
        input_list = node_context.input['port2']
        parameters = node_context.parameters
        copy_input = parameters['copy_input'].value
        output_list = node_context.output['port3']
        functions = self._selected_functions(node_context)
        if not functions:
            exceptions.sywarn('No calculations selected.')

        n_inputs = len(input_list)
        n_functions = len(functions)

        for i, in_datafile in enumerate(input_list):
            try:
                input_factor = 100. / n_inputs
                set_progress(i * input_factor)

                out_datafile = input_list.create()
                if copy_input:
                    out_datafile.source(in_datafile)

                for j, function in enumerate(functions):
                    func_factor = input_factor / n_functions
                    _execute(function, in_datafile, out_datafile)
                    set_progress(i * input_factor + j * func_factor)

                output_list.append(out_datafile)
            except Exception:
                raise exceptions.SyListIndexError(i, sys.exc_info())
