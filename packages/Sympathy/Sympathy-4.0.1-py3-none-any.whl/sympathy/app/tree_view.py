# This file is part of Sympathy for Data.
# Copyright (c) 2013 Combine Control Systems AB
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
import html
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

from sympathy.platform import widget_library as sywidgets
from sympathy.platform import item_models
from sympathy.utils import search


def font_color_highlighter(color='#990000', **kw):
    return 'color="{}"'.format(color)


def font_background_highlighter(color='#EECC22', **kw):
    return 'style="background-color: {}"'.format(color)


def font_weight_highlighter(**kw):
    return 'style="font-weight: bold"'


def style_font_weight_bold(text):
    return f'<font style="font-weight: bold">{text}</font>'


highlighters = {
    'color': font_color_highlighter,
    'background-color': font_background_highlighter,
    'font-weight': font_weight_highlighter
}


(IdentityRole,
 BoldRole,
 PositionRole,
 RawRole) = (QtCore.Qt.UserRole + i for i in range(4))


HighlightedText = QtGui.QPalette.HighlightedText


class LeafItem(item_models.TreeItem):
    """Interface that items of the TreeModel must fulfill."""

    def __init__(self, *args, **kwargs):
        self._name = ''
        self._highlighted_text = ''
        self._parent = None
        super().__init__(*args, **kwargs)

    def name(self):
        name = self._name
        return name[:1].upper() + name[1:]

    def data(self, role=QtCore.Qt.DisplayRole):
        res = None
        if role == RawRole:
            name = self.name()
            res = name[:1].upper() + name[1:]
        elif role == QtCore.Qt.DecorationRole:
            res = self.icon()
        elif role == QtCore.Qt.ToolTipRole:
            res = self.tool_tip()
        elif role == IdentityRole:
            res = self.identifier()
        elif role == QtCore.Qt.DisplayRole:
            res = self.highlighted()
        return res

    def set_data(self, value, role):
        res = False
        if role == QtCore.Qt.DisplayRole:
            self.set_highlighted_text(value)
            res = True
        return res

    def parent(self):
        return self._parent

    def is_leaf(self):
        return True

    def child_count(self):
        return 0

    def icon(self):
        return None

    def identifier(self):
        """
        Unique identifier, used for drag operations
        """
        return None

    def tool_tip(self):
        return ''

    def highlighted(self):
        """Highlighted text"""
        return self._highlighted_text

    def set_highlighted_text(self, text):
        """Set Highlighted text"""
        self._highlighted_text = text

    def node(self):
        """Not valid for parents"""
        return None

    def flags(self):
        return (QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsDragEnabled |
                QtCore.Qt.ItemIsSelectable)


class TreeItem(LeafItem):
    def __init__(self, *args, **kwargs):
        self._children = []
        super().__init__(*args, **kwargs)

    def is_leaf(self):
        return False

    def add_child(self, child):
        """Add a child"""
        self._children.append(child)

    def remove_child(self, child):
        self._children.remove(child)

    def insert_child(self, i, child):
        self._children.insert(i, child)

    def index(self, child):
        """Returns the index of child"""
        return self._children.index(child)

    def child(self, row):
        """Returns the child at row"""
        return self._children[row]

    def child_count(self):
        return len(self._children)

    def flags(self):
        return (QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsSelectable)


class TreeModel(item_models.TreeModel):
    """
    Responsible for building and updating the (viewed) tree.
    """

    def __init__(self, root_item, parent=None):
        self._old_root = None
        super().__init__(root_item, parent)
        self._build_model()

    def _build_model(self):
        raise NotImplementedError

    @QtCore.Slot()
    def update_model(self):
        self.beginResetModel()
        self._clear_items()
        self._build_model()
        self.endResetModel()

    def get_node(self, index):
        item = self._get_item(index)
        data = None
        if item is not None:
            data = item.node()
        return data

    # Override to avoid loop due to dataChanged in filterAcceptsRow. The method
    # of applying highlight should be changed to avoid this, dataChanged should
    # be emitted: https://doc.qt.io/qt-5/qabstractitemmodel.html#setData
    def setData(self, index, value, role):
        res = False
        if index.isValid():
            item = self._get_item(index)
            if item is not None:
                res = item.set_data(value, role)
        if res is None:
            res = super().setData(index, value, role)
        return res


class TreeView(sywidgets.HtmlTreeView):
    """
    Tree view. It is separated from the regular tree view in order to support
    selection_changed signalling.
    """

    selection_changed = QtCore.Signal(dict)
    switch_to_filter = QtCore.Signal()
    item_accepted = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._font = QtWidgets.QApplication.font()

        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setIndentation(15)
        self.setDropIndicatorShown(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self.setFont(self._font)
        self.doubleClicked.connect(self._accept_index)
        self.setStyleSheet(
            'QTreeView {'
            '  border-image: url(none.png);'
            '  selection-background-color: transparent; }')

    def selectionChanged(self, selected, deselected):
        if len(selected.indexes()) > 0:
            index = self.model().mapToSource(selected.indexes()[0])
            self.selection_changed.emit(
                self.model().sourceModel().get_node(index))
        super().selectionChanged(selected, deselected)

    def keyPressEvent(self, event):
        index = self.currentIndex()
        parent = index.parent()
        if (event.key() == QtCore.Qt.Key_Up and parent and
                parent.row() == 0 and index.row() == 0):
            self.switch_to_filter.emit()
        elif event.key() == QtCore.Qt.Key_Return:
            proxy_index = self.currentIndex()
            self._accept_index(proxy_index)
            event.accept()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self.setCurrentIndex(QtCore.QModelIndex())
        super().focusOutEvent(event)

    def _accept_index(self, index):
        index = self.model().mapToSource(index)
        item = self.model().sourceModel().get_node(index)
        self._accept_item(item)

    def _accept_item(self, item):
        self.item_accepted.emit(item)


class AdvancedFilter(QtWidgets.QWidget):
    switch_to_list = QtCore.Signal()
    filter_changed = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._init_gui()

    def _init_gui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(QtCore.QMargins())

        self._filter = FilterLineEdit(parent=self)
        layout.addWidget(self._filter)
        self._filter.switch_to_list.connect(self.switch_to_list)
        self._filter.textChanged[str].connect(self.filter_changed)
        self.setLayout(layout)

    def set_focus(self):
        # TODO: if enhanced mode is open, set focus to lowest LineEdit widget
        self._filter.setFocus()


class FilterLineEdit(sywidgets.ClearButtonLineEdit):
    switch_to_list = QtCore.Signal()

    def __init__(self, placeholder="Filter", clear_button=True, parent=None):
        super().__init__(placeholder, clear_button, parent)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down:
            self.switch_to_list.emit()
            # event.accept()
        else:
            super().keyPressEvent(event)


class FilterTreeView(QtWidgets.QWidget):
    """Combination widget - tree view and filter edit."""

    item_accepted = QtCore.Signal(object)

    def __init__(self, proxy_model, view, parent=None):
        super().__init__(parent)
        self._proxy_model = proxy_model
        self._model = None

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(QtCore.QMargins())
        self._layout.setSpacing(0)

        self._filter = AdvancedFilter(parent=self)
        self._layout.addWidget(self._filter)
        self._view = view
        self._view.setModel(self._proxy_model)
        self._layout.addWidget(self._view, stretch=10)

        self.update_filter('')

        self._filter.filter_changed[str].connect(
            self.update_filter)
        self._filter.switch_to_list.connect(self._handle_switch_to_list_view)
        self._view.switch_to_filter.connect(self._handle_switch_to_filter)
        self._view.item_accepted.connect(self.item_accepted)
        self.setLayout(self._layout)

    def set_model(self, model):
        # Store model as a private member to avoid shiboken
        # deallocation problem.
        self._model = model
        self._reset_model()
        self._setup_view()
        self._model.modelReset.connect(self._reset_model)

    def _setup_view(self):
        self._view.setIndentation(15)
        self._view.setItemsExpandable(True)

    def _default_expand(self):
        self._view.collapseAll()

    @QtCore.Slot()
    def update_model(self):
        self._model.update_model()

    @QtCore.Slot(tuple)
    def set_highlighter(self, highlighter_param):
        matcher_type, highlighter_type, highlighter_color = highlighter_param
        highlighter_func = highlighters.get(highlighter_type,
                                            font_color_highlighter)
        highlighter_attr = highlighter_func(color=highlighter_color)
        self._proxy_model.highlighter_attr = highlighter_attr
        self._proxy_model.matcher_type = matcher_type

    @QtCore.Slot()
    def _reset_model(self):
        """Reset (reload) model"""
        sort_role = self._proxy_model.sortRole()
        self._proxy_model.setSourceModel(self._model)
        self._proxy_model.setSortRole(sort_role)
        self.update_filter()

    @QtCore.Slot(str)
    def update_filter(self, new_filter=None):
        used_filter = self._proxy_model.update_filter(new_filter)
        self._handle_expanding(used_filter != '')

    def focus_filter(self):
        self._filter.set_focus()

    @QtCore.Slot()
    def clear_filter(self):
        self._filter.setText('')
        self.update_filter('')
        self._view.collapseAll()

    def _handle_expanding(self, state):
        if state:
            self._view.expandAll()
        else:
            self._default_expand()

    def _handle_switch_to_list_view(self):
        self._view.setFocus()
        try:
            proxy_index = self._proxy_model.index(0, 0)
            self._view.setCurrentIndex(proxy_index)
        except Exception:
            pass

    def _handle_switch_to_filter(self):
        self._filter.set_focus()
        self._view.setCurrentIndex(QtCore.QModelIndex())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            view = self._view
            proxy_index = view.currentIndex()
            index = self._proxy_model.mapToSource(proxy_index)
            item = self._proxy_model.sourceModel().get_node(index)
            self.item_accepted.emit(item)
            event.accept()
        super().keyPressEvent(event)


class TreeFilterProxyModelBase(QtCore.QSortFilterProxyModel):
    """
    Proxy model that supplies sorting and filtering for the tree model.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._filter = ''
        self._output_type = None
        self._cache = {}
        self._matcher_type = 'character'
        self._highlighter_attr = 'style="background-color: #EECC22"'
        self._filter_regex = None
        self._highlight_regex = []
        self.highlighted = set()

    @property
    def matcher_type(self):
        return self._matcher_type

    @matcher_type.setter
    def matcher_type(self, matcher_type):
        self._matcher_type = matcher_type
        self.update_filter(self._filter)

    @property
    def highlighter_attr(self):
        return self._highlighter_attr

    @highlighter_attr.setter
    def highlighter_attr(self, attr):
        self._highlighter_attr = attr
        self.update_filter(self._filter)

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(
            source_row, self.sourceModel().columnCount() - 1, source_parent)
        return self._show_row(index)

    def _show_row(self, index):
        ret_val = False
        source = self.sourceModel()
        number_of_rows = source.rowCount(index)

        def get_parents(parent):
            parent_names = []
            parents = []
            parent_name = source.data(parent, RawRole)

            while parent_name is not None:
                parent_names.append(parent_name)
                parents.append(parent)
                parent = source.parent(parent)
                parent_name = source.data(parent, RawRole)

            parent_names = [p for p in reversed(parent_names)]
            parents = list(reversed(parents))
            return (parent_names, parents)

        def get_parent_indices(parent_names):
            res = []
            pos = 0
            for parent_name in parent_names:
                next_pos = pos + len(parent_name)
                res.append((pos, next_pos))
                pos = next_pos
            return res

        def get_highlighted_parents(parent_struct, highlight_struct):
            res = {}
            highlight_struct_tmp = []
            for highlight, (start, end) in highlight_struct:
                highlight_struct_tmp.append(
                    (highlight, (start - seg_offsets[start],
                                 end - seg_offsets[end])))
            highlight_struct = highlight_struct_tmp
            highlight_iter = iter(highlight_struct)
            parent_iter = iter(parent_struct)

            pos = 0
            highlight, (hstart, hend) = next(highlight_iter, (None, (-1, -1)))
            (parent, parent_name), (pstart, pend) = next(
                parent_iter, ((None, None), (None, None)))
            while highlight is not None and parent is not None:
                next_pos = min(pend, hend)
                res.setdefault(parent, []).append(
                    (highlight, parent_name[pos - pstart:next_pos - pstart]))

                if next_pos >= hend:
                    highlight, (hstart, hend) = next(
                        highlight_iter, (None, (-1, -1)))

                if next_pos >= pend:
                    (parent, parent_name), (pstart, pend) = next(
                        parent_iter, ((None, None), (None, None)))

                pos = next_pos
            return res

        def set_highlight(full_name, parents, parent_names):
            parent_indices = get_parent_indices(parent_names)
            parent_struct = list(zip(zip(parents, parent_names),
                                     parent_indices))

            if self._matcher_type == 'word':
                highlight_struct = self.highlight_word(full_name)
            elif self._matcher_type == 'character':
                highlight_struct = self.highlight_character(full_name)
            else:
                assert False, 'Unknown highlight'

            highlighted_parents = get_highlighted_parents(
                parent_struct, highlight_struct)

            for (parent, _), (_, _) in parent_struct:
                segs = []
                for highlight, chars in highlighted_parents.get(parent, []):
                    chars = html.escape(chars)
                    if highlight:
                        chars = f'<font {self.highlighter_attr}>{chars}</font>'
                    segs.append(chars)

                parent_name = ''.join(segs)

                if source.data(parent, BoldRole):
                    parent_name = style_font_weight_bold(parent_name)

                source.setData(
                    parent, parent_name, QtCore.Qt.DisplayRole)

        if number_of_rows > 0:
            for i in range(number_of_rows):
                child_index = source.index(i, 0, index)
                if not child_index.isValid():
                    break
                else:
                    ret_val = self._show_row(child_index)
                if ret_val:
                    break
        else:
            parent = source.index(index.row(), 0, index.parent())
            item = source._get_item(parent)

            if not item or not self._show_item(item):
                return False

            parent_names, parents = get_parents(parent)

            full_name = ' '.join(parent_names)
            # Generate offsets to be able to transform between positions
            # from new name (with spaces included) used in the regex and
            # the old names used to apply highlight, etc.
            seg_offsets = []
            for i, parent_name in enumerate(parent_names):
                seg_offsets.extend([i] * (len(parent_name) + 1))

            ret_val = search.matches(self._filter_regex, full_name)

            if ret_val:
                set_highlight(full_name, parents, parent_names)

        return ret_val

    def _show_item(self, item):
        return True

    def _highlight_match(self, line, match):
        """
        Highlight struct for line.
        """
        if match:
            end = 0
            parts = []
            for i in range(1, len(match.groups()) + 1):
                old_end = end
                start, end = match.span(i)
                if old_end < start:
                    parts.append((False, (old_end, start)))

                parts.append((True, (start, end)))

            old_end = end
            end = len(line)
            if old_end < end:
                parts.append((False, (old_end, end)))
            return parts
        else:
            return [(False, (0, len(line)))]

    def highlight_character(self, line):
        return self._highlight_match(
            line, self._highlight_regex.match(line))

    def highlight_word(self, line):
        return self._highlight_match(
            line, self._highlight_word_regex.match(line))

    def update_filter(self, new_filter):
        if new_filter is not None:
            self._highlight_regex = search.highlight_patterns(new_filter)
            self._highlight_word_regex = search.highlight_word_patterns(
                new_filter)
            self._filter = new_filter
            self._filter_regex = search.fuzzy_pattern(new_filter)

        sort_role = self.sortRole()
        self.invalidateFilter()
        self.setSortRole(sort_role)
        self.sort(0, QtCore.Qt.AscendingOrder)
        return self._filter
