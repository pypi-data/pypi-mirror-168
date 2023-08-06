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
from sylib.figure.models import Backend


MARKERS = [
    'circle',
    'diamond',
    'hex',
    'inverted_triangle',
    'plus',
    'square',
    'star',
    'triangle',
]


FONTSIZE = [
    '8px',
    '9px',
    '10px',
    '12px',
    '16px',
    '24px',
    '36px',
    '48px',
    '68px',
    '80px',
    '94px',
]


LEGEND_LOC = [
    'upper left',
    'upper right',
    'lower left',
    'lower right',
    'center left',
    'center right',
    'upper center',
    'lower center',
    'center',
    'outside right',
    'outside left',
    'outside upper',
    'outside lower',
]


bokeh_backend = Backend(
    name='bokeh',
    markers=MARKERS,
    font_sizes=FONTSIZE,
    legend_locations=LEGEND_LOC,
    wizards=[],
)
