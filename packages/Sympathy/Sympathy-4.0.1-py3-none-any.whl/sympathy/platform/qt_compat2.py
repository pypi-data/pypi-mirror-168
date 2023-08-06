# This file is part of Sympathy for Data.
# Copyright (c) 2013, 2018, Combine Control Systems AB
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

import PySide6
from PySide6 import QtCore
from PySide6 import QtGui  # noqa: F401
from PySide6 import QtWidgets  # noqa: F401
import PySide6.QtCore  # noqa: F401


class PySideBackend:
    def use_matplotlib_qt(self):
        import matplotlib
        matplotlib.use('Qt5Agg')
        matplotlib.rcParams['backend'] = 'Qt5Agg'
        os.environ['QT_API'] = 'pyside6'

    def use_ipython_qt(self):
        os.environ['QT_API'] = 'pyside6'


backend = PySideBackend()


# These classes were moved in Qt6. Add references to them in their old
# places for increased compatibility.
QtWidgets.QAction = QtGui.QAction
QtWidgets.QActionGroup = QtGui.QActionGroup
QtWidgets.QUndoCommand = QtGui.QUndoCommand
QtWidgets.QUndoStack = QtGui.QUndoStack
QtWidgets.QUndoGroup = QtGui.QUndoGroup


def import_module(module_name):
    return importlib.import_module(f'PySide6.{module_name}')


Signal = QtCore.Signal
Slot = QtCore.Slot
Property = QtCore.Property
