# This file is part of Sympathy for Data.
# Copyright (c) 2013, 2017, Combine Control Systems AB
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
from sympathy.api import node_helper
from sympathy.api import qt2 as qt_compat
from sympathy.api import node as synode
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, adjust
from sylib.converters import TYPE_NAMES, CONVERSIONS

QtCore = qt_compat.QtCore
QtGui = qt_compat.import_module('QtGui')
QtWidgets = qt_compat.import_module('QtWidgets')


DOCS = """
With the considered node it is possible to convert the data types of a number
of selected columns in the incoming Table. In general, the columns in the
internal :ref:`Table` type can have the same data types that exist for numpy
arrays, except for numpy object type. For this node the list of available data
types to convert to is restricted.

The following data types are available for conversion:
    - binary
    - bool
    - datetime (UTC or naive)
    - float
    - integer
    - text


Converting strings to datetimes
-------------------------------
Converting a str/unicode column to datetime might require some extra thought if
the strings include time-zone information. The datetimes stored by Sympathy
have no time zone information (due to limitations in the underlying data
libraries), but Sympathy is able to use the time-zone information when creating
the datetime columns. This can be done in two different ways, which we call
"UTC" and "naive".

datetime (UTC)
##############
The option *datetime (UTC)* will calculate the UTC-time corresponding to each
datetime in the input column. This is especially useful when your data contains
datetimes from different time zones (a common reason for this is daylight
savings time), but when looking in the viewer, exports etc. the datetimes will
not be the same as in the input.

For example the string ``'2016-01-01T12:00:00+0100'`` will be stored as
``2016-01-01T11:00:00`` which is the corresponding UTC time.

There is currently no standard way of converting these UTC datetimes back to
the localized datetime strings with time-zone information.

datetime (naive)
################
The option *datetime (naive)* simply discards any time-zone information. This
corresponds pretty well to how we "naively" think of time when looking at a
clock on the wall.

For example the string ``'2016-01-01T12:00:00+0100'`` will be stored as
``2016-01-01T12:00:00``.

Text vs. binary
---------------
Text data is a string of arbitrary characters from any writing system. Binary
data on the other hand is a series of bytes as they would be stored in a
computer. Text data can be converted to binary data and vice versa by choosing
one of several different character encodings. The character encoding maps the
characters onto series of bytes, but many encodings only support some subset of
all the different writing systems.

This node currently only supports the ASCII encoding, which means that only the
letters a-z (lower and upper case), as well as digits and a limited number of
punctuation characters can be converted. Trying to convert a string with any
other characters will lead to errors.
"""


class ConvertColumnsTable(synode.Node):
    __doc__ = DOCS
    author = 'Erik der Hagopian'
    description = 'Convert selected columns to specified data type'
    icon = 'select_table_columns.svg'
    name = 'Convert columns in Table'
    nodeid = 'org.sysess.sympathy.data.table.convertcolumnstable'
    tags = Tags(Tag.DataProcessing.TransformData)

    inputs = Ports([Port.Table('Input')])
    outputs = Ports([Port.Table('Output')])

    parameters = synode.parameters()
    editor = synode.Util.multilist_editor(edit=True)
    parameters.set_list(
        'columns', label='Columns',
        description='Columns that should be converted.',
        value=[], editor=editor)
    editor = synode.Util.combo_editor()
    parameters.set_list(
        'types', label='Target type',
        description='The type that these columns should be converted to.',
        list=list(sorted(TYPE_NAMES.values())),
        value_names=['text'],
        editor=editor)

    def adjust_parameters(self, node_context):
        adjust(node_context.parameters['columns'], node_context.input[0])

    def execute(self, node_context):
        in_table = node_context.input[0]
        out_table = node_context.output[0]
        self.convert_columns(
            in_table, out_table, node_context.parameters['columns'],
            self.conversion(node_context.parameters['types'].selected),
            self.set_progress)

    @staticmethod
    def conversion(type_):
        for k, v in TYPE_NAMES.items():
            if v == type_:
                return CONVERSIONS[k][None]
        assert False, 'Unknown conversion: "{}".'.format(type_)

    @staticmethod
    def convert_columns(input_table, output_table, parameter, conversion,
                        set_progress):
        output_table.set_name(input_table.get_name())
        output_table.set_attributes(input_table.get_attributes())
        column_names = input_table.column_names()
        selected_names = set(parameter.selected_names(column_names))
        n_column_names = len(column_names)

        for i, name in enumerate(column_names):
            set_progress(i * (100. / n_column_names))
            if name in selected_names:
                output_table.set_column_from_array(
                    name, conversion(input_table.get_column_to_array(name)))
                output_table.set_column_attributes(
                    name, input_table.get_column_attributes(name))
            else:
                output_table.update_column(name, input_table, name)


@node_helper.list_node_decorator(input_keys=[0], output_keys=[0])
class ConvertColumnsTables(ConvertColumnsTable):
    name = 'Convert columns in Tables'
    nodeid = 'org.sysess.sympathy.data.table.convertcolumnstables'
