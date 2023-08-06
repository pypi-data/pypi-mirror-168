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


_METHODS = ['zero', 'nearest', 'linear', 'quadratic', 'cubic']


class InterpolateADAF300(migrations.UpdateParametersMigration):
    nodeid = 'org.sysess.sympathy.data.adaf.assertequaladaf'

    def updated_definition(self):
        parameters = synode.parameters()
        parameters.set_boolean(
            'resample_all_rasters', value=True, label="Resample all signals",
            description='Apply resampling to all signals')
        ts_editor = synode.editors.multilist_editor(edit=True)
        ts_editor.set_attribute('filter', True)
        parameters.set_list(
            'ts', label="Choose signals",
            description='Choose signals to interpolate', editor=ts_editor)
        parameters.set_float(
            'dt', label='Time step',
            description=('Time step in new timebasis. If old timebasis is of '
                         'type datetime this is considered to be in seconds.'),
            editor=synode.editors.decimal_spinbox_editor(
                step=1e-3, decimals=6))
        parameters.set_list(
            'new_tb', label='Timebasis to use for interpolation',
            description=('Timebasis to use as new timebasis '
                         'for selected timeseries'),
            editor=synode.editors.combo_editor(filter=True))
        parameters.set_boolean(
            'use_dt', label='Time step approach', value=True,
            description='Choose between a custom time step and using an '
                        'existing.')
        parameters.set_boolean(
            'only_timebasis', label='Export time basis only', value=False,
            description='Choose to only export the time basis')
        parameters.set_list(
            'bool_interp_method', plist=['zero', 'nearest'], value=[1],
            description=('Method used to interpolate boolean, text, and '
                         'byte string data'),
            editor=synode.editors.combo_editor())
        parameters.set_list(
            'int_interp_method', plist=_METHODS,
            value=[_METHODS.index('nearest')],
            description='Method used to interpolate integer data',
            editor=synode.editors.combo_editor())
        parameters.set_list(
            'interpolation_method', plist=_METHODS,
            value=[_METHODS.index('linear')],
            description='Method used to interpolate other data types',
            editor=synode.editors.combo_editor())
        return parameters


class InterpolateADAFs300(InterpolateADAF300):
    nodeid = 'org.sysess.sympathy.data.adaf.interpolateadafs'


class InterpolateADAF400(migrations.Migration):
    nodeid = 'org.sysess.sympathy.data.adaf.assertequaladaf'
    from_version = migrations.updated_version
    to_version = '4.0.0'

    def forward_status(self):
        return migrations.Perfect

    def forward_parameters(self, old_parameters):
        old_parameters['dt'].editor = (
            synode.editors.spinbox_editor(step=1e-3))
        return old_parameters


class InterpolateADAFs400(InterpolateADAF400):
    nodeid = 'org.sysess.sympathy.data.adaf.interpolateadafs'
