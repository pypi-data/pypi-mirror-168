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
import os
import tempfile

from PySide6 import QtCore, QtWidgets, QtWebEngineWidgets

from sympathy.platform import settings
from sympathy.api.typeutil import ViewerBase


class BokehViewer(ViewerBase):
    def __init__(self, plot_data=None, console=None, parent=None):
        super().__init__(parent)
        self._figure = plot_data
        self._web_enigine_view = QtWebEngineWidgets.QWebEngineView()

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._web_enigine_view)
        self.setLayout(self._layout)
        self.setMinimumWidth(300)

    def figure(self):
        return self._figure

    def data(self):
        return self.figure()

    def update_data(self, data):
        if data is not None:
            fileno, tmp_file = tempfile.mkstemp(
                prefix='bokeh_viewer_',
                suffix='.html',
                dir=settings.settings()['session_folder'])
            os.close(fileno)
            data.save_figure(tmp_file, use_cdn=False, stretch=True)
            self._web_enigine_view.load(QtCore.QUrl.fromLocalFile(tmp_file))
