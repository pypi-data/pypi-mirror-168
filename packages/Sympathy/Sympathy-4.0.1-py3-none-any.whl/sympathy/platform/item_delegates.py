# This file is part of Sympathy for Data.
# Copyright (c) 2021 Combine Control Systems AB
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
"""
Gather various item delegates to encourage sharing.
"""
from . import widget_library as sywidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

EditRole = QtCore.Qt.EditRole
DisplayRole = QtCore.Qt.DisplayRole


class UniqueItemDelegate(QtWidgets.QItemDelegate):
    """
    Ensure values in column are not duplicated.
    """
    def createEditor(self, parent, option, index):
        model = index.model()
        values = [model.data(model.index(row, index.column()),
                             EditRole)
                  for row in range(model.rowCount())]
        del values[index.row()]
        values = set(values)

        def unique_validator(value):
            try:
                valid = value not in values
                if not valid:
                    raise sywidgets.ValidationError(
                        f'"{value}" is not a unique value')
            except Exception as e:
                raise sywidgets.ValidationError(str(e))
            return value

        editor = sywidgets.ValidatedTextLineEdit(parent=parent)
        editor.setBuilder(unique_validator)
        return editor

    def setEditorData(self, editor, index):
        data = index.model().data(index, EditRole)
        editor.setText(str(data or ''))
        editor.selectAll()

    def setModelData(self, editor, model, index):
        value = editor.value()
        index.model().setData(index, value, EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class HtmlItemDelegate(QtWidgets.QStyledItemDelegate):
    """
    ItemDelegate capable of displaying HTML text.

    Designed for TreeView items.
    """
    _highlight_role = QtGui.QPalette.HighlightedText

    def __init__(self, *args, highlight_role=None, **kwargs):
        if highlight_role is not None:
            self._highlight_role = highlight_role
        super().__init__(*args, **kwargs)

    def paint(self, painter, option, index):
        style_option = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(style_option, index)

        if style_option.widget is None:
            style = QtWidgets.QApplication.style()
        else:
            style = style_option.widget.style()

        doc = QtGui.QTextDocument()
        doc.setHtml(style_option.text)

        style_option.text = ""
        style.drawControl(
            QtWidgets.QStyle.CE_ItemViewItem, style_option, painter)

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()

        # Highlighting text if item is selected.
        if (style_option.state & QtWidgets.QStyle.State_Selected):
            ctx.palette.setColor(
                QtGui.QPalette.Text,
                style_option.palette.color(
                    QtGui.QPalette.Active, self._highlight_role))

        text_rect = style.subElementRect(
            QtWidgets.QStyle.SE_ItemViewItemText, style_option, None)
        painter.save()
        painter.setClipRect(text_rect)
        painter.translate(text_rect.topLeft())
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        size_hint = super().sizeHint(option, index)
        style_option = QtWidgets.QStyleOptionViewItem(option)
        doc = QtGui.QTextDocument()
        self.initStyleOption(style_option, index)
        doc.setHtml(style_option.text)
        doc.setTextWidth(style_option.rect.width())
        return QtCore.QSize(
            doc.idealWidth(), max(doc.size().height(), size_hint.height()))
