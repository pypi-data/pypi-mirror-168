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
import sklearn
import sklearn.cluster

from sylib.machinelearning.descriptors import Descriptor
from packaging import version as pversion
from sympathy.api.exceptions import sywarn

sklearn_version = pversion.parse(sklearn.__version__)


class KMeansDescriptor(Descriptor):

    def get_parameters(self, parameters):
        """Converts parameters from Sympathy's format into a keyword dictionary
        suitable for sklearn"""
        kwargs = {}
        for name, info in self._parameters.items():
            type_ = info['type']
            skl_name = info['skl_name']

            if 'no-kw' in info and info['no-kw']:
                continue
            if 'deprecated' in info and info['deprecated']:
                if (name in parameters
                    and (type_.from_string(parameters[name].value) !=
                         type_.default)):

                    sywarn("Parameter {} is deprecated and will be ignored"
                           .format(name))
                continue

            # Ensure that old saved parameters do not lead
            # to errors in later versions
            params_11 = sklearn_version >= pversion.Version('1.1.0')
            if (params_11 and parameters[name].value in ["auto", "full"]
                    and name == "algorithm"):
                compat_dict = {"auto": "lloyd", "full": "lloyd"}
                kwargs[skl_name] = compat_dict[parameters[name].value]
            else:
                kwargs[skl_name] = type_.from_string(parameters[name].value)

        return kwargs
