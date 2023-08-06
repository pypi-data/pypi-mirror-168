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
import sys
from PySide6 import QtWidgets
from sympathy.api import node
from sympathy.platform.settings import settings as create_settings


def main():
    # Use of settings fail when code editor parameter is used from python.
    settings = create_settings()
    settings._attributes['Gui/code_editor_theme'] = 'colorful'

    parameters = node.parameters()
    parameters.set_string(
        'code',
        label='Python code',
        value='',
        editor=node.editors.code_editor(language='python'))

    app = QtWidgets.QApplication(sys.argv)
    w = parameters['code'].gui()
    w.show()
    app.exec_()


if __name__ == '__main__':
    main()
