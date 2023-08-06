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


SIGNALS = ['sinus', 'cosines', 'tangent']


def table_signal_base_parameters():
    parameters = synode.parameters()
    table_parameters = parameters.create_page('table_params', 'Table')
    table_parameters.set_integer(
        'column_entries', value=100, label='Column entries',
        description='The number of column entries to be generated.',
        editor=synode.editors.bounded_spinbox_editor(0, 1000000, 1))
    table_parameters.set_integer(
        'column_length', value=1000, label='Column length',
        description='The length of columns to be generated.',
        editor=synode.editors.bounded_spinbox_editor(0, 100000000, 1))

    signal_parameters = parameters.create_page('signal_params', 'Signal')
    signal_parameters.set_list(
        'signal_type', value=[0], label='Signal type',
        plist=SIGNALS,
        description='The signal to be generated.',
        editor=synode.editors.combo_editor())
    signal_parameters.set_float(
        'amplitude', value=1., label='Amplitude',
        description='The amplitude of the signal to be generated.')
    signal_parameters.set_float(
        'frequency', value=0.01, label='Frequency',
        description='The frequency in inverse samples of the signal '
                    'to be generated.')
    signal_parameters.set_float(
        'period', value=100., label='Period',
        description='The period in samples of the signal to be generated.')
    signal_parameters.set_boolean(
        'use_period', value=True, label='Period or Frequency',
        description=('Use Period [Checked] or Frequency [Unchecked] to ' +
                     'generate the signal.'))
    signal_parameters.set_float(
        'phase_offset', value=0., label='Phase offset',
        description='Phase offset in radians of the signal to be generated.')
    signal_parameters.set_boolean(
        'add_noise', value=False, label='Add random noise',
        description='If random noise should be added to the signals.')
    signal_parameters.set_float(
        'noise_amplitude', value=0.01, label='Amplitude of noise',
        description='The amplitude of the noise.',
        editor=synode.editors.spinbox_editor(0.05))
    signal_parameters.set_boolean(
        'index_column', value=True, label='First column as index',
        description='Add an index column to the beginning of the table.')
    return parameters


class GenerateSignalTable300(migrations.UpdateParametersMigration):
    nodeid = 'org.sysess.sympathy.generate.signaltable'

    def updated_definition(self):
        parameters = table_signal_base_parameters()
        return parameters


class GenerateSignalTables300(migrations.UpdateParametersMigration):
    nodeid = 'org.sysess.sympathy.generate.signaltables'

    def updated_definition(self):
        parameters = table_signal_base_parameters()
        parameters['table_params'].set_integer(
            'length', value=5, label='Table list length',
            description='The length of table list to be generated.',
            editor=synode.editors.bounded_spinbox_editor(0, 10000, 1))
        return parameters


class GenerateSignalTable400(migrations.Migration):
    nodeid = 'org.sysess.sympathy.generate.signaltable'
    from_version = migrations.updated_version
    to_version = '4.0.0'

    def forward_status(self):
        return migrations.Perfect

    def forward_parameters(self, old_parameters):
        old_parameters['signal_params']['noise_amplitude'].editor = (
            synode.editors.spinbox_editor(0.05))
        return old_parameters


class GenerateSignalTables400(GenerateSignalTable400):
    nodeid = 'org.sysess.sympathy.generate.signaltables'
