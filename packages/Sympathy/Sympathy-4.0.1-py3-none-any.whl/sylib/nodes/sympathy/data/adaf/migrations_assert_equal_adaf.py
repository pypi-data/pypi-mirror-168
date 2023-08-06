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
from sympathy.api import node as synode
from sympathy.platform import migrations


class AssertEqualADAF300(migrations.UpdateParametersMigration):
    nodeid = 'org.sysess.sympathy.data.adaf.assertequaladaf'

    def updated_definition(self):
        parameters = synode.parameters()
        parameters.set_boolean(
            'col_order', value=True, label='Compare column order',
            description='Differing column order will trigger error')
        parameters.set_boolean(
            'col_attrs', value=True, label='Compare column attributes',
            description='Differing column attributes will trigger error')
        parameters.set_boolean(
            'tbl_names', value=True, label='Compare table names',
            description='Differing table name will trigger error')
        parameters.set_boolean(
            'tbl_attrs', value=True, label='Compare table attributes',
            description='Differing table attributes will trigger error')
        parameters.set_boolean(
            'inexact_float', value=False,
            label='Approximate comparison of floats',
            description='If any arithemtics is invovled floats should '
                        'probably be compared approximately.')
        parameters.set_float(
            'rel_tol', value=1e-5, label='Relative tolerance',
            description='Floats are considered unequal if the relative '
                        'difference between them is larger than this value.',
            editor=synode.editors.decimal_spinbox_editor(
                step=1e-5, decimals=10))
        parameters.set_float(
            'abs_tol', value=1e-8, label='Absolute tolerance',
            description='Floats are considered unequal if the absolute '
                        'difference between them is larger than this value.',
            editor=synode.editors.decimal_spinbox_editor(
                step=1e-8, decimals=10))
        return parameters


class AssertEqualADAF400(migrations.Migration):
    nodeid = 'org.sysess.sympathy.data.adaf.assertequaladaf'
    from_version = migrations.updated_version
    to_version = '4.0.0'

    def forward_status(self):
        return migrations.Perfect

    def forward_parameters(self, old_parameters):
        old_parameters['rel_tol'].editor = (
            synode.editors.spinbox_editor(step=1e-8))
        old_parameters['abs_tol'].editor = (
            synode.editors.spinbox_editor(step=1e-8))
        return old_parameters
