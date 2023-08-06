# This file is part of Sympathy for Data.
# Copyright (c) 2021 Combine Control Systems AB
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
import os
import re
import datetime
from collections import abc
from sympathy.platform import parameter_helper
from sympathy.platform.exceptions import sywarn
from sympathy.utils import prim
_pattern = re.compile(r'\$\((\w+)(?:=([^\(^\)]+))?\)')


def parse_variables(string):
    return _pattern.finditer(string)


def expand_variables(string: str, variables: abc.Mapping) -> str:
    """
    Expand environment variables matching $(NAME) or $(NAME=DEFAULT).
    """
    matches = parse_variables(string)
    if not matches:
        return string
    diff = 0

    # String as list to allow setitem.
    string_list = list(string)

    for match in matches:
        # Replace according to matched positions.
        name, default = match.groups()
        try:
            value = variables[name]
        except KeyError:
            if default is not None:
                value = default
            else:
                value = f'$({name})'

        start, end = match.span()
        start += diff
        end += diff

        string_list[start:end] = value
        diff += len(value) + start - end

    return ''.join(string_list)


def warning_message(msg):
    timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
    sywarn(f'{timestamp}  WARNING    {msg}\n')


class ExecutionEnvironment(abc.Mapping):

    def __init__(self, workflow_variables, shell_variables, global_variables):
        self._workflow_variables = workflow_variables
        self._shell_variables = shell_variables
        self._global_variables = global_variables

    def get(self, name, warn=False):
        value = None
        if prim.is_windows():
            value = self._shell_variables.get(name.upper())
        if value is None:
            for variables in [
                    self._shell_variables,
                    self._workflow_variables,
                    self._global_variables]:
                value = variables.get(name)
                if value is not None:
                    break
        if value is None and warn:
            # Remove this warning and simplify the code a bit?
            warning_message(
                f'Cannot find variable {name} in the environment.')
        return value

    def __getitem__(self, name):
        value = self.get(name, warn=True)
        if value is None:
            raise KeyError(name)
        else:
            return value

    def __contains__(self, name):
        return self.get(name) is not None

    def __iter__(self):
        items = {}
        for variables in [
                self._global_variables,
                self._workflow_variables,
        ]:
            items.update(dict.fromkeys(variables))

        shell_keys = self._shell_variables
        if prim.is_windows():
            shell_keys = [k.upper() for k in self._shell_variables]

        items.update(dict.fromkeys(shell_keys))
        for k in items:
            yield k

    def __len__(self):
        return len(list(iter(self)))


class Environment:
    def __init__(self):
        self.shell_variables = {}
        self.global_variables = {}
        self._base_shell = dict(os.environ)

    def set_variables(self, shell_variables, global_variables):
        self.shell_variables = dict(shell_variables)
        self.global_variables = dict(global_variables)
        os.environ.clear()
        os.environ.update(self._base_shell)
        os.environ.update(self.shell_variables)

    def execution_environment(self, workflow_variables):
        return ExecutionEnvironment(
            workflow_variables,
            self.shell_variables,
            self.global_variables)

    def expanded_node_dict(self, old_node_dict, workflow_variables):

        def inner(group):
            for key in list(group):
                subitem = group[key]
                if isinstance(subitem, parameter_helper.ParameterGroup):
                    inner(subitem)
                else:
                    try:
                        subitem._expand_variables(variables)
                    except Exception:
                        pass

        node_dict = old_node_dict
        if old_node_dict and old_node_dict.get('parameters', {}).get('data'):
            try:
                node_dict = copy.deepcopy(old_node_dict)
                data = parameter_helper.ParameterRoot(
                    node_dict['parameters']['data'])
            except Exception:
                data = None

        if data is not None:
            variables = self.execution_environment(workflow_variables)
            inner(data)
            node_dict['parameters']['data'] = data.to_dict()
        return node_dict


_instance = Environment()


def set_variables(variables):
    _instance.set_variables(*variables)


def expanded_node_dict(old_node_dict, workflow_variables):
    return _instance.expanded_node_dict(old_node_dict, workflow_variables)


def execution_environment(workflow_variables) -> abc.Mapping:
    return _instance.execution_environment(workflow_variables)


def has_variables(string):
    return next(parse_variables(string), None) is not None
