# This file is part of Sympathy for Data.
# Copyright (c) 2017 Combine Control Systems AB
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
import os

from sympathy.utils import log
from collections import abc

from sympathy.utils import environment

core_logger = log.get_logger('core')
env_logger = log.get_logger('core.env')

_instance = None


def expand_variables(string):
    return environment.expand_variables(string, instance())


class Environment(abc.Mapping):
    def __init__(self):
        self._shell_variables = {}
        self._global_variables = {}
        self._shell_variables.update(os.environ.items())

    def shell_variables(self):
        return self._shell_variables

    def global_variables(self):
        return self._global_variables

    def set_shell_variables(self, variable_dict):
        self._shell_variables.clear()
        self._shell_variables.update(variable_dict)

    def set_global_variables(self, variable_dict):
        self._global_variables.clear()
        self._global_variables.update(variable_dict)

    def __getitem__(self, name):
        return (self._shell_variables.get(name) or
                self._global_variables.get(name))

    def __contains__(self, name):
        return self[name] is not None

    def __iter__(self):
        items = {}
        items.update(dict.fromkeys(self._global_variables.keys()))
        items.update(dict.fromkeys(self._shell_variables.keys()))
        for k in items:
            yield k

    def __len__(self):
        return len(list(iter(self)))

    def to_dict(self):
        return {
            'shell': self._shell_variables,
            'global': self._global_variables,
        }

    def set_from_dict(self, data):
        self.set_global_variables(data['global'])
        self.set_shell_variables(data['shell'])


def instance():
    global _instance
    if _instance is None:
        _instance = Environment()
    return _instance
