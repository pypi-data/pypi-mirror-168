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
import datetime
import json
import copy
from sympathy.platform import exceptions
from sympathy.platform.parameter_types import Connection
from sympathy.utils.event import Event
from sympathy.utils.context import deprecated_function
from sympathy.utils import environment
from sympathy.platform import state
from sympathy.platform.exceptions import sywarn
from sympathy.utils.prim import combined_key, parse_isoformat_datetime
from sympathy.utils import log


node_logger = log.get_logger('node')


def _is_nan(a):
    return isinstance(a, float) and a != a


class ParameterEntity:
    __slots__ = ('_name', 'value_changed')
    _parameter_type = None

    # Adding keywords here will make their names unusable for child parameters
    # in ParameterGroups. That would be a non-compatible change.
    def __init__(self, name='',
                 label='', description='', order=None,
                 state_settings=None, gui_visitor=None, binding=None,
                 type=None,
                 **kwargs):

        super().__init__()
        self._state_settings = (state.node_state().settings.to_dict()
                                if state_settings is None
                                else state_settings)
        self._gui_visitor = gui_visitor
        self._binding = binding

        self.name = name
        if type:
            assert type == self._parameter_type
        self._type = self._parameter_type

        self.order = order

        self._label = label
        self._description = description
        self._order = order

        self.value_changed = Event()

    def to_dict(self):
        res = {
            'label': self.label,
            'description': self.description,
            'type': self.type,
        }
        if self._binding_ is not None:
            res['binding'] = self._binding
        if self.order is not None:
            res['order'] = self.order
        return res

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def label(self):
        return self._label or ""

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def description(self):
        return self._description or ""

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        self._order = order

    def gui(self):
        if self._gui_visitor is None:
            raise ValueError('Gui visitor must be set before building GUI.')
        return self.accept(self._gui_visitor)

    def as_dict(self):
        raise NotImplementedError("Must extend this method!")

    def adjust(self, names):
        raise NotImplementedError("adjust is not defined for this type.")

    def equal_to(self, other, as_stored=False):
        """
        Parameters
        ----------
        other: ParameterEntity
            Parameter to compare for equality against self.
        as_stored : bool
            Compare the parameters as they are stored in a .syx file.
            This removes descriptions and other fields that are not considered
            part of the value from the comparison.

        Returns
        -------
        bool
            True if two parameters are equal and False otherwise.
        """
        if as_stored:
            return (
                self.type == other.type and
                self._binding == other._binding)
        else:
            raise NotImplementedError

    @property
    def _binding(self):
        return self._binding_

    @_binding.setter
    def _binding(self, value):
        self._binding_ = value

    @classmethod
    def _update_dict(cls, parameter_dict):
        """
        Used for updates to the parameter_dict before passing to constructor
        via from_dict. For example to parse and replace value.

        When modifying, return a copy and unsure original is unchanged.
        """
        return parameter_dict

    @classmethod
    def from_dict(cls, parameter_dict, **kwargs):
        """
        Used to build from existing parameters.

        Intended for internal use.

        Deserialization of parameters should use ParameterRoot.
        """
        type = parameter_dict.get('type')
        assert not type or type == cls._parameter_type
        updated_dict = cls._update_dict(parameter_dict)
        obj = cls(**updated_dict, **kwargs)
        return obj

    def _expand_variables(self, variables):
        """
        Use variables in env to expand the value of parameter.
        Return True if any expansion took placed and False otherwise.

        Intended for internal use.
        """
        return False

    def _format_require(self) -> str:
        return f'{self.label} is required.'

    def _bool(self) -> bool:
        """
        Intended for internal use.
        """
        raise NotImplementedError()

    def _require(self, text: str = None):
        """
        Intended for internal use.
        """
        if not self._bool():
            raise exceptions.SyConfigurationError(
                self._format_require())
        return self

    def _set_gui_visitor(self, gui_visitor):
        """
        Intended for internal use.
        """
        self._gui_visitor = gui_visitor


class ParameterValue(ParameterEntity):
    """docstring for ParameterValue"""
    _value_type = None

    def __init__(self, value, editor=None, **kwargs):
        super().__init__(**kwargs)
        self._value = value
        self.editor = editor

    def _check_value_type(self, value):
        if self._value_type:
            if value is not None and not isinstance(value, self._value_type):
                if isinstance(value, int) and self._value_type is float:
                    return
                name = self.name or 'parameter'
                node_logger.warning(
                    'Mismatched type: value of %s parameter "%s" is %s (%s).',
                    self._value_type.__name__, name, repr(value),
                    type(value).__name__)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._check_value_type(value)
        self._value = value
        self.value_changed.emit()

    @property
    def editor(self):
        return copy.deepcopy(self._editor)

    @editor.setter
    def editor(self, item):
        if isinstance(item, Editor):
            item = item.value()
        self._editor = copy.deepcopy(item)

    def to_dict(self):
        res = super().to_dict()
        res['value'] = self.value
        res['editor'] = self.editor
        return res

    def as_dict(self):
        return ({
            "type": self.type,
            "value": self.value})

    def __str__(self):
        return str({
            "type": self.type,
            "value": self.value})

    def equal_to(self, other, as_stored=False):
        return (
            super().equal_to(other, as_stored=as_stored) and
            self.value == other.value)

    def _adjust_scalar_combo(self, values):
        if self._editor and self._editor['type'] == 'combobox':
            include_empty = self._editor.get('include_empty', False)
            if isinstance(values, dict):
                options = list(values.keys())
                display = list(values.values())
            else:
                display = None
                options = list(values)
            if include_empty:
                options.insert(0, '')
                if display is not None:
                    display.insert(0, '')
            self._editor['options'] = options
            self._editor['display'] = display


class ParameterInteger(ParameterValue):
    _parameter_type = "integer"
    _value_type = int

    def __init__(self, value=0, **kwargs):
        super().__init__(value, **kwargs)

    def accept(self, visitor):
        return visitor.visit_integer(self)

    def adjust(self, values):
        self._adjust_scalar_combo(values)


class ParameterFloat(ParameterValue):
    _parameter_type = "float"
    _value_type = float

    def __init__(self, value=0, **kwargs):
        super().__init__(value, **kwargs)

    def accept(self, visitor):
        return visitor.visit_float(self)

    def adjust(self, values):
        self._adjust_scalar_combo(values)

    def equal_to(self, other, as_stored=False):
        # super call intentionally skips direct parent.
        return (
            super(ParameterValue, self).equal_to(
                other, as_stored=as_stored) and
            (self.value == other.value or
             _is_nan(self.value) and _is_nan(other.value)))


class ParameterString(ParameterValue):
    _parameter_type = "string"
    _value_type = str

    def __init__(self, value="", **kwargs):
        super().__init__(value, **kwargs)

    def accept(self, visitor):
        return visitor.visit_string(self)

    def adjust(self, values):
        self._adjust_scalar_combo(values)

    def _expand_variables(self, variables):
        res = False
        old_value = self.value
        if old_value is not None:
            new_value = environment.expand_variables(old_value, variables)
            if old_value != new_value:
                self.value = new_value
                res = True
        return res

    def _bool(self):
        """
        Intended for internal use.
        """
        return bool(self.value)


class ParameterBoolean(ParameterValue):
    _parameter_type = "boolean"
    _value_type = bool

    def __init__(self, value=False, **kwargs):
        super().__init__(value, **kwargs)

    def accept(self, visitor):
        return visitor.visit_boolean(self)


class ParameterDateTime(ParameterValue):
    _parameter_type = "datetime"
    _value_type = datetime.datetime

    def __init__(self, value=False, **kwargs):
        super().__init__(value.isoformat(), **kwargs)

    @property
    def value(self):
        return parse_isoformat_datetime(self._value)

    @value.setter
    def value(self, value):
        self._check_value_type(value)
        self._value = value.isoformat()
        self.value_changed.emit()

    def accept(self, visitor):
        return visitor.visit_datetime(self)

    @classmethod
    def _update_dict(cls, parameter_dict):
        parameter_dict = dict(parameter_dict)
        parameter_dict['value'] = parse_isoformat_datetime(
            parameter_dict['value'])
        return parameter_dict

    def to_dict(self):
        res = super().to_dict()
        res['value'] = self._value
        return res


class ParameterJson(ParameterValue):
    _parameter_type = "json"
    _value_type = object

    def __init__(self, value=None, **kwargs):
        super().__init__(value, **kwargs)

    def accept(self, visitor):
        return visitor.visit_json(self)

    def adjust(self, values):
        pass

    @property
    def value(self):
        return copy.deepcopy(super().value)

    @value.setter
    def value(self, value):
        ParameterValue.value.fset(self, copy.deepcopy(value))

    def equal_to(self, other, as_stored=False):
        nan = object()

        def parse_constant_nan(value):
            # Replace 'NaN' with object nan so two different values
            # become equal.
            if value == 'NaN':
                value = nan
            return value

        # super call intentionally skips direct parent.
        return (
            super(ParameterValue, self).equal_to(
                other, as_stored=as_stored) and (
                    json.loads(json.dumps(self._value),
                               parse_constant=parse_constant_nan) ==
                    json.loads(json.dumps(other.value),
                               parse_constant=parse_constant_nan)))


class ParameterConnection(ParameterValue):
    _parameter_type = "connection"
    _value_type = Connection

    def __init__(self, value=Connection(), **kwargs):
        super().__init__(value.to_dict(), **kwargs)

    @property
    def value(self):
        return Connection.from_dict(self._value)

    @value.setter
    def value(self, value):
        self._value = value.to_dict()
        self.value_changed.emit()

    def accept(self, visitor):
        return visitor.visit_connection(self)

    @classmethod
    def _update_dict(cls, parameter_dict):
        parameter_dict = dict(parameter_dict)
        parameter_dict['value'] = Connection.from_dict(parameter_dict['value'])
        return parameter_dict

    def _expand_variables(self, variables):
        res = False
        old_resource = self.value.resource
        new_resource = environment.expand_variables(old_resource, variables)
        if old_resource != new_resource:
            self.value = Connection(
                resource=new_resource,
                credentials=self.value.credentials)
            res = True
        return res

    def to_dict(self):
        res = super().to_dict()
        res['value'] = self._value
        return res


_list = list


class ParameterList(ParameterEntity):
    """ParameterList"""
    _parameter_type = 'list'
    # Only for access by views.
    _mode_selected = 'selected'
    _mode_selected_exists = 'selected_exists'
    _mode_unselected = 'unselected'
    _mode_passthrough = 'passthrough'

    def __init__(self, list=None, value=None, editor=None, **kwargs):
        # Rename list argument to _list and restore list to builtin.
        list_ = list
        super().__init__(**kwargs)
        self.editor = editor
        self.multiselect_mode = kwargs.get('mode', self._mode_selected)
        self._passthrough = kwargs.get('passthrough', False)
        self._old_list_storage = kwargs.get('_old_list_storage')

        value_names = kwargs.get('value_names')
        self._list = copy.deepcopy(list_)

        if value is None and value_names is None and list_:
            # When a list has been specified, but neither value nor
            # value_names are specified, select first element. This is
            # for backwards compatibility.
            value = [0]

        if value_names:
            value = self._build_value(value_names)

        elif value:
            try:
                value_names = [list_[i] for i in value]
            except IndexError:
                value = []
                value_names = []
        else:
            value = []
            value_names = []
        self._value = value
        self._value_names_ = value_names

    def selected_names(self, names):
        """
        Return the selected names depending on the multselect mode,
        the actual selection (self.value_names) and the supplied names.

        names should be a list or iterable containing the relevant
        names. Typically this would be the names that are used to
        set self.list in adjust_parameters, the argument makes it
        possible to return different names when iterating over a
        structure where the relevant names change.
        """
        res = []
        if self.multiselect_mode == self._mode_selected:
            res = self.value_names
            missing = set(res).difference(names)
            if missing:
                name = self.label or self.name
                raise exceptions.SyDataError(
                    'Names that should exist for "{}" are missing: "{}"'
                    .format(
                        name,
                        ', '.join(sorted(missing, key=combined_key))))
        elif self.multiselect_mode == self._mode_selected_exists:
            res = [name for name in self.value_names if name in names]
        elif self.multiselect_mode == self._mode_unselected:
            res = [name for name in names if name not in self.value_names]
        elif self.multiselect_mode == self._mode_passthrough:
            res = names
        else:
            assert False, 'selected_names got unknown mode.'

        order = dict(zip(names, range(len(names))))
        return sorted(res, key=lambda x: order[x])

    @property
    def _old_list_storage(self):
        return self._old_list_storage_ or False

    @_old_list_storage.setter
    def _old_list_storage(self, value):
        self._old_list_storage_ = value

    @property
    def _passthrough(self):
        return self.multiselect_mode == self._mode_passthrough

    @_passthrough.setter
    def _passthrough(self, passthrough_):
        if passthrough_:
            self.multiselect_mode = self._mode_passthrough

    # Only for access by views.
    @property
    @deprecated_function('5.0.0', 'ParameterList.multiselect_mode')
    def _multiselect_mode(self):
        return self.multiselect_mode

    # Only for access by views.
    @_multiselect_mode.setter
    @deprecated_function('5.0.0', 'ParameterList.multiselect_mode')
    def _multiselect_mode(self, value):
        self.multiselect_mode = value

    @property
    def multiselect_mode(self):
        return self._multiselect_mode_

    @multiselect_mode.setter
    def multiselect_mode(self, value):
        self._multiselect_mode_ = value
        self.value_changed.emit()

    @property
    def editor(self):
        return copy.deepcopy(self._editor)

    @editor.setter
    def editor(self, item):
        if isinstance(item, Editor):
            item = item.value()
        self._editor = copy.deepcopy(item)

    def accept(self, visitor):
        return visitor.visit_list(self)

    def adjust(self, names):
        self.list = names

    def equal_to(self, other, as_stored=False):
        equal = (
            super().equal_to(other, as_stored=as_stored) and
            self.value_names == other.value_names and
            self.multiselect_mode == other.multiselect_mode)
        if equal and (self._old_list_storage or other._old_list_storage):
            equal &= self.list == other.list
        return equal

    @property
    def selected(self):
        """Return the first selected item in the value list,
        does not support multi-select."""
        try:
            return self.value_names[0]
        except IndexError:
            return None

    @selected.setter
    def selected(self, item):
        if item is None:
            self.value_names = []
        else:
            self.value_names = [item]

    def _value_names(self):
        """Internal value_names access"""
        return self._value_names_

    def _build_value(self, value_names):
        # Lookup could be cached to save work.
        list_ = self._list
        try:
            lookup = dict(zip(list_, range(len(list_))))
            return [lookup[v]
                    for v in value_names if v in lookup]
        except TypeError:
            # Slow lookup for deprecated cases where list could contain lists,
            # which are unhashable.
            return [list_.index(v) for v in list_]

    @property
    def value(self):
        return self._build_value(self._value_names())

    @value.setter
    def value(self, value):
        assert isinstance(value, list), 'Guard against accidental iterators.'
        list_ = self._list
        value_names = [list_[i] for i in value]
        self.value_names = value_names

    @property
    def value_names(self):
        try:
            return list(self._value_names())
        except KeyError:
            # This can happen during initiation of the parameter.
            return []

    @value_names.setter
    def value_names(self, value_names):
        new_value_names = value_names[:]
        self._value_names_ = new_value_names
        self._value = self._build_value(new_value_names)
        self.value_changed.emit()

    @property
    def list(self):
        return self._list[:]

    @list.setter
    def list(self, plist):
        if not isinstance(plist, list):
            plist = list(plist)

        self._list = plist[:]
        # Update self.value:
        self._value = self._build_value(self._value_names())
        # Should it be possible to change list without triggering
        # value_changed?  For parameter not using old_list_storage the value
        # should be determined by .value_names, .list could be seen as an
        # internal state.
        self.value_changed.emit()

    @classmethod
    def _update_dict(cls, parameter_dict):
        parameter_dict = dict(parameter_dict)
        value = parameter_dict.get('value')

        if value:
            # Update value_names from value if value is valid.
            list_ = parameter_dict['list'] or []
            value_names = parameter_dict.get('value_names')
            try:
                value_names_ = [list_[i] for i in value]
            except IndexError:
                value_names_ = None
            except TypeError:
                value_names_ = None
            # Choose value_names_ only if value_names is empty
            if value_names_ and not value_names:
                value_names = value_names_
            parameter_dict['value_names'] = value_names
        parameter_dict['value'] = None
        return parameter_dict

    def _bool(self):
        """
        Intended for internal use.
        """
        return bool(self.value_names)

    def to_dict(self):
        res = super().to_dict()
        res.update({
            'list': self.list,
            'value': self.value,
            'value_names': self.value_names,
            'mode': self.multiselect_mode,
            'editor': self.editor,
        })
        if self._old_list_storage_ is not None:
            res['_old_list_storage'] = self._old_list_storage
        return res


def update_list_dict(parameter_dict):
    parameter = ParameterList.from_dict(parameter_dict)
    parameter.name = '<name>'


class ParameterGroup(ParameterEntity):
    _parameter_type = "group"
    # Should be kept up to date with reserved kwargs in super().__init__.
    _reserved = set([
        'label',
        'description',
        'order',
        'state_settings',
        'gui_visitor',
        'type',
        'binding',
        ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._subgroups = {}

    def trigger_value_changed(self):
        self.value_changed.emit()

    def add_handler_to_subgroup(self, subgroup):
        if (hasattr(subgroup, 'value_changed') and
                isinstance(subgroup.value_changed, Event)):
            subgroup.value_changed.add_handler(self.trigger_value_changed)

    def _create_group(self, value_class, name=None, **kwargs):
        self._check_name(name)
        if name in self._subgroups:
            assert False, (
                f'Set of existing group ({name}). '
                'This is not allowed in 3.0.0')
        else:
            self[name] = value_class(
                gui_visitor=self._gui_visitor, **kwargs)
        return self._subgroups[name]

    def create_group(self, name, label="", order=None):
        return self._create_group(
            ParameterGroup, name=name, label=label, order=order)

    def create_page(self, name, label="", order=None):
        return self._create_group(
            ParameterPage, name=name, label=label, order=order)

    def set_integer(self, name, value=0, label="",
                    description="", order=None, **kwargs):
        self._set_parameter(ParameterInteger, name, value=value, label=label,
                            description=description, order=order, **kwargs)

    def set_float(self, name, value=0.0, label="",
                  description="", order=None, **kwargs):
        self._set_parameter(ParameterFloat, name, value=value, label=label,
                            description=description, order=order, **kwargs)

    def set_string(self, name, value="", label="",
                   description="", order=None, **kwargs):
        self._set_parameter(ParameterString, name, value=value, label=label,
                            description=description, order=order, **kwargs)

    def set_boolean(self, name, value=False, label="",
                    description="", order=None, **kwargs):
        self._set_parameter(ParameterBoolean, name, value=value, label=label,
                            description=description, order=order, **kwargs)

    def set_json(self, name, value=None, label="",
                 description="", order=None, **kwargs):
        self._set_parameter(ParameterJson, name, value=value, label=label,
                            description=description, order=order, **kwargs)

    def set_datetime(self, name, value=None, label="",
                     description="", order=None, **kwargs):
        if value is None:
            value = datetime.datetime.now()
        self._set_parameter(ParameterDateTime, name, value=value, label=label,
                            description=description, order=order, **kwargs)

    def set_connection(self, name, value=Connection(), label="",
                       description="", order=None, **kwargs):
        self._set_parameter(
            ParameterConnection, name, value=value, label=label,
            description=description, order=order, **kwargs)

    def set_list(self, name, plist=None, value=None, label="",
                 description="", order=None, list=None, value_names=None,
                 **kwargs):
        # Rename list argument to _list and restore list to builtin.
        list_ = list
        list = _list
        if plist is not None and list_ is not None:
            raise ValueError(
                "Only one of the arguments 'list' and 'plist' may be "
                "used at a time.")
        elif plist is None:
            plist = list_ or []
        if not isinstance(plist, list):
            plist = list(plist)

        if value is not None and value_names is not None:
            sywarn("Only one of the arguments 'value' and 'value_names' "
                   "may be used at a time")

        return self._set_parameter(
            ParameterList, name, list=plist, value=value,
            label=label, description=description, order=order,
            state_settings=self._state_settings, value_names=value_names,
            **kwargs)

    def set_custom(self, custom_handler, name, **kwargs):
        sywarn("Custom parameters are no longer supported!")

    def value_or_default(self, name, default):
        try:
            return self._subgroups[name].value
        except KeyError:
            return default

    def value_or_empty(self, name):
        return self.value_or_default(name, '')

    def keys(self):
        nextorder = self._nextorder()

        return sorted(
            self._subgroups.keys(),
            key=lambda sub: (nextorder if self._subgroups[sub].order is None
                             else self._subgroups[sub].order))

    def _nextorder(self):
        orders = [item.order
                  for item in self._subgroups.values()]
        orders = [order for order in orders if order is not None]
        if orders:
            return max(orders) + 1
        return 0

    def children(self):
        nextorder = self._nextorder()

        return sorted(
            self._subgroups.values(),
            key=lambda sub: nextorder if sub.order is None else sub.order)

    def reorder(self):
        items = self._subgroups.values()
        if items:
            nextorder = self._nextorder()
            orders = [nextorder if item.order is None else item.order
                      for item in items]

            for i, (order, item) in enumerate(sorted(
                    zip(orders, items), key=lambda x: x[0])):
                item.order = i
                if isinstance(item, ParameterGroup):
                    item.reorder()

    def gui(self, controllers=None):
        if self._gui_visitor is None:
            raise ValueError('Gui visitor must be set before building GUI.')
        return self._gui_visitor.visit_group(
            self, controllers=controllers)

    def accept(self, visitor):
        return visitor.visit_group(self)

    def equal_to(self, other, as_stored=False):
        return (
            super().equal_to(other, as_stored=as_stored) and
            set(self.keys()) == set(other.keys()) and
            all(self[k].equal_to(other[k], as_stored=True)
                for k in self.keys()))

    def _check_name(self, name):
        assert name is not None, 'Parameter name can not be None'
        assert name, 'Parameter name can not be empty'
        assert name not in self._reserved, (
            f'Parameter name: "{name}", can not be among reserved names: '
            f'{", ".join(self._reserved)}')

    def _set_parameter(self, value_class, name=None, **kwargs):
        self._check_name(name)
        parameter = self._subgroups.get(name)
        if parameter is None:
            parameter = value_class(
                gui_visitor=self._gui_visitor, **kwargs)
            self[name] = parameter
            return parameter
        else:
            assert False, (
                f'Set of existing parameter ({name}). '
                f'This is not allowed in 3.0.0')

    def pop(self, key, default=None):
        res = default
        try:
            res = self[key]
            del self[key]
        except KeyError:
            pass
        return res

    def __delitem__(self, name):
        del self._subgroups[name]

    def __getitem__(self, name):
        return self._subgroups[name]

    def __setitem__(self, name, parameter):
        self._subgroups[name] = parameter
        parameter.name = name
        self.add_handler_to_subgroup(parameter)

    def __iter__(self):
        for name in self.keys():
            yield name

    def __contains__(self, name):
        return name in self._subgroups

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        res = super().to_dict()
        res.update({key: value.to_dict()
                    for key, value in self._subgroups.items()})
        return res

    def _set_gui_visitor(self, gui_visitor):
        """
        Intended for internal use.
        """
        self._gui_visitor = gui_visitor
        for child in self.children():
            child._set_gui_visitor(gui_visitor)


class ParameterPage(ParameterGroup):
    _parameter_type = "page"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def accept(self, visitor):
        return visitor.visit_page(self)


class ParameterRoot(ParameterGroup):
    _binding_mode_internal = 'internal'
    _binding_mode_external = 'external'

    _reserved = ParameterGroup._reserved | set(['binding_mode'])

    def __init__(self, parameter_data=None, **kwargs):
        if parameter_data is None:
            parameter_dict = {}
        elif isinstance(parameter_data, ParameterGroup):
            parameter_dict = parameter_data.to_dict()
        else:
            parameter_dict = parameter_data
        self._binding_mode = parameter_dict.get('binding_mode')
        binding = parameter_dict.get('binding')
        super().__init__(binding=binding, **kwargs)
        self.name = 'root'
        _builder.build(self, parameter_dict, self._gui_visitor)

    def accept(self, visitor):
        return visitor.visit_root(self)

    def gui(self, controllers=None):
        if self._gui_visitor is None:
            raise ValueError('Gui visitor must be set before building GUI.')
        return self._gui_visitor.visit_root(
            self, controllers=controllers)

    @property
    def _binding_mode(self):
        return self._binding_mode_

    @_binding_mode.setter
    def _binding_mode(self, value):
        if value is not None:
            assert value in [
                self._binding_mode_internal, self._binding_mode_external]
        self._binding_mode_ = value

    def equal_to(self, other, as_stored=False):
        return (
            super().equal_to(other, as_stored=as_stored) and
            self._binding_mode == other._binding_mode)

    def _bool(self):
        """
        Intended for internal use.
        """
        return bool(self._subgroups)

    def to_dict(self):
        res = super().to_dict()
        if self._binding_mode_ is not None:
            res['binding_mode'] = self._binding_mode
        return res


class ParameterBuilder:
    """ParameterBuilder"""
    def __init__(self):
        super().__init__()
        self._parameter_values = {}
        for parameter_cls in [
                ParameterInteger,
                ParameterFloat,
                ParameterString,
                ParameterBoolean,
                ParameterDateTime,
                ParameterJson,
                ParameterConnection]:
            self._parameter_values[
                parameter_cls._parameter_type] = parameter_cls

    def build(self, parameter_group, parameter_dict, gui_visitor):
        for name, value in parameter_dict.items():
            if isinstance(value, dict) and value.get('type'):
                self._factory(parameter_group, name, value, gui_visitor)

    def _factory(self, parameter_group, name, value_dict, gui_visitor):
        parameter_type = value_dict['type']
        if parameter_type == "group":
            new_group = ParameterGroup.from_dict(
                value_dict, gui_visitor=gui_visitor)
            parameter_group[name] = new_group
            # Build groups recursively
            _builder.build(new_group, value_dict, gui_visitor)
        elif parameter_type == "page":
            new_page = ParameterPage.from_dict(
                value_dict, gui_visitor=gui_visitor)
            # Build groups recursively
            parameter_group[name] = new_page
            _builder.build(new_page, value_dict, gui_visitor)
        elif parameter_type in self._parameter_values:
            parameter_cls = self._parameter_values[parameter_type]
            parameter_obj = parameter_cls.from_dict(
                value_dict, gui_visitor=gui_visitor)
            parameter_group[name] = parameter_obj
        elif parameter_type == "list":
            parameter_list = ParameterList.from_dict(
                value_dict, gui_visitor=gui_visitor)
            parameter_group[name] = parameter_list
        elif parameter_type == "custom":
            sywarn("Custom parameters are no longer supported!")
        else:
            assert isinstance(parameter_type, str)
            # Assume that we have encountered a parameter type that was added
            # in a later Sympathy version.
            node_logger.debug(
                'Ignoring parameter: "%s" of unknown type: "%s". '
                'This might cause unintended behavior. To be safe, use the '
                'most recent Sympathy version used to configure the node.',
                name, parameter_type)

    def get_parameter_cls(self, parameter_type):
        return self._parameter_values.get(parameter_type)


_builder = ParameterBuilder()


def get_parameter_cls(parameter_type):
    """
    Return class for parameter_type, limited to ParameterValue instances.
    This may change.
    """
    return _builder.get_parameter_cls(parameter_type)


class Editor:
    def __init__(self, editor1=None, editor2=None):
        self.attr = {}
        if editor1 is not None:
            self.attr.update(editor1.attr)
        if editor2 is not None:
            self.attr.update(editor2.attr)

    def set_type(self, etype):
        self.attr['type'] = etype

    def set_attribute(self, attribute, value):
        self.attr[attribute] = value

    def __setitem__(self, key, value):
        self.attr[key] = value

    def __getitem__(self, key):
        return self.attr[key]

    def value(self):
        return self.attr


class Editors:
    @staticmethod
    def _bounded_editor(min_, max_):
        editor = Editor()
        editor.set_attribute('min', min_)
        editor.set_attribute('max', max_)
        return editor

    @staticmethod
    def _decimal_editor(decimals):
        editor = Editor()
        editor.set_attribute('decimals', decimals)
        return editor

    @staticmethod
    def lineedit_editor(placeholder=None):
        editor = Editor()
        editor.set_type('lineedit')
        if placeholder is not None:
            editor.set_attribute('placeholder', placeholder)
        return editor

    @staticmethod
    def textedit_editor():
        editor = Editor()
        editor.set_type('textedit')
        return editor

    @staticmethod
    def table_editor(headers, types, unique=None):
        """
        Table editor with fixed headers.

        Parameters
        ----------
        headers : list of str
        types : list of str
        """
        assert headers and types, 'headers and types are required'

        headers = list(headers)
        types = list(types)

        assert len(headers) == len(types), (
            'headers and types must have the same length')

        assert len(headers) == len(set(headers)), (
            'header names cannot repeat')

        if unique:
            unique = list(unique)
            assert headers and all(u in headers for u in unique), (
                'unique columns must be among headers')

        editor = Editor()
        editor.set_type('table')
        editor.set_attribute('headers', headers)
        editor.set_attribute('types', types)
        editor.set_attribute('unique', unique)
        return editor

    @staticmethod
    def connection_editor(modes=None):
        """
        Connection editor
        """
        editor = Editor()
        editor.set_type('connection')
        if modes:
            editor.set_attribute('modes', list(modes))
        return editor

    @staticmethod
    def azure_connection_editor():
        """
        Azure-connection editor
        """
        editor = Editor()
        editor.set_type('azure')
        return editor

    @staticmethod
    def code_editor(language='python'):
        editor = Editor()
        editor.set_type('code')
        editor.set_attribute('language', language)
        return editor

    @staticmethod
    def bounded_lineedit_editor(min_, max_, placeholder=None):
        return Editor(Editors.lineedit_editor(placeholder),
                      Editors._bounded_editor(min_, max_))

    @staticmethod
    def spinbox_editor(step):
        editor = Editor()
        editor.set_type('spinbox')
        editor.set_attribute('step', step)
        return editor

    @staticmethod
    def bounded_spinbox_editor(min_, max_, step):
        editor = Editor(Editors.spinbox_editor(step),
                        Editors._bounded_editor(min_, max_))
        return editor

    @staticmethod
    def decimal_spinbox_editor(step, decimals):
        editor = Editor(
            Editors.spinbox_editor(step),
            Editors._decimal_editor(decimals))
        return editor

    @staticmethod
    def bounded_decimal_spinbox_editor(min_, max_, step, decimals):
        editor = Editor(
            Editors.bounded_spinbox_editor(min_, max_, step),
            Editors._decimal_editor(decimals))
        return editor

    @staticmethod
    def filename_editor(filter_pattern=None, states=None):
        editor = Editor()
        editor.set_type('filename')
        editor.set_attribute('filter', filter_pattern or ['Any files (*)'])
        editor.set_attribute('states', states)
        return editor

    @staticmethod
    def savename_editor(filter_pattern=None, states=None):
        editor = Editor()
        editor.set_type('savename')
        editor.set_attribute('filter', filter_pattern or ['Any files (*)'])
        editor.set_attribute('states', states)
        return editor

    @staticmethod
    def directory_editor(states=None):
        editor = Editor()
        editor.set_type('dirname')
        editor.set_attribute('states', states)
        return editor

    @staticmethod
    def list_editor(**kwargs):
        editor = Editor()
        editor.set_type('listview')
        editor.set_attribute('edit', False)
        editor.attr.update(kwargs)
        return editor

    @staticmethod
    @deprecated_function('4.0.0', 'list_editor or multilist_editor')
    def selectionlist_editor(selection, **kwargs):
        editor = Editors.list_editor()
        editor.set_attribute('selection', selection)
        editor.attr.update(kwargs)
        return editor

    @staticmethod
    def multilist_editor(**kwargs):
        editor = Editors.list_editor()
        editor.set_attribute('selection', 'multi')
        editor.set_attribute('filter', True)
        editor.set_attribute('mode', True)
        editor.attr.update(kwargs)
        return editor

    @staticmethod
    def combo_editor(options=None, include_empty=False, placeholder=None,
                     **kwargs):
        """
        Options and display should only unique values (no duplicates).
        """
        if options is None:
            options = []
        if isinstance(options, dict):
            display = list(options.values())
            options = list(options.keys())
        else:
            display = None
        editor = Editor()
        editor.set_type('combobox')
        editor.set_attribute('options', options)
        editor.set_attribute('display', display)
        editor.set_attribute('include_empty', include_empty)
        editor.set_attribute('edit', False)
        editor.set_attribute('filter', False)
        editor.attr.update(kwargs)

        if placeholder is not None and editor.attr.get('edit'):
            editor.set_attribute('placeholder', placeholder)

        return editor

    @staticmethod
    def datetime_editor(date_format=None, **kwargs):
        editor = Editor()
        editor.set_type('datetime')
        editor.set_attribute('date_format', date_format)
        editor.attr.update(kwargs)
        return editor
