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

from sylib.bokeh import exporter


class DataExportVectorized(exporter.BokehFigureDataExporterBase):
    """Exporter for Figure producing vectorized images."""
    EXPORTER_NAME = "Html"
    FILENAME_EXTENSION = None

    def create_filenames(self, input_list, filename, *args):
        return super().create_filenames(
            input_list, filename, *args, ext="html")

    def export_data(self, data, fq_outfilename, progress=None):
        """Export Figure to Image."""
        if not os.path.exists(os.path.dirname(fq_outfilename)):
            os.makedirs(os.path.dirname(fq_outfilename))

        data.save_figure(fq_outfilename)
