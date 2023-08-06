# This file is part of Sympathy for Data.
# Copyright (c) 2022, Combine Control Systems AB
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

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from sympathy.api import table
from sympathy.api.exceptions import SyDataError, NoDataError
from pyarrow.lib import ArrowInvalid
import pyarrow.types as ptypes


def _validate(data):
    ''' Validate parquet file. '''
    if data is None:
        raise NoDataError
    else:
        try:
            pa.Table.validate(data)
        except ArrowInvalid as e:
            raise SyDataError(e.args[0])


def read_pqfile_to_table(pq_file):
    '''
    Read parquet file to table and add column and table metadata to output
    '''
    out_table = table.File()
    try:
        data = pq.read_table(pq_file)
        _validate(data)
    except SyDataError as e:
        raise SyDataError(f'{e.args[0]} in file: {pq_file}')
    except NoDataError as e:
        raise NoDataError(f'{e.message} in file: {pq_file}')
    except ValueError as e:
        raise ValueError(f'{e} in file: {pq_file}')

    column_length = len(data.column_names)
    names = data.column_names
    out_table.set_name(pq_file)
    col_type_dict = {col: type for col, type in zip(names, data.schema.types)}

    if not column_length:
        return out_table
    if not len(names):
        names = [str(i) for i in range(column_length)]

    def filter_metadata(d: dict, rm_keys=[]):
        '''
        Remove uninteresting metadata fields from standard column metadata
        '''
        if isinstance(d, dict):
            for key in rm_keys:
                try:
                    del d[key]
                except KeyError:
                    pass
            return d
        else:
            return {}

    def get_string_representation(b):
        """
        If b is a string, return it. If b is a bytes object,
        return its string representation. Otherwise,
        return str(b)
        :param b: The bytes to be converted to a string
        :return: The string representation of the bytes object.
        """
        if b is None:
            return None
        else:
            if isinstance(b, bytes):
                return b.decode('utf-8')
            else:
                return str(b)

    # Combine relevant standard column metadata with custom column metadata
    # (opinionated)
    col_attr_fields = [
        {
            **(
                filter_metadata(
                    data.schema.field(names[i]).metadata,
                    rm_keys=[b'PARQUET:field_id'])
                if isinstance(data.schema.field(
                                names[i]).metadata, dict)
                else {} or {}
            ),
        }
        for i in range(column_length)
    ]

    col_attr = [list(i.keys()) if i is not None
                else i for i in col_attr_fields]

    for i, column in enumerate(names):
        column = column.rstrip()
        if ptypes.is_string(col_type_dict[column]):
            str_array = data[column].to_numpy().astype(str)
            output = np.ma.masked_where(str_array is None, str_array)
        elif ptypes.is_timestamp(col_type_dict[column]):
            # Convert timestamp in nanoseconds to datetime
            # supported in Sympathy (milliseconds)
            output = np.ma.masked_invalid(data[column]
                                          .to_numpy().astype('datetime64[us]'))
        else:
            output = np.ma.masked_invalid(data[column].to_numpy())
        out_table.set_column_from_array(column, output)
        if len(col_attr_fields):
            col_attrs = {}
            if not col_attr[i] == {}:
                for j in col_attr[i]:
                    value = col_attr_fields[i][j]
                    value = get_string_representation(value)
                    j = get_string_representation(j)
                    col_attrs[j] = value
            else:
                col_attrs = {}
            out_table.set_column_attributes(column, col_attrs)

    # Remove uninteresting table attributes from conversion to parquet
    # from Pandas or Spark (opinionated)
    table_attr_dict = {
        **(
            filter_metadata(
                data.schema.metadata,
                rm_keys=[b"org.apache.spark.sql.parquet.row.metadata",
                         b"pandas"],
            )
            if isinstance(data.schema.metadata, dict)
            else {} or {}
        ),
    }

    if len(table_attr_dict):
        attributes, values = list(table_attr_dict.keys()), list(
            table_attr_dict.values())
        attributes = [get_string_representation(i) for i in attributes]
        values = [get_string_representation(i) for i in values]
        out_table.set_table_attributes(dict(zip(attributes, values)))

    return out_table
