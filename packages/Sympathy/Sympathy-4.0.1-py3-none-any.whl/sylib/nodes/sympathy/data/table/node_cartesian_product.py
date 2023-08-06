# This file is part of Sympathy for Data.
# Copyright (c) 2017, Combine Control Systems AB
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
from sympathy.api import node as synode
from sympathy.api import table as sytable
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sympathy.api.exceptions import SyDataError

import numpy as np
from typing import List
from itertools import combinations


common_docs = """
Cartesian product of a number of tables creates a new table
containing all combinations of rows of the inputs. This output has
one column for each unique column in the input tables. For example two
tables with columns A and B of length N and M each create a new table
of length N * M and containing A + B columns. It is an error to have
duplicate column names.
"""


def _cartesian_product(input: List[sytable.File], output: sytable.File
                       ) -> None:
    for cmb in combinations([tab.column_names() for tab in input], 2):
        if set(cmb[0]) & set(cmb[1]):
            raise SyDataError(
                "No duplicate column names allowed in input tables.")
    rows = [tab.number_of_rows() for tab in input]
    for i, tab in enumerate(input):
        row_prod_upper = np.product(rows[:i], dtype=int)
        row_prod_lower = np.product(rows[i + 1:], dtype=int)
        for column in tab.cols():
            data = np.tile(column.data.repeat(row_prod_lower), row_prod_upper)
            output.set_column_from_array(column.name, data)


class CartesianProductTable(synode.Node):
    __doc__ = common_docs

    name = "Cartesian Product Table"
    description = (
        "Cartesian product of two or more Tables into a single Table.")
    nodeid = "se.combine.sympathy.data.table.cartesian_product_table"
    author = "Mathias Broxvall"
    version = "1.0"
    icon = "cartesian_product.svg"
    tags = Tags(Tag.DataProcessing.TransformStructure)
    related = ["se.combine.sympathy.data.table.cartesian_product_tables"]

    parameters = synode.parameters()

    inputs = Ports([Port.Custom(
        "table", "Input Tables", name="in", n=(2, None))])
    outputs = Ports([Port.Table(
        "Table with cartesian product of inputs", name="out")])

    def execute(self, node_context):
        """Execute"""
        inputs = node_context.input.group("in")
        output = node_context.output["out"]
        _cartesian_product(inputs, output)


class CartesianProductTables(synode.Node):
    __doc__ = common_docs

    name = "Cartesian Product Tables"
    description = "Cartesian product of a list of Tables into a single Table."
    nodeid = "se.combine.sympathy.data.table.cartesian_product_tables"
    author = "Mathias Broxvall"
    version = "1.0"
    icon = "cartesian_product.svg"
    tags = Tags(Tag.DataProcessing.TransformStructure)
    related = ["se.combine.sympathy.data.table.cartesian_product_table"]

    parameter = synode.parameters()

    inputs = Ports([Port.Custom("[table]", "List of input tables", name="in")])
    outputs = Ports([Port.Table(
        "Table with cartesian product of inputs", name="out")])

    def execute(self, node_context):
        """Execute"""
        inputs = node_context.input["in"]
        output = node_context.output["out"]
        _cartesian_product(inputs, output)
