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
from sylib.table_importer_gui import (PreviewGroupBoxWidget, TableImportWidget,
                                      TableImportController)
from sylib.table_sources import TableSourceModel, PreviewWorker
import sylib.table_sources as table_sources

from sylib.parquet import parquet
from sympathy.api import node as synode
from sympathy.api import importers
from sympathy.api import table
from sympathy.api import qt2 as qt_compat

QtGui = qt_compat.import_module('QtGui')
QtCore = qt_compat.QtCore
QtWidgets = qt_compat.import_module('QtWidgets')


class ImporterParquet:
    """Importer class for data in parquet format."""

    def __init__(self, pq_source):
        self._source = pq_source
        self._partial_read = False

    def set_partial_read(self, value):
        self._partial_read = value

    def import_parquet(self, out_table, nr_data_rows):
        self._discard = False
        data_table = self._data_as_table(nr_data_rows)
        out_table.update(data_table)

    def _data_as_table(self, no_rows):
        """
        Merges the imported data, stored in one or many Tables, into a single
        Table.
        """
        out_table = self._data_as_table_full_rows(no_rows)
        return out_table

    def _data_as_table_full_rows(self, no_rows):
        """Import data from mat-file as whole rows."""
        if no_rows == -1:
            return self._source.read(-1, True)
        elif no_rows > 0:
            return self._source.read(no_rows, True)
        else:
            raise Exception('Not valid number of rows to read.')


class TableSourceParquet:
    """
    This class is the layer between the physical parquet-file and the import
    routines.
    """

    def __init__(self, fq_infilename):
        self._fq_infilename = fq_infilename

    def read(self, no_rows, part):
        out_table = table.File()
        pq_table = parquet.read_pqfile_to_table(self._fq_infilename)
        names = pq_table.column_names()
        rows = pq_table.number_of_rows()

        end_row = table_sources.compute_end_row(0, no_rows, rows, part)

        for column in names:
            data = pq_table.get_column_to_array(column)
            if end_row == -1:
                data = data[:]
            else:
                data = data[:end_row]
            out_table.set_column_from_array(column, data)

        out_table.set_attributes(pq_table.get_attributes())
        out_table.set_name(pq_table.get_name())
        return out_table


class TableSourceModelParquet(TableSourceModel):
    """Model layer between GUI and parquet importer."""

    get_preview = qt_compat.Signal(int)

    def __init__(self, parameters, fq_infilename, mode, valid):
        super().__init__(
            parameters, fq_infilename, mode)
        self.data_table = None
        self._valid = valid
        self._pq_source = TableSourceParquet(fq_infilename)
        self._importer = ImporterParquet(self._pq_source)
        self._importer.set_partial_read(True)

        self._init_model_specific_parameters()
        self._init_preview_worker()

    def _init_model_common_parameters(self):
        """Init common parameters xlsx, csv, mat and parquet importers."""
        self.preview_start_row = self._parameters['preview_start_row']
        self.no_preview_rows = self._parameters['no_preview_rows']

    def _init_model_specific_parameters(self):
        """Init special parameters for parquet importer."""
        self.preview_start_row = self._parameters['preview_start_row']
        self.no_preview_rows = self._parameters['no_preview_rows']
        self.data_offset = lambda: None
        self.data_offset.value = 1

    def _init_preview_worker(self):
        """Collect preview data from parquet file."""
        def import_function(*args):
            self._importer.import_parquet(*args)

        self._preview_thread = QtCore.QThread()
        self._preview_worker = PreviewWorker(self._importer.import_parquet)
        self._preview_worker.moveToThread(self._preview_thread)
        self._preview_thread.finished.connect(self._preview_worker.deleteLater)
        self.get_preview.connect(self._preview_worker.create_preview_table)
        self._preview_worker.preview_ready.connect(self.set_preview_table)
        self._preview_worker.preview_failed.connect(self.set_preview_failed)
        self._preview_thread.start()
        self.collect_preview_values()

    @qt_compat.Slot()
    def collect_preview_values(self):
        """Collect preview data from parquet file."""
        no_rows = self.no_preview_rows.value
        if self._valid:
            self.get_preview.emit(no_rows)
        else:
            self.data_table = table.File()
        self.update_table.emit()

    @qt_compat.Slot(table.File)
    def set_preview_table(self, data_table):
        self.data_table = data_table
        self.update_table.emit()

    def cleanup(self):
        self._preview_thread.quit()
        self._preview_thread.wait()


class ImportParametersWidgetParquet(QtWidgets.QWidget):
    """
    The control group box includes the widgets for determination of
    data start and end row/column and transpose condition.
    """

    get_preview = QtCore.Signal()

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self._model = model
        self._init_gui(model)
        self._init_preview_signals()

    def _init_gui(self, model):
        pass

    def _init_preview_signals(self):
        pass


class TableImportWidgetParquet(TableImportWidget):
    MODE = 'Parquet'

    def __init__(self, parameters, fq_infilename, valid=True):
        self.model = TableSourceModelParquet(
            parameters, fq_infilename, self.MODE, valid)
        super().__init__(
            parameters, fq_infilename, self.MODE, valid)

    def _init_gui(self, model, mode, valid):
        """Initialize GUI structure."""
        layout = QtWidgets.QVBoxLayout()

        import_parameters = self._collect_import_parameters_widget(
            model)

        table_source = self._collect_table_source_widget(model)

        preview_table = PreviewGroupBoxWidget(model)

        layout.addWidget(preview_table)

        self.controller = self._collect_controller(
            model=model,
            table_source=table_source,
            import_param=import_parameters,
            preview_table=preview_table, valid=valid)

        self.setLayout(layout)
        self.adjustSize()

    def _collect_import_parameters_widget(self, model):
        return ImportParametersWidgetParquet(model)

    def _collect_table_source_widget(self, model):
        pass

    def _collect_controller(self, **kwargs):
        return TableImportController(**kwargs)


class DataImportParquet(importers.TableDataImporterBase):
    """Importer for Parquet files."""

    IMPORTER_NAME = "Parquet"

    def __init__(self, fq_infilename, parameters):

        super().__init__(fq_infilename, parameters)

        if parameters is not None:

            if 'preview_start_row' not in parameters:
                parameters.set_integer(
                    'preview_start_row', value=1, label='Preview start row',
                    description='The first row where data will review from.',
                    editor=synode.Util.bounded_spinbox_editor(
                        1, 500, 1))

            if 'no_preview_rows' not in parameters:
                parameters.set_integer(
                    'no_preview_rows', value=20,
                    label='Number of preview rows',
                    description='The number of preview rows to show.',
                    editor=synode.editors.bounded_spinbox_editor(1, 200, 1))

    def name(self):
        return self.IMPORTER_NAME

    def valid_for_file(self):
        """Return True if input file is a valid Parquet file."""
        if (self._fq_infilename is None or
                not self._fq_infilename.endswith(".parquet")):
            return False
        try:
            parquet.read_pqfile_to_table(self._fq_infilename)
        except Exception:
            return False

        allowed_extensions = ['parquet', 'PARQUET']
        extension = os.path.splitext(self._fq_infilename)[1][1:]

        return extension in allowed_extensions

    def parameter_view(self, parameters):
        valid_for_file = self.valid_for_file()
        return TableImportWidgetParquet(parameters, self._fq_infilename,
                                        valid_for_file)

    def import_data(self, out_datafile, parameters=None, progress=None):
        """Import Parquet data from a file"""

        parameters = parameters

        # Establish connection to Parquet datasource
        table_source = TableSourceParquet(self._fq_infilename)

        importer = ImporterParquet(table_source)

        try:
            importer.import_parquet(out_datafile, -1)
        except Exception as e:
            raise self.import_failed(e)
