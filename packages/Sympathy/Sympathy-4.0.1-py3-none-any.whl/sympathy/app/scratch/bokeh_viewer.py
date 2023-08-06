# This file is part of Sympathy for Data.
# Copyright (c) 2022 Combine Control Systems AB
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
import os.path
import sys

from bokeh.plotting import figure, Document
from bokeh.embed import file_html
from bokeh.resources import CDN
import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets
import PySide6.QtWebEngineWidgets as QtWebEngineWidgets

if __name__ == '__main__':
    filename = "test.html"
    fig = figure()
    fig.line([0, 1, 2, 3, 4], [2, 1, 3, 5, 4])
    doc = Document()
    doc.add_root(fig)
    data = doc.to_json_string()

    html = file_html(Document.from_json_string(data), CDN)
    with open(filename, 'w') as f:
        f.write(html)

    app = QtWidgets.QApplication(sys.argv)
    w = QtWebEngineWidgets.QWebEngineView()
    w.load(QtCore.QUrl.fromLocalFile(os.path.abspath(filename)))
    w.show()
    app.exec_()
