# This file is part of Sympathy for Data.
# Copyright (c) 2016, Combine Control Systems AB
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
from packaging import version as pversion

import matplotlib
from matplotlib import markers as mpl_markers

from . import colors
from . import wizards
from .models import Backend


def _mpl_version():
    return pversion.parse(matplotlib.__version__)


def list_from_cycle(cycle):
    first = next(cycle)
    result = [first]
    for current in cycle:
        if current == first:
            break
        else:
            result.append(current)

    # Reset iterator state:
    for current in cycle:
        if current == result[-1]:
            break
    return result


def set_color_cycle(axes, color_cycle):
    from matplotlib import cycler
    axes.set(prop_cycle=cycler(color=color_cycle))


def color_cycle(axes=None):
    if axes is None:
        return ['#' + c for c in colors.COLOR_CYCLES['default']]

    return [prop['color']
            for prop in list_from_cycle(axes._get_lines.prop_cycler)]


def next_color(axes):
    return next(axes._get_lines.prop_cycler)['color']


MARKERS = mpl_markers.MarkerStyle.markers

HISTTYPES = ['bar', 'step']

GROUPTYPES = ['grouped', 'stacked']

VALIGNMENTS = ['over', 'top', 'center', 'bottom', 'under']

LEGEND_LOC = {
    'best': 0,  # (only implemented for axes legends)
    'upper left': 2,
    'upper right': 1,
    'lower left': 3,
    'lower right': 4,
    # 'right': 5,
    'center left': 6,
    'center right': 7,
    'upper center': 9,
    'lower center': 8,
    'center': 10
}

OUTSIDE_LEGEND_LOC = [
    'outside right',
    'outside left',
    'outside upper',
    'outside lower',
]

FONTSIZE = ['xx-small',
            'x-small',
            'small',
            'medium',
            'large',
            'x-large',
            'xx-large']


def lookup_marker(marker):
    for key, value in MARKERS.items():
        if marker == key:
            return marker
        elif marker == value:
            return key
    return None


matplotlib_backend = Backend(
    name='matplotlib',
    markers=list(MARKERS.values()),
    font_sizes=FONTSIZE,
    legend_locations=list(LEGEND_LOC.keys()) + OUTSIDE_LEGEND_LOC,
    wizards=list(wizards.wizard_classes.keys()),
)
