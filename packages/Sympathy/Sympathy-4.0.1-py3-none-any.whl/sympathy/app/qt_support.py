# This file is part of Sympathy for Data.
# Copyright (c) 2018 Combine Control Systems AB
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

import PySide6  # noqa: F401


def _qt_mod(subpath):
    assert subpath
    res = __import__('{}.{}'.format('PySide6', subpath))
    for seg in subpath.split('.'):
        assert subpath
        res = getattr(res, seg)
    return res


def data_location():
    QtCore = _qt_mod('QtCore')
    sp = QtCore.QStandardPaths
    return sp.writableLocation(sp.AppDataLocation)


def cache_location():
    QtCore = _qt_mod('QtCore')
    sp = QtCore.QStandardPaths
    return sp.writableLocation(sp.CacheLocation)


def documents_location():
    QtCore = _qt_mod('QtCore')
    sp = QtCore.QStandardPaths
    return sp.writableLocation(sp.DocumentsLocation)
