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
"""
Methods for handling global state.
"""
from sympathy.platform import node_result
from contextlib import contextmanager


__node_state = None
__cache_state = None


def node_state():
    global __node_state
    if __node_state is None:
        __node_state = NodeState()
    return __node_state


@contextmanager
def state():
    """
    Produce a fresh state to run in.
    The original state is restored when the contextmanager finishes.

    Example:

    >>> with state():
    >>>    pass  # Do something.

    This is required for example when running debug using editor plugin to make
    sure that the current context is not cleared when the new state is set up.
    Otherwise this would lead to files being closed in a very unexpected
    manner.
    """
    from sympathy.datasources.hdf5 import dsstate
    global __node_state

    old_node_state = __node_state
    old_hdf5_state = dsstate.get_hdf5_state()

    __node_state = None
    dsstate.set_hdf5_state(None)

    yield

    __node_state = old_node_state
    dsstate.set_hdf5_state(old_hdf5_state)


class Node:
    def __init__(self, instance_id):
        """
        Parameters
        ----------
        instance_id : string
            Full node uuid or arbitrary identifier string
        """
        self._instance_id = instance_id

    @property
    def identifier(self):
        return self._instance_id


class Settings(object):
    _env_lookup = {
        'node/flow_filename': 'SY_FLOW_FILEPATH',
        'node/flow_dir': 'SY_FLOW_DIR',
        'node/lib_dir': 'SY_LIBRARY_DIR'
    }

    def __init__(self, attributes):
        self._attributes = attributes

    def __getitem__(self, key):
        env_key = self._env_lookup.get(key)
        if env_key:
            try:
                return self._attributes['flow_vars'][env_key]
            except Exception:
                pass
        try:
            return self._attributes['worker_settings'][key]
        except KeyError:
            return self._attributes[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def to_dict(self):
        res = {}
        res.update(self._attributes.get('worker_settings', {}))
        flow_vars = self._attributes.get('flow_vars', {})
        res.update(flow_vars)
        for k, v in self._env_lookup.items():
            var = flow_vars.get(v)
            if var is not None:
                res[k] = var
        return res


class NodeState(object):
    def __init__(self):
        from sympathy.datasources.hdf5 import dsstate
        self.attributes = {}
        self.hdf5 = dsstate.hdf5_state()
        self.result = None

    def create(self, **kwargs):
        self.hdf5.create()
        self.attributes.update(kwargs)
        self.result = node_result.NodeResult()

    def set_attributes(self, **kwargs):
        self.attributes.update(kwargs)

    def clear(self):
        self.hdf5.clear()
        self.attributes.clear()
        self.result = None

    def cleardata(self):
        self.hdf5.clear()

    @property
    def settings(self):
        return Settings(self.attributes)
