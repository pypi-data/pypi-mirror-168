# This file is part of Sympathy for Data.
# Copyright (c) 2013, 2018 Combine Control Systems AB
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
import importlib
import os

from PySide6 import QtCore

from sympathy.platform import qt_gui_compat as QtGui
from sympathy.utils.context import deprecated_warn


deprecated_warn('sympathy.api.qt', '5.0.0', 'sympathy.api.qt2')


class PySideBackend:
    def use_matplotlib_qt(self):
        import matplotlib
        matplotlib.use('Qt5Agg')
        matplotlib.rcParams['backend'] = 'Qt5Agg'
        os.environ['QT_API'] = 'pyside6'

    def use_ipython_qt(self):
        os.environ['QT_API'] = 'pyside6'


backend = PySideBackend()


def import_module(module_name):
    if module_name == 'QtGui':
        return QtGui
    elif module_name == 'QtWidgets':
        from PySide6 import QtWidgets
        # These classes were moved in Qt6. Add references to them in their old
        # places for increased compatibility.
        QtWidgets.QAction = QtGui.QAction
        QtWidgets.QActionGroup = QtGui.QActionGroup
        QtWidgets.QUndoCommand = QtGui.QUndoCommand
        QtWidgets.QUndoStack = QtGui.QUndoStack
        QtWidgets.QUndoGroup = QtGui.QUndoGroup
        return QtWidgets

    return importlib.import_module(f'PySide6.{module_name}')


Signal = QtCore.Signal
Slot = QtCore.Slot
Property = QtCore.Property
