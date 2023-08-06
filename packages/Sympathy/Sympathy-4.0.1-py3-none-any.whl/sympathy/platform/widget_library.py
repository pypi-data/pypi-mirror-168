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
import os.path
import sys
import datetime
import functools
import contextlib
import re
import html
from typing import Tuple, Optional

from sympathy.platform import qt_compat2
from sympathy.utils import prim
from sympathy.utils import search
from sympathy.utils import code_edit
from sympathy.platform import settings
from sympathy.platform import colors
from sympathy.platform import item_delegates

import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets
import PySide6.QtGui as QtGui

QTextCursor = QtGui.QTextCursor
MoveOperation = QTextCursor.MoveOperation
MoveMode = QTextCursor.MoveMode
QEvent = QtCore.QEvent


def _pygments():
    # Importing pygments can in rare cases with unicode paths
    # result in UnicodeEncodeErrors.
    import pygments.lexers
    import pygments.lexers.special
    import pygments.styles
    import pygments.token
    return pygments


def monospace_font():
    # This should select the systems default monospace font
    f = QtGui.QFont('Monospace')
    f.setStyleHint(QtGui.QFont.TypeWriter)
    f.setFixedPitch(True)
    return f


toolbar_stylesheet = """
QToolBar {
    background: %s;
    border: 1px solid %s;
    spacing: 3px;
}

QLineEdit {
    padding: 0px;
    border-radius: 1px;
}

QToolButton:checked {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 rgba(0,0,0,60),
                                      stop: 1 rgba(0,0,0,30));
}

QToolButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 rgba(140,190,255,100),
                                      stop: 1 rgba(140,190,255,50));
}
"""


_NavigationToolbar = None


def mpl_toolbar_factory(canvas, parent, coordinates=True):
    def construct_style_sheet(toolbar):
        return toolbar_stylesheet % (get_parent_color(toolbar),
                                     get_border_color(toolbar))

    def get_parent_color(toolbar):
        color = toolbar.palette().color(toolbar.backgroundRole())
        return color.name()

    def get_border_color(toolbar):
        color = toolbar.palette().color(QtGui.QPalette.Mid)
        return color.name()

    global _NavigationToolbar
    if _NavigationToolbar is None:
        qt_compat2.backend.use_matplotlib_qt()
        from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

        class _ConnectNavigationToolbar(NavigationToolbar2QT):
            def connect_canvas(self):
                """
                Workaround to restore lost canvas interactivity.
                """
                self._id_press = self.canvas.mpl_connect(
                    'button_press_event', self._zoom_pan_handler)
                self._id_release = self.canvas.mpl_connect(
                    'button_release_event', self._zoom_pan_handler)
                self._id_drag = self.canvas.mpl_connect(
                    'motion_notify_event', self.mouse_move)
        _NavigationToolbar = _ConnectNavigationToolbar

    toolbar = _NavigationToolbar(canvas, parent, coordinates)
    toolbar.setStyleSheet(construct_style_sheet(toolbar))
    return toolbar


def plain_text_to_rich(text):
    """
    Format plain text so that it will be recognized as rich text, but with
    all special content escaped.

    Using rich text helps to get line wrapping in tooltips.
    """
    return f'<div>{html.escape(text)}</div>'


def set_plain_text_to_rich_tooltip(widget, text):
    widget.setToolTip(plain_text_to_rich(text))


class ModeComboBox(QtWidgets.QComboBox):
    itemChanged = qt_compat2.Signal(str)

    def __init__(self, items, parent=None):
        super().__init__(parent)
        self._lookup = dict(items)
        self._rlookup = dict(zip(self._lookup.values(), self._lookup.keys()))
        self.addItems([item[1] for item in items])
        self.currentIndexChanged[int].connect(self._index_changed)

    def set_selected(self, key):
        text = self._lookup[key]
        index = self.findText(text)
        if index >= 0:
            self.setCurrentIndex(index)

    def _index_changed(self, index):
        if index >= 0:
            text = self.currentText()
            self.itemChanged.emit(self._rlookup[text])


class SpaceHandlingListWidget(QtWidgets.QListView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = QtGui.QStandardItemModel()
        self.setModel(self._model)

    def setModel(self, model):
        self._model = model
        return super().setModel(model)

    def clear(self):
        self._model.clear()

    def count(self):
        return self._model.rowCount()

    def addItem(self, item):
        row = self._model.rowCount()
        self._model.insertRow(row, item)

    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def item(self, row):
        return self._model.item(row, 0)

    def items(self):
        return [self.item(row) for row in range(self.count())]

    def row(self, item):
        return self._model.indexFromItem(item).row()

    def removeItem(self, item):
        return self._model.removeRow(item.row())

    def selectedItems(self):
        return [self._model.itemFromIndex(i) for i in self.selectedIndexes()]

    def findItems(self, text, flags=QtCore.Qt.MatchExactly):
        return self._model.findItems(text, flags=flags)


class SpaceHandlingContextMenuListWidget(SpaceHandlingListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._menu = QtWidgets.QMenu(self)
        self._actions = []
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(
            self._custom_context_menu)

    def add_menu_action(self, action):
        self._actions.append(action)
        self._menu.addAction(action)
        self.addAction(action)

    def add_menu_separator(self):
        self._menu.addSeparator()

    def _custom_context_menu(self, pos):
        if self._actions:
            pos = self.mapToGlobal(pos)
            self._menu.exec_(pos)


class CheckableComboBox(QtWidgets.QComboBox):
    selectedItemsChanged = QtCore.Signal(bool)
    checked_items_changed = QtCore.Signal(list)

    def __init__(self):
        super().__init__()
        self.setItemDelegate(QtWidgets.QStyledItemDelegate(self))

        self._listview = self.view()

        self._listview.pressed.connect(self.handleItemPressed)
        self._listview.clicked.connect(self.handleItemClicked)

    def handleItemClicked(self, index):
        self.handleItemPressed(index, alter_state=False)

    def handleItemPressed(self, index, alter_state=True):
        item = self.model().itemFromIndex(index)
        self.blockSignals(True)
        if alter_state:
            if item.checkState() == QtCore.Qt.Checked:
                item.setCheckState(QtCore.Qt.Unchecked)
                idx = self.select_current_index()
            else:
                item.setCheckState(QtCore.Qt.Checked)
                idx = index.row()
        else:
            if item.checkState():
                idx = index.row()
            else:
                idx = self.select_current_index()
        self.setCurrentIndex(idx)
        self.blockSignals(False)
        self.selectedItemsChanged.emit(True)
        self.currentIndexChanged.emit(idx)
        self.checked_items_changed.emit(self.checkedItemNames())

    def select_current_index(self):
        selected_items = self.checkedItems()
        if len(selected_items):
            idx = selected_items[-1].row()
        else:
            idx = 0
        return idx

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        select_all = menu.addAction('Select all')
        unselect_all = menu.addAction('Unselect all')
        invert_selection = menu.addAction('Invert selection')
        action = menu.exec_(event.globalPos())
        if action == select_all:
            for row_idx in range(self.model().rowCount()):
                self.set_checked_state(row_idx, True)
        elif action == unselect_all:
            for row_idx in range(self.model().rowCount()):
                self.set_checked_state(row_idx, False)
        elif action == invert_selection:
            for row_idx in range(self.model().rowCount()):
                state = self.get_checked_state(row_idx)
                self.set_checked_state(row_idx, not state)
        self.selectedItemsChanged.emit(True)

    def set_checked_state(self, idx, state):
        checked = QtCore.Qt.Checked if state else QtCore.Qt.Unchecked
        self.model().item(idx).setCheckState(checked)

    def get_checked_state(self, idx):
        return bool(self.model().item(idx).checkState())

    def checkedItems(self):
        selected_items = []
        for row_idx in range(self.model().rowCount()):
            item = self.model().item(row_idx)
            if item is not None and bool(item.checkState()):
                selected_items.append(item)
        return selected_items

    def checkedItemNames(self):
        return [item.text() for item in self.checkedItems()]

    def add_item(self, text, checked=False):
        item = QtGui.QStandardItem(text)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                      QtCore.Qt.ItemIsEnabled)
        is_checked = QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked
        item.setData(is_checked, QtCore.Qt.CheckStateRole)
        last_idx = self.model().rowCount()
        self.model().setItem(last_idx, 0, item)


class MacStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        widget = QtWidgets.QCheckBox(index.data(), parent=parent)
        widget.stateChanged[bool].connect(self.stateChanged)
        return widget

    def paint(self, painter, option, index):
        option.showDecorationSelected = False
        super().paint(painter, option, index)

    def setEditorData(self, editor, index):
        editor.setCheckState(index.data(QtCore.Qt.EditRole))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.checkState(), QtCore.Qt.EditRole)

    @QtCore.Slot(bool)
    def stateChanged(self):
        self.commitData.emit(self.sender())


class LineEditDropDownMenuButton(QtWidgets.QToolButton):
    def __init__(self, icon=None, parent=None):
        super().__init__(parent)
        if isinstance(icon, QtGui.QIcon):
            self.setIcon(icon)
            self.setIconSize(QtCore.QSize(14, 14))
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.setStyleSheet(
            """
            QToolButton {
                border: none;
                padding: 0px;
                background-color: white;
            }
            QToolButton:hover { background-color: rgba(0,0,0,30); }
            QToolButton:pressed { background-color: rgba(0,0,0,60); }
            """)


class LineEditComboButton(QtWidgets.QToolButton):
    value_changed = QtCore.Signal(tuple)
    value_edited = QtCore.Signal(tuple)

    def __init__(self, options=None, value=None, parent=None):
        super().__init__(parent=parent)

        self.setCursor(QtCore.Qt.ArrowCursor)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self._options = []
        self._current_value = None
        self._separator = '\t'
        self._menu = QtWidgets.QMenu(parent=self)
        self.setMenu(self._menu)

        if options is None:
            options = []
        elif value is None and options:
            value = options[0]
        self.options = options
        self.current_value = value
        self._menu.triggered.connect(self._state_changed)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        self._options = options
        self._menu.clear()
        self._set_drop_down_items(options)

    @property
    def current_value(self):
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            self._text_changed(value)

    def _set_drop_down_items(self, items):
        self.setEnabled(len(items) > 0)
        for short, description in items:
            action = QtGui.QAction(
                '{}{}{}'.format(description, self._separator, short),
                self._menu)
            self._menu.addAction(action)

    def _state_changed(self, action):
        text = action.text()
        description, short = text.split(self._separator)
        self._text_changed((short, description), edit=True)

    def _text_changed(self, text, edit=False):
        prev = self.current_value
        if isinstance(text, tuple) and text != prev:
            self._current_value = text
            self.setText(text[0])
            if edit:
                self.value_edited.emit(self.current_value)
            self.value_changed.emit(self.current_value)


class LineEditToggleableLabelButton(QtWidgets.QToolButton):
    state_changed = QtCore.Signal(bool)

    def __init__(self, prefix_states=('Off', 'On'), parent=None):
        super().__init__(parent)

        self.setCursor(QtCore.Qt.ArrowCursor)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.prefix_states = prefix_states

        self.setCheckable(True)
        self.setText(self._prefix_states[self.isChecked()])
        self.set_style_sheet()

        self.toggled.connect(self._state_changed)

    def setChecked(self, state):
        super().setChecked(state)
        self._state_changed(state)

    @property
    def prefix_states(self):
        return self._prefix_states

    @prefix_states.setter
    def prefix_states(self, prefix_states):
        self._prefix_states = prefix_states
        self.set_style_sheet()

    def set_style_sheet(self):
        f = monospace_font()
        self.setFont(f)

        fm = QtGui.QFontMetrics(f)
        max_len_prefix = max([fm.horizontalAdvance(p[:3]) for p in
                              self._prefix_states]) + 5

        self.setStyleSheet("""
        QToolButton {
            border: none;
            padding: 0px;
            background-color: rgba(0,0,0,30);
            max-width: %spx;
        }

        QToolButton:hover {
            background-color: rgba(0,0,0,60);
        }

        QToolButton:pressed {
            font-weight: bold;
        }
        """ % (str(max_len_prefix + 2)))

    def _state_changed(self, state):
        self.setText(self._prefix_states[state][:3])
        self.state_changed.emit(state)

    def _handle_menu(self):
        state = self.menu_action2.isChecked() is True
        self._state_changed(state)


class WidgetToolButton(QtWidgets.QToolButton):
    """ToolButton which pops up a widget."""

    def __init__(self, widget, parent=None):
        super().__init__(parent=parent)
        menu = QtWidgets.QMenu()
        self._menu = menu
        self.setMenu(menu)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        action = QtWidgets.QWidgetAction(parent)
        action.setDefaultWidget(widget)
        menu.addAction(action)


class MenuToolButton(QtWidgets.QToolButton):
    """ToolButton which changes active action depending on selection."""
    active_action_changed = QtCore.Signal(QtGui.QAction)

    def __init__(self, active_action, actions, parent=None):
        super().__init__(parent=parent)
        self._actions = actions
        menu = QtWidgets.QMenu()
        # menu.setToolTipsVisible(True)
        for action in actions:
            menu.addAction(action)
        self._menu = menu
        self.setMenu(menu)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.set_active_action(active_action)
        menu.triggered.connect(self._menu_triggered)

    def _menu_triggered(self, action):
        self.setDefaultAction(action)
        self.active_action_changed.emit(action)

    def active_action(self):
        return self.defaultAction()

    def set_active_action(self, action):
        assert action in self._actions, (
            'default_action must be among actions')
        self._menu_triggered(action)


class LeftRightPadMixin:

    def __init__(self, parent=None):
        super().__init__(parent)
        self._left_child_widget = None
        self._right_child_widget = None

    def _widget_width(self, widget):
        return 0 if widget is None else widget.sizeHint().width()

    def _widget_height(self, widget):
        return 0 if widget is None else widget.sizeHint().height()

    def add_widget(self, widget, to_right=True):
        widget.setParent(self)
        if to_right:
            self._right_child_widget = widget
        else:
            self._left_child_widget = widget
        self.update_geometry()

    def remove_widget(self, widget):
        widget.setParent(None)
        if widget is self._left_child_widget:
            self._left_child_widget = None
        if widget is self._right_child_widget:
            self._right_child_widget = None

    def update_geometry(self):
        style = self.style()
        frame_width = style.pixelMetric(
            QtWidgets.QStyle.PM_DefaultFrameWidth)
        left_width = self._widget_width(self._left_child_widget)
        right_width = self._widget_width(self._right_child_widget)
        left_height = self._widget_height(self._left_child_widget)
        right_height = self._widget_height(self._right_child_widget)
        left_padding, right_padding = self._padding(
            left_width, right_width, frame_width)
        self.setStyleSheet(self._stylesheet() % (left_padding, right_padding))
        msz = self.minimumSizeHint()
        self.setMinimumSize(
            max(msz.width(),
                left_width + right_width +
                frame_width * 2 + 52),
            max([self.sizeHint().height(),
                 right_height + frame_width * 2 + 2,
                 left_height + frame_width * 2 + 2]))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        frame_width = self.style().pixelMetric(
            QtWidgets.QStyle.PM_DefaultFrameWidth)
        rect = self.rect()
        right_width = self._widget_width(self._right_child_widget)
        left_height = self._widget_height(self._left_child_widget)
        right_height = self._widget_height(self._right_child_widget)
        if self._left_child_widget:
            self._left_child_widget.move(
                frame_width + 1,
                (rect.bottom() + 1 - left_height) / 2)
        if self._right_child_widget:
            self._right_child_widget.move(
                rect.right() - frame_width - right_width,
                (rect.bottom() + 1 - right_height) / 2)


class BaseLineTextEdit(LeftRightPadMixin, QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(100)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def sizeHint(self):
        fm = QtGui.QFontMetrics(self.font())
        opt = QtWidgets.QStyleOptionFrame()
        text = self.document().toPlainText()

        h = max(fm.height(), 14) + 4
        w = fm.horizontalAdvance(text) + 4

        opt.initFrom(self)

        o = (self.style().sizeFromContents(QtWidgets.QStyle.CT_LineEdit,
                                           opt,
                                           QtCore.QSize(w, h),
                                           self))
        return o

    def _stylesheet(self):
        return """
        QTextEdit {
            padding-left: %spx;
            padding-right: %spx;
        }
        """

    def _padding(self, left_width, right_width, frame_width):
        left_padding = left_width + frame_width + 1
        left_padding += 0 if not self._left_child_widget else 5
        right_padding = right_width + frame_width + 1
        return left_padding, right_padding


class BaseLineEdit(LeftRightPadMixin, QtWidgets.QLineEdit):

    def __init__(self, inactive="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(inactive)
        self.setMinimumWidth(100)
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(1)
        policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(policy)

    def _stylesheet(self):
        return """
        QLineEdit {
            padding-left: %spx;
            padding-right: %spx;
        }
        """

    def _padding(self, left_width, right_width, frame_width):
        return (left_width + frame_width + 1,
                right_width + frame_width + 1)


class ClearButtonLineEdit(QtWidgets.QLineEdit):
    def __init__(self, placeholder="", clear_button=True, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        if clear_button:
            self.setClearButtonEnabled(True)


class PrefixLineEdit(BaseLineEdit):
    def __init__(self, placeholder="", prefix="", parent=None):
        super().__init__(placeholder, parent)

        self.prefix_label = QtWidgets.QLabel(prefix, parent=self)
        self.add_widget(self.prefix_label, to_right=False)

    def set_prefix(self, prefix):
        self.prefix_label.setText(prefix)


class ToggleablePrefixLineEdit(BaseLineEdit):
    state_toggled = QtCore.Signal(bool)

    def __init__(self, placeholder="", state=True, prefix_states=('Off', 'On'),
                 parent=None):
        super().__init__(placeholder, parent)

        assert (len(prefix_states) == 2)
        self.prefix_button = LineEditToggleableLabelButton(
            prefix_states=prefix_states, parent=self)
        self.prefix_button.setChecked(state)
        self.add_widget(self.prefix_button, to_right=False)

        self.prefix_button.state_changed.connect(self.state_toggled)

    def get_state(self):
        return self.prefix_button.isChecked()

    def set_state(self, state):
        self.prefix_button.setChecked(state)

    def set_prefix_states(self, prefix_states):
        if len(prefix_states) == 2:
            self.prefix_button.set_prefix_states(prefix_states)


class MenuLineEdit(BaseLineEdit):
    state_changed = QtCore.Signal(tuple)
    state_edited = QtCore.Signal(tuple)

    def __init__(self, placeholder="", options=None, value=None, parent=None):
        super().__init__(placeholder, parent)
        self.prefix_button = LineEditComboButton(
            options=options, value=value, parent=self)
        self.add_widget(self.prefix_button, to_right=False)
        self.prefix_button.value_edited.connect(self.state_edited)
        self.prefix_button.value_changed.connect(self.state_changed)

    @property
    def current_value(self):
        return self.prefix_button.current_value

    @current_value.setter
    def current_value(self, value):
        self.prefix_button.current_value = value


class SyBaseToolBar(QtWidgets.QToolBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(self.construct_style_sheet())

    def construct_style_sheet(self):
        return toolbar_stylesheet % (self.get_parent_color(),
                                     self.get_border_color())

    def get_parent_color(self):
        color = self.palette().color(self.backgroundRole())
        return color.name()

    def get_border_color(self):
        color = self.palette().color(QtGui.QPalette.Mid)
        return color.name()


class TogglePushButton(QtWidgets.QPushButton):
    def __init__(self, *args, parent=None):
        super().__init__(*args, parent=parent)
        self.setCheckable(True)


def folder_icon(style):
    icon = QtGui.QIcon()
    icon.addPixmap(
        style.standardPixmap(QtWidgets.QStyle.SP_DirClosedIcon),
        QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon.addPixmap(
        style.standardPixmap(QtWidgets.QStyle.SP_DirOpenIcon),
        QtGui.QIcon.Normal, QtGui.QIcon.On)
    return icon


def file_icon(style):
    icon = QtGui.QIcon()
    icon.addPixmap(
        style.standardPixmap(QtWidgets.QStyle.SP_FileIcon))
    return icon


def messagebox_critical_icon(style):
    icon = QtGui.QIcon()
    icon.addPixmap(
        style.standardPixmap(QtWidgets.QStyle.SP_MessageBoxCritical))
    return icon


def messagebox_warning_icon(style):
    icon = QtGui.QIcon()
    icon.addPixmap(
        style.standardPixmap(QtWidgets.QStyle.SP_MessageBoxWarning))
    return icon


def messagebox_question_icon(style):
    icon = QtGui.QIcon()
    icon.addPixmap(
        style.standardPixmap(QtWidgets.QStyle.SP_MessageBoxQuestion))
    return icon


def browser_reload_icon(style):
    icon = QtGui.QIcon()
    icon.addPixmap(
        style.standardPixmap(QtWidgets.QStyle.SP_BrowserReload))
    return icon


def preview_icon():
    pixmap = QtGui.QPixmap(prim.get_icon_path(
        'node_open.svg'))
    return QtGui.QIcon(pixmap)


class PreviewButton(TogglePushButton):
    def __init__(self, parent=None):
        super().__init__(preview_icon(), 'Preview')


def filter_icon():
    pixmap = QtGui.QPixmap(prim.get_icon_path(
        'actions/view-filter-symbolic.svg'))
    return QtGui.QIcon(pixmap)


class FilterButton(TogglePushButton):
    def __init__(self, parent=None):
        super().__init__(filter_icon(), '')
        self.setFlat(True)


def edit_icon():
    pixmap = QtGui.QPixmap(prim.get_icon_path(
        'actions/fontawesome/svgs/solid/edit.svg'))
    return QtGui.QIcon(pixmap)


def copy_icon():
    pixmap = QtGui.QPixmap(prim.get_icon_path(
        'actions/fontawesome/svgs/regular/copy.svg'))
    return QtGui.QIcon(pixmap)


class EditButton(TogglePushButton):
    def __init__(self, parent=None):
        super().__init__(edit_icon(), '')
        self.setFlat(True)


class ShowButton(TogglePushButton):
    def __init__(self, parent=None):
        super().__init__(preview_icon(), '')
        self.setToolTip('Show/Hide.')


class ToggleFilterButton(FilterButton):
    def __init__(self, filter_widget=None, next_to_widget=None):
        """
        Button with a magnifying glass intended for toggling
        the display of filter options.

        If a filter_widget is provided it will automatically
        be connected and hidden by default.

        When placing it next to another widget it will look best if the height
        is the same: use set_size or next_to_widget.
        """
        super().__init__()
        self.setToolTip('Show/Hide filter.')
        self.setCheckable(True)
        self.setFlat(True)

        self._filter_widget = filter_widget
        if self._filter_widget:
            # Default hidden.
            self._filter_widget.hide()
            self.toggled.connect(self._toggled)

        if next_to_widget:
            # TODO(erik): Assuming a 1px border (which is not always true).
            # Next to a combobox seems good on Windows 10 and worse on Mac OS.
            size = next_to_widget.sizeHint().height() + 2
            self.set_size(size)

    def set_size(self, size):
        self.setIconSize(QtCore.QSize(size, size))
        self.setFixedSize(size, size)

    def _toggled(self, checked=False):
        if checked:
            self._filter_widget.show()
        else:
            self._filter_widget.hide()


class TogglePreviewButton(TogglePushButton):
    def __init__(self, child_widget=None, next_to_widget=None):
        """
        Button with a eye icon intended for toggling
        the display of preview.

        If a child_widget is provided it will automatically
        be connected and hidden by default.

        When placing it next to another widget it will look best if the height
        is the same: use set_size or next_to_widget.
        """
        icon = preview_icon()
        super().__init__(icon, '')
        self.setToolTip('Show/Hide preview.')
        self.setFlat(True)

        self._child_widget = child_widget
        if self._child_widget:
            # Default hidden.
            self._child_widget.hide()
            self.toggled.connect(self._toggled)

        if next_to_widget:
            # TODO(erik): Assuming a 1px border (which is not always true).
            # Next to a combobox seems good on Windows 10 and worse on Mac OS.
            size = next_to_widget.sizeHint().height() + 2
            self.set_size(size)

    def set_size(self, size):
        self.setIconSize(QtCore.QSize(size, size))
        self.setFixedSize(size, size)

    def _toggled(self, checked=False):
        if checked:
            self._child_widget.show()
        else:
            self._child_widget.hide()


class SortedSearchFilterModel(QtCore.QSortFilterProxyModel):
    """
    Search filter model which sorts the data in ascending order.
    """
    filter_changed = qt_compat2.Signal(str)

    def __init__(self, parent=None):
        self._filter = None
        super().__init__(parent)

    def set_filter(self, filter):
        if filter is not None:
            self._filter = search.fuzzy_free_pattern(filter)
            self.invalidateFilter()
        self.filter_changed.emit(filter)

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        if self._filter is None or model is None:
            return True
        index = model.index(
            source_row, model.columnCount() - 1, source_parent)
        data = model.data(index, self.filterRole())
        if data is None:
            return True
        return search.matches(self._filter, data)


class OrderedSearchFilterModel(SortedSearchFilterModel):
    """
    Search Filter model which keeps the ordering from the source
    model.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def lessThan(self, left, right):
        return self.mapFromSource(left).row() < self.mapFromSource(right).row()


class OrderedComboboxSearchFilterModel(OrderedSearchFilterModel):
    """
    Search Filter model which keeps the ordering from the source
    model.

    For convenience also creates a new combobox model which is set as
    source model.
    """

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setSourceModel(model)

    def clear(self):
        self.sourceModel().clear()


class ToggleFilterCombobox(QtWidgets.QWidget):
    currentIndexChanged = qt_compat2.Signal(int)

    def __init__(self, combobox, use_filter=True, parent=None):
        super().__init__(parent=parent)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setSpacing(0)

        self._combobox = combobox

        # SortedSearchFilterModel
        self._search_model = self._combobox.model()
        self._filter_widget = ClearButtonLineEdit(
            placeholder='Filter')

        hlayout.addWidget(self._combobox)
        self._filter_button = ToggleFilterButton(
            filter_widget=self._filter_widget,
            next_to_widget=self._combobox)

        if use_filter:
            hlayout.addWidget(self._filter_button)

        vlayout.addLayout(hlayout)
        vlayout.addWidget(self._filter_widget)
        self.setLayout(vlayout)
        self._combobox.currentIndexChanged[int].connect(
            self.currentIndexChanged)
        self._search_model.setFilterRole(QtCore.Qt.DisplayRole)
        self._search_model.set_filter('')
        self._filter_widget.textChanged.connect(self._search_model.set_filter)
        self._search_model.filter_changed.connect(self._filter_changed)

    def _filter_changed(self, filter):
        # Auto-select after filtering if nothing nothing is already selected.
        if filter and self._combobox.currentIndex() == -1:
            index = self._search_model.index(
                self._search_model.rowCount() - 1,
                self._search_model.columnCount() - 1)

            if index.isValid():
                src_index = self._search_model.mapToSource(index)
                self._combobox.setCurrentIndex(src_index.row())

    def addItems(self, items):
        items = items
        for text in items:
            item = QtGui.QStandardItem(text)
            self._search_model.sourceModel().appendRow(item)
        self._search_model.set_filter(self._filter_widget.text())

    def clear(self):
        # Clear combobox first to improve performance.
        self._combobox.clear()
        self._search_model.sourceModel().clear()

    def combobox(self):
        return self._combobox


# TODO(erik): refactor, move to appropriate utility module?
def create_action(text, icon=None, icon_name=None, tooltip_text=None,
                  is_checkable=False, is_checked=False,
                  triggered=None, toggled=None, parent=None):
    """
    Convenience function for creating an action and optionally
    connecting it.

    Many properties can be specified: text, icon, tooltip, checkable,
    checked.

    Signal handlers can be specified using: triggered and toggled.
    """
    if icon is None:
        if icon_name is not None:
            icon = QtGui.QIcon(prim.get_icon_path(icon_name))
        else:
            icon = None

    if icon is None:
        action = QtGui.QAction(text, parent=parent)
    else:
        action = QtGui.QAction(icon, text, parent=parent)

    if tooltip_text is not None:
        action.setToolTip(tooltip_text)
    if is_checkable:
        action.setCheckable(is_checkable)
        action.setChecked(is_checked)

    if triggered:
        action.triggered.connect(triggered)
    if toggled:
        action.toggled.connect(toggled)
    return action


class SyToolBar(SyBaseToolBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumHeight(22)
        self.setMaximumHeight(38)
        self.setIconSize(QtCore.QSize(26, 26))

    def add_action(self, text, icon_name=None, tooltip_text=None,
                   is_checkable=False, is_checked=False,
                   receiver=None, triggered=None, toggled=None, icon=None):
        """
        Convenience method for creating an action and adding it.
        The action is created using create_action and the toolbar becomes
        the parent.

        Returns created action.
        """
        triggered = triggered or receiver

        action = create_action(text,
                               icon_name=icon_name,
                               icon=icon,
                               tooltip_text=tooltip_text,
                               is_checkable=is_checkable,
                               is_checked=is_checked,
                               triggered=triggered,
                               toggled=toggled,
                               parent=self)
        self.addAction(action)
        return action

    def addStretch(self):
        spacer = QtWidgets.QWidget(parent=self)
        spacer.setMinimumWidth(0)
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(0)
        policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        spacer.setSizePolicy(policy)
        self.addWidget(spacer)


class BasePreviewTable(QtWidgets.QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWordWrap(False)

        self._context_menu_actions = []

        self.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems)
        self.setSelectionMode(
            QtWidgets.QAbstractItemView.ContiguousSelection)
        self.ScrollHint(
            QtWidgets.QAbstractItemView.EnsureVisible)
        self.setCornerButtonEnabled(True)
        self.setShowGrid(True)
        self.setAlternatingRowColors(True)
        self.setMinimumHeight(100)

        vertical_header = self.verticalHeader()
        vertical_header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        vertical_header.customContextMenuRequested.connect(
            self.vertical_header_context_menu)
        horizontal_header = self.horizontalHeader()
        horizontal_header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        horizontal_header.customContextMenuRequested.connect(
            self.horizontal_header_context_menu)
        self.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollPerPixel)

    def vertical_header_context_menu(self, pos):
        if not self._context_menu_actions:
            return
        header = self.verticalHeader()
        row_idx = header.logicalIndexAt(pos)
        self._show_context_menu(row_idx, -1, header.mapToGlobal(pos))

    def horizontal_header_context_menu(self, pos):
        if not self._context_menu_actions:
            return
        header = self.horizontalHeader()
        column_idx = header.logicalIndexAt(pos)
        self._show_context_menu(-1, column_idx, header.mapToGlobal(pos))

    def contextMenuEvent(self, event):
        if not self._context_menu_actions:
            return

        global_pos = event.globalPos()
        pos = self.viewport().mapFromGlobal(global_pos)
        qindex = self.indexAt(pos)
        row_idx = qindex.row()
        column_idx = qindex.column()

        self._show_context_menu(row_idx, column_idx, global_pos)
        event.accept()

    def _show_context_menu(self, row, column, pos):
        current_menu_items = self.create_menu(row, column)
        action = self.menu.exec_(pos)
        if action:
            callback = current_menu_items[action]
            callback(row, column)

    def create_menu(self, row_idx, column_idx):
        self.menu = QtWidgets.QMenu(self)
        current_menu_items = {}
        for action_param in self._context_menu_actions:
            title, func, icon_name, validate_func = action_param

            is_valid = validate_func(row_idx, column_idx)
            if is_valid:
                if icon_name is not None:
                    icon = QtGui.QIcon(prim.get_icon_path(icon_name))
                    action = self.menu.addAction(icon, title)
                else:
                    action = self.menu.addAction(title)
                current_menu_items[action] = func
        return current_menu_items

    def add_context_menu_action(self, title, function, icon_name=None,
                                validate_callback=None, key_sequence=None):
        # Create a separate action for the shortcut:
        if validate_callback is None:
            def validate_callback(row, col): True
        if key_sequence is not None:
            if icon_name is not None:
                icon = QtGui.QIcon(prim.get_icon_path(icon_name))
                action = QtGui.QAction(icon, title, self)
            else:
                action = QtGui.QAction(title, self)
            action.setShortcuts(key_sequence)
            action.triggered.connect(
                lambda: self._emit_context_menu_clicked(function))
            self.addAction(action)

        self._context_menu_actions.append((title, function, icon_name,
                                           validate_callback))

    def _emit_context_menu_clicked(self, callback, row=0, column=0):
        callback(row, column)

    def selection(self):
        """
        Return a tuple with two ranges (startrow, endrow, startcol, endcol) for
        the currently selected area. Both ranges are half closed meaning that
        e.g. rows where startrow <= row < endrow are selected.
        """
        selection_model = self.selectionModel()
        if not selection_model.selection().count():
            return None
        selection_range = selection_model.selection()[0]
        minrow, maxrow = selection_range.top(), selection_range.bottom() + 1
        mincol, maxcol = selection_range.left(), selection_range.right() + 1
        return (minrow, maxrow, mincol, maxcol)

    def center_on_cell(self, row=None, col=None):
        if row is None:
            row = max(self.rowAt(0), 0)
        if col is None:
            col = max(self.columnAt(0), 0)

        index = self.model().createIndex(row, col, 0)
        if index.isValid():
            self.scrollTo(index)


class EnhancedPreviewTable(QtWidgets.QWidget):
    def __init__(self, model=None, filter_function=None, parent=None):
        super().__init__(parent)

        if model is None:
            model = QtCore.QAbstractItemModel()
        self._model = model
        self._transposed = False
        self._filter_function = filter_function

        self._preview_table = BasePreviewTable()

        # Toolbar
        self._toolbar = SyToolBar()
        # Search field
        self._filter_lineedit = ClearButtonLineEdit(placeholder='Search',
                                                    parent=self)
        self._filter_lineedit.setMaximumWidth(250)

        self._toolbar.addWidget(self._filter_lineedit)
        self._toolbar.addStretch()

        # Legend
        self._legend_layout = QtWidgets.QHBoxLayout()
        self._legend_layout.addStretch()

        # Setup layout
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._toolbar)
        layout.addWidget(self._preview_table)
        layout.addLayout(self._legend_layout)

        self.setLayout(layout)

        # Connect signals
        self._filter_lineedit.textChanged[str].connect(
            self._filter_columns)

        self.set_model(self._model, self._transposed)

    def preview_table(self):
        return self._preview_table

    def toolbar(self):
        return self._toolbar

    def _show_all(self):
        """
        Show all items in the table.
        This method is expensive so don't call it if the table is too big.
        """
        headers = [self._preview_table.horizontalHeader(),
                   self._preview_table.verticalHeader()]
        for header in headers:
            for i in range(header.count()):
                header.showSection(i)

    def _filter_columns(self, pattern):
        try:
            table = self._model.table()
        except AttributeError:
            self._show_all()
            return
        if table is None:
            # No table available for filtering. This probably means that we are
            # currently showing attributes, so simply show all rows and
            # columns.
            self._show_all()
            return

        columns = [table.col(name) for name in table.column_names()]
        item_count = len(columns)

        filter_func = self._filter_function
        if filter_func is None:
            # Fall back to showing all columns
            self._show_all()
            return

        filtered_item_indexes = set(filter_func(pattern, columns))

        if self._transposed:
            set_hidden = self._preview_table.setRowHidden
        else:
            set_hidden = self._preview_table.setColumnHidden
        for i in range(item_count):
            set_hidden(i, i not in filtered_item_indexes)

    def reapply_filter(self):
        filter_pattern = self._filter_lineedit.text()
        self._filter_lineedit.textChanged.emit(filter_pattern)

    def clear_filter(self):
        self._filter_lineedit.textChanged.emit('')

    def set_model(self, model, transposed):
        # Temporary reset the filter to make sure that all columns and rows are
        # shown before changing the model.
        self.clear_filter()
        self._model = model
        self._transposed = transposed
        self._preview_table.setModel(model)
        self.reapply_filter()

    def set_filter_function(self, func):
        self._filter_function = func

    def add_widget_to_legend(self, widget, on_left=False):
        legend_layout = self._legend_layout
        if on_left:
            legend_layout.insertWidget(0, widget)
        else:
            legend_layout.addWidget(widget)

    def add_widget_to_layout(self, widget, on_top=False):
        layout = self.layout()
        if on_top:
            layout.insertWidget(0, widget)
        else:
            layout.addWidget(widget)

    def add_layout_to_layout(self, layout, on_top=False):
        main_layout = self.layout()
        if on_top:
            main_layout.insertLayout(0, layout)
        else:
            main_layout.addLayout(layout)


class RowColumnLegend(QtWidgets.QGroupBox):
    def __init__(self, row=0, column=0, parent=None):
        super().__init__(parent)
        self._row = row
        self._column = column
        self._init_gui()

    def _init_gui(self):
        self._row_column_label = QtWidgets.QLabel()
        self._row_column_label.setMaximumHeight(16)

        row_count_layout = QtWidgets.QHBoxLayout()
        row_count_layout.setContentsMargins(0, 0, 0, 0)
        row_count_layout.setAlignment(QtCore.Qt.AlignCenter)
        icon_label = QtWidgets.QLabel()
        icon = QtGui.QPixmap(prim.get_icon_path(
            'actions/view-grid-symbolic.svg'))
        icon_label.setPixmap(icon)
        row_count_layout.addWidget(icon_label)
        row_count_layout.addWidget(self._row_column_label)

        self.setLayout(row_count_layout)
        self._update_row_column_label()

    def _update_row_column_label(self):
        text = '{} \u00D7 {}'.format(self._row, self._column)
        self._row_column_label.setText(text)
        tooltip = '{} row{}<br>{} column{}'.format(
            self._row, '' if self._row == 1 else 's',
            self._column, '' if self._column == 1 else 's')
        self.setToolTip(tooltip)

    def set_row(self, row):
        self._row = row
        self._update_row_column_label()

    def set_column(self, column):
        self._column = column
        self._update_row_column_label()

    def set_row_column(self, row, column):
        self._row = row
        self._column = column
        self._update_row_column_label()


class PathMixinWidget(QtWidgets.QWidget):
    """
    Mixin which adds context menu actions *Make absolute* and *Make relative*
    to self._editor. It also provides a few helpers.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        make_relative = QtGui.QAction(
            'Make relative', self._editor)
        make_absolute = QtGui.QAction('Make absolute', self._editor)
        self._editor.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self._editor.addAction(make_relative)
        self._editor.addAction(make_absolute)
        make_relative.triggered.connect(self._make_relative)
        make_absolute.triggered.connect(self._make_absolute)

    def _make_default_path(self, path):
        """Helper for making the default kind of path."""
        res = path
        if self._default_relative and self._root_path is not None:
            res = self._make_relative_path(path)
        return res

    def _make_relative_path(self, path):
        """Helper for making relative path out of path."""
        res = path
        if os.path.isabs(path):
            try:
                res = os.path.relpath(path, self._root_path)
            except Exception:
                pass
        return res

    def _make_absolute_path(self, path):
        """Helper for making absolute path out of path."""
        res = path
        try:
            res = os.path.normpath(
                os.path.join(self._root_path, path))
        except Exception:
            pass
        return res


class PathListWidget(PathMixinWidget):
    """
    Widget with a list of paths, buttons to add remove paths and some utilities
    for handling relative/absolute paths.
    """
    def __init__(self, paths, root_path=None, default_relative=False,
                 recent=None, parent=None):
        self._root_path = root_path
        self._default_relative = default_relative
        self._editor = QtWidgets.QListWidget()
        self._editor.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self._editor.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self._recent = recent

        super().__init__(parent)
        self.set_items(paths)

        remove_action = QtGui.QAction('Remove items', self._editor)
        remove_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete))
        remove_action.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self._editor.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self._editor.addAction(remove_action)
        remove_action.triggered.connect(self._remove_path)
        add_button = QtWidgets.QPushButton('Add')
        remove_button = QtWidgets.QPushButton('Remove')

        buttons_container = QtWidgets.QVBoxLayout()
        buttons_container.addWidget(add_button)
        buttons_container.addWidget(remove_button)
        if recent is not None:
            recent_button = QtWidgets.QPushButton('Recent')
            buttons_container.addWidget(recent_button)
            menu = QtWidgets.QMenu(recent_button)
            for i, item in enumerate(recent, 1):
                action = menu.addAction(item)
                action.triggered.connect(functools.partial(
                    lambda item: self._add_item(item), item))
            recent_button.setMenu(menu)
        buttons_container.addStretch()

        container = QtWidgets.QHBoxLayout()
        container.setContentsMargins(1, 1, 1, 1)
        container.addWidget(self._editor)
        container.addLayout(buttons_container)
        self.setLayout(container)

        add_button.clicked.connect(self._add_path_dialog)
        remove_button.clicked.connect(self._remove_path)

    def add_item(self, path):
        self._add_item(path)

    def set_items(self, paths):
        self._editor.clear()
        for path in paths:
            self._add_item(path)
        self._initial_paths = list(paths)

    def _add_item(self, path):
        """Append a path to the list."""
        item = QtWidgets.QListWidgetItem(path)
        item.setFlags(QtCore.Qt.ItemIsEnabled |
                      QtCore.Qt.ItemIsSelectable |
                      QtCore.Qt.ItemIsEditable |
                      QtCore.Qt.ItemIsDragEnabled)
        self._editor.addItem(item)

    def _add_path_dialog(self):
        """Open a dialog to let the user select a directory, which is added."""
        default_directory = self._root_path or settings.get_default_dir()
        dir_ = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Choose a directory', default_directory)
        if len(dir_) > 0:
            dir_ = self._make_default_path(dir_)
            self._add_item(dir_)

    def _make_relative(self):
        """Make all selected paths relative."""
        if len(self._editor.selectedItems()) > 0:
            for selected_item in self._editor.selectedItems():
                old_path = selected_item.text()
                new_path = self._make_relative_path(old_path)
                if old_path != new_path:
                    self._editor.model().setData(
                        self._editor.indexFromItem(selected_item), new_path,
                        QtCore.Qt.DisplayRole)

    def _make_absolute(self):
        """Make all selected paths absolute."""
        if len(self._editor.selectedItems()) > 0:
            for selected_item in self._editor.selectedItems():
                old_path = selected_item.text()
                new_path = self._make_absolute_path(old_path)
                if old_path != new_path:
                    self._editor.model().setData(
                        self._editor.indexFromItem(selected_item), new_path,
                        QtCore.Qt.DisplayRole)

    def _remove_path(self):
        """Remove all selected paths."""
        if len(self._editor.selectedItems()) > 0:
            for selected_item in self._editor.selectedItems():
                row = self._editor.row(selected_item)
                self._editor.takeItem(row)
                del selected_item

    def paths(self):
        """Return a list of all paths in the list."""
        row_count = self._editor.model().rowCount(QtCore.QModelIndex())
        return [self._editor.item(i).text()
                for i in range(row_count)]

    def recent(self):
        new_recent_libs = []
        new_libs = [path for path in self.paths()
                    if path not in self._initial_paths]
        recent_libs = self._recent or []

        for lib in new_libs + recent_libs:
            if lib not in new_recent_libs:
                new_recent_libs.append(lib)
        return new_recent_libs

    def clear(self):
        self._editor.clear()


class PathLineEdit(PathMixinWidget):
    """
    Widget with a single path editor and some utilities
    for handling relative/absolute paths.
    """

    def __init__(self, path, root_path=None, default_relative=False,
                 placeholder_text=None, filter=None, parent=None):
        self._root_path = root_path
        self._default_relative = default_relative
        self._filter = filter
        self._editor = QtWidgets.QLineEdit()
        self._editor.setText(path or '')
        if placeholder_text:
            self._editor.setPlaceholderText(placeholder_text)

        super().__init__(parent)
        self._editor.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        dialog_button = QtWidgets.QPushButton('...')
        container = QtWidgets.QHBoxLayout()
        container.setContentsMargins(1, 1, 1, 1)
        container.addWidget(self._editor)
        container.addWidget(dialog_button)
        self.setLayout(container)
        dialog_button.clicked.connect(self._add_path_dialog)

    def _add_path_dialog(self):
        """Open a dialog to let the user select a directory, which is added."""
        default_directory = self._root_path or settings.get_default_dir()
        fq_filename = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select file", default_directory, self._filter)[0]
        if len(fq_filename) > 0:
            fq_filename = self._make_default_path(fq_filename)
            self._change_item(fq_filename)

    def _change_item(self, path):
        """Change current itemt."""
        self._editor.setText(path)

    def _make_relative(self):
        """Make all selected paths relative."""
        old_path = self._editor.text()
        new_path = self._make_relative_path(old_path)
        if old_path != new_path:
            self._editor.setText(new_path)

    def _make_absolute(self):
        """Make all selected paths absolute."""
        old_path = self._editor.text()
        new_path = self._make_absolute_path(old_path)
        if old_path != new_path:
            self._editor.setText(new_path)

    def path(self):
        return self._editor.text()


class StackedTextViews(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._combo = QtWidgets.QComboBox()
        self._stacked = QtWidgets.QStackedWidget()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._combo)
        layout.addWidget(self._stacked)
        self.setLayout(layout)

        self._combo.currentIndexChanged[int].connect(
            self._stacked.setCurrentIndex)

    def add_text(self, label, text):
        text_edit = SyTextEdit(text)
        text_edit.setReadOnly(True)
        self._combo.addItem(label)
        self._stacked.addWidget(text_edit)


class SearchBar(SyBaseToolBar):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setMinimumHeight(22)
        self.setMaximumHeight(38)
        self.setIconSize(QtCore.QSize(18, 18))

        style = self.style()

        self._line_edit = QtWidgets.QLineEdit()
        self._line_edit.setPlaceholderText('Find in text')
        self._line_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.find_action = QtGui.QAction('Find', parent=self)
        self.find_action.setShortcutContext(
            QtCore.Qt.WidgetWithChildrenShortcut)
        self.find_action.setShortcut(QtGui.QKeySequence.Find)
        self.find_action.setShortcutVisibleInContextMenu(True)

        self.forward_action = QtGui.QAction(
            'Find Next', parent=self)
        self.forward_action.setShortcutContext(
            QtCore.Qt.WidgetWithChildrenShortcut)
        self.forward_action.setShortcut(QtGui.QKeySequence.FindNext)
        self.forward_action.setShortcutVisibleInContextMenu(True)

        self.backward_action = QtGui.QAction(
            'Find Previous', parent=self)
        self.backward_action.setShortcutContext(
            QtCore.Qt.WidgetWithChildrenShortcut)
        self.backward_action.setShortcut(QtGui.QKeySequence.FindPrevious)
        self.backward_action.setShortcutVisibleInContextMenu(True)

        self.close_action = QtGui.QAction(parent=self)

        self.backward_action.setIcon(QtGui.QIcon(prim.get_icon_path(
            'actions/go-up-symbolic.svg')))
        self.forward_action.setIcon(QtGui.QIcon(prim.get_icon_path(
            'actions/go-down-symbolic.svg')))
        self.close_action.setIcon(style.standardIcon(
            QtWidgets.QStyle.SP_LineEditClearButton))

        self._line_edit.addAction(self.backward_action)
        self._line_edit.addAction(self.forward_action)

        self.addAction(self.close_action)
        self.addWidget(self._line_edit)
        self.addAction(self.backward_action)
        self.addAction(self.forward_action)

        self.close_action.triggered.connect(self.close)
        self.find_action.triggered.connect(self._find)
        self._line_edit.customContextMenuRequested.connect(
            self._custom_lineedit_context_menu)

    def _find(self, *args, **kwargs):
        self.open()

    def _custom_lineedit_context_menu(self, pos):
        pos = self._line_edit.mapToGlobal(pos)
        menu = self._line_edit.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction(self.find_action)
        if self.isVisible():
            menu.addAction(self.backward_action)
            menu.addAction(self.forward_action)
        menu.exec_(pos)

    def text(self):
        return self._line_edit.text()

    def open(self):
        self.show()
        QtCore.QTimer.singleShot(0, self._line_edit.setFocus)
        QtCore.QTimer.singleShot(0, self._line_edit.selectAll)

    def close(self):
        self.hide()


class SearchableTextEdit(QtWidgets.QWidget):
    textChanged = qt_compat2.Signal()

    def __init__(self, text_edit, search_bar, parent=None):
        super().__init__(parent=parent)
        self._search_bar = search_bar
        self._text_edit = text_edit

        self.addAction(self._search_bar.find_action)
        self.addAction(self._search_bar.forward_action)
        self.addAction(self._search_bar.backward_action)

        self._text_edit.addAction(self._search_bar.find_action)
        self._text_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._text_edit)
        self._search_bar.hide()
        layout.addWidget(self._search_bar)
        self.setLayout(layout)

        self._search_bar.forward_action.triggered.connect(
            self._forward_search)
        self._search_bar.backward_action.triggered.connect(
            self._backward_search)
        self._text_edit.textChanged.connect(self.textChanged)
        self._text_edit.customContextMenuRequested.connect(
            self._custom_textedit_context_menu)

    def _forward_search(self, *args, **kwargs):
        term = self._search_term()
        if term:
            self._text_edit.find(term)

    def _backward_search(self, *args, **kwargs):
        term = self._search_term()
        if term:
            self._text_edit.find(term, QtGui.QTextDocument.FindBackward)

    def _search_term(self):
        if self._search_bar.isVisible():
            return self._search_bar.text()
        return ''

    def _custom_textedit_context_menu(self, pos):
        pos = self._text_edit.mapToGlobal(pos)
        menu = self._text_edit.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction(self._search_bar.find_action)
        if self._search_bar.isVisible():
            menu.addAction(self._search_bar.backward_action)
            menu.addAction(self._search_bar.forward_action)
        menu.exec_(pos)

    # Intended to more or less satisfy QTextEdit interface.
    # Please forward whatever methods and signals that are needed.

    def toPlainText(self):
        return self._text_edit.toPlainText()

    def setPlainText(self, text):
        return self._text_edit.setPlainText(text)

    def toHtml(self):
        return self._text_edit.toHtml()

    def setHtml(self, text):
        return self._text_edit.setHtml(text)

    def setText(self, text):
        return self._text_edit.setText(text)

    def textCursor(self):
        return self._text_edit.textCursor()

    def setTextCursor(self, cursor):
        return self._text_edit.setTextCursor(cursor)

    def isReadOnly(self):
        return self._text_edit.isReadOnly()

    def setReadOnly(self, ro):
        return self._text_edit.setReadOnly(ro)

    def wordWrapMode(self, policy):
        return self._text_edit.wordWrapMode()

    def setWordWrapMode(self, policy):
        return self._text_edit.setWordWrapMode(policy)

    def document(self):
        return self._text_edit.document()

    def setDocument(self, document):
        return self._text_edit.setDocument(document)

    def font(self):
        return self._text_edit.font()

    def setFont(self, font):
        return self._text_edit.setFont(font)


class ReplaceDropTextEdit(QtWidgets.QTextEdit):
    _sub_pattern = None

    def insertFromMimeData(self, source):
        text_plain = 'text/plain'
        if self._sub_pattern and source.hasFormat(text_plain):
            mime = QtCore.QMimeData()
            pattern, replace = self._sub_pattern
            mime.setData(
                text_plain,
                re.sub(pattern, replace, source.data(text_plain)))
            source = mime
        super().insertFromMimeData(source)

    def set_drop_sub_pattern(self, pattern):
        self._sub_pattern = pattern


class SyTextEdit(SearchableTextEdit):
    def __init__(self, text=None, parent=None):
        if text:
            text_edit = ReplaceDropTextEdit(text)
        else:
            text_edit = ReplaceDropTextEdit()

        search_bar = SearchBar()
        super().__init__(text_edit, search_bar, parent=parent)
        self._text_edit.setAcceptRichText(False)

    def set_drop_sub_pattern(self, pattern):
        self._text_edit.set_drop_sub_pattern(pattern)


class CodeEditMixin(object):
    def __init__(self, language='python', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFont(monospace_font())
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self._language = _pygments_language_factory(language)
        self._highlighter = _pygments_highlighter_factory(self, self._language)
        self.textChanged.connect(self._highlighter.text_changed)


@contextlib.contextmanager
def _cursor_context(cursor: QtGui.QTextCursor):
    anchor = cursor.anchor()
    position = cursor.position()
    yield
    if anchor == position:
        cursor.setPosition(position)
    else:
        cursor.setPosition(anchor)
        cursor.setPosition(position, QtGui.QTextCursor.KeepAnchor)


class CodeEdit(CodeEditMixin, SyTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._text_edit.installEventFilter(self)
        self._text_edit.set_drop_sub_pattern(
            self._language.get_drop_sub_pattern())

    def _selected_text(self, cursor):
        # Qt method produces the paragraph separator in place of newlines
        # which is not suitable for processing.
        return cursor.selectedText().replace('\u2029', '\n')

    def _text_from_position_to_move(
            self, cursor, operation=MoveOperation.Start):
        with _cursor_context(cursor):
            cursor.setPosition(cursor.position())
            cursor.movePosition(operation, MoveMode.KeepAnchor)
            return self._selected_text(cursor)

    def _text_from_position_line(self, cursor):
        with _cursor_context(cursor):
            cursor.movePosition(MoveOperation.StartOfLine, MoveMode.MoveAnchor)
            cursor.movePosition(MoveOperation.EndOfLine, MoveMode.KeepAnchor)
            return self._selected_text(cursor)

    def _text_from_position_to_line_start(self, cursor):
        return self._text_from_position_to_move(
            cursor, operation=MoveOperation.StartOfLine)

    def _text_position(self, text: str) -> Tuple[int, int]:
        # Inefficient position, can be more reliable than
        # blockNumber and positionInBlock (QTextCursor).
        lines = text.split('\n')
        col = len(lines[-1])
        row = len(lines) - 1
        return (row, col)

    def _newline_and_indent(self, cursor):
        text_last_line = self._text_from_position_line(cursor)
        indent_after = None
        if not text_last_line.strip():
            text_before = f'\n{text_last_line}'
        else:
            text_before = self._text_from_position_to_move(
                cursor, MoveOperation.Start)
            text_after = self._text_from_position_to_move(
                cursor, MoveOperation.End)
            pos = self._text_position(text_before)
            indent, indent_after = self._language.get_newline_indent(
                text_before + text_after, pos)
            text_before = f'\n{" " * indent}'

        cursor.insertText(text_before)
        if indent_after is not None:
            position = cursor.position()
            cursor.insertText(f'\n{" " * indent_after}')
            cursor.setPosition(position)
            self._text_edit.setTextCursor(cursor)

    def _leading_indent(self, text, indents=' '):
        return len(text) - len(text.lstrip(indents))

    def _newline_and_same_indent(self, cursor):
        text = self._text_from_position_to_line_start(cursor)
        diff = self._leading_indent(text, '\t ')
        cursor.insertText(f'\n{text[:diff]}')

    def _select_line_before_pos(self, cursor):
        position = cursor.position()
        cursor.movePosition(MoveOperation.StartOfLine, MoveMode.MoveAnchor)
        cursor.setPosition(position, MoveMode.KeepAnchor)

    def _extend_selection_to_lines(self, cursor):
        anchor = cursor.anchor()
        position = cursor.position()
        if anchor >= position:
            position_operation = MoveOperation.StartOfLine
            anchor_operation = MoveOperation.EndOfLine
        else:
            position_operation = MoveOperation.EndOfLine
            anchor_operation = MoveOperation.StartOfLine
        cursor.setPosition(anchor)
        cursor.movePosition(anchor_operation, MoveMode.MoveAnchor)
        cursor.setPosition(position, MoveMode.KeepAnchor)
        cursor.movePosition(position_operation, MoveMode.KeepAnchor)

    def _next_indent(self, line, indent):
        spaces = self._leading_indent(line)
        diff = indent - spaces % indent
        return f'{" " *  diff }{line}'

    def _next_dedent_count(self, line, indent):
        spaces = self._leading_indent(line)
        diff = spaces % indent
        if not diff:
            diff = indent
        return min(spaces, diff)

    def _dedented_line(self, line, count):
        return line[count:]

    def _next_dedent(self, line, indent):
        count = self._next_dedent_count(line, indent)
        return self._dedented_line(line, count)

    def _indent_selection(self, cursor, indent, line_func):
        self._extend_selection_to_lines(cursor)
        position = cursor.position()
        anchor = cursor.anchor()
        selected_text = self._selected_text(cursor)
        selected_lines = selected_text.splitlines()
        selected_lines = [
            line_func(line, indent)
            for line in selected_lines]
        cursor.insertText('\n'.join(selected_lines))
        cursor.setPosition(min(position, anchor), MoveMode.KeepAnchor)
        self._text_edit.setTextCursor(cursor)

    def _indent_info(self, cursor):
        text_before = self._text_from_position_to_move(
            cursor, MoveOperation.Start)
        pos = self._text_position(text_before)
        return pos, self._language.get_indent(text_before)

    def _indent(self, cursor):
        pos, indent = self._indent_info(cursor)
        if cursor.hasSelection():
            self._indent_selection(cursor, indent, self._next_indent)
        else:
            col = pos[1]
            diff = indent - col % indent
            cursor.insertText(" " * diff)

    def _dedent(self, cursor):
        pos, indent = self._indent_info(cursor)
        if cursor.hasSelection():
            self._indent_selection(cursor, indent, self._next_dedent)
        else:
            position = cursor.position()
            text_last_line = self._text_from_position_line(cursor)
            count = self._next_dedent_count(text_last_line, indent)
            line = self._dedented_line(text_last_line, count)
            self._extend_selection_to_lines(cursor)
            cursor.insertText(line)
            col = pos[1]
            diff = 0
            prev_col = col % indent
            if prev_col:
                diff = prev_col
            elif self._leading_indent(line) < col:
                diff = indent
            diff = min(count, diff)
            cursor.setPosition(position - diff)
            self._text_edit.setTextCursor(cursor)

    def _backspace(self, cursor):
        pos, indent = self._indent_info(cursor)
        text_last_line = self._text_from_position_to_line_start(cursor)
        line = self._next_dedent(text_last_line, indent)
        self._select_line_before_pos(cursor)
        cursor.insertText(line)
        self._text_edit.setTextCursor(cursor)

    def eventFilter(self, obj, event):
        res = False
        if event.type() == QEvent.KeyPress and (
                not self._text_edit.isReadOnly()):
            cursor = self._text_edit.textCursor()
            cursor.beginEditBlock()
            event_key = event.key()
            if self._language.supports_indent:
                if event_key == QtCore.Qt.Key_Return:
                    if cursor.hasSelection():
                        cursor.removeSelectedText()
                    self._newline_and_indent(cursor)
                    res = True
            else:
                if event_key == QtCore.Qt.Key_Return:
                    if cursor.hasSelection():
                        cursor.removeSelectedText()
                    self._newline_and_same_indent(cursor)
                    res = True

            if event_key == QtCore.Qt.Key_Tab:
                self._indent(cursor)
                res = True
            elif event_key == QtCore.Qt.Key_Backtab:
                self._dedent(cursor)
                res = True
            elif event_key == QtCore.Qt.Key_Backspace:
                if not cursor.hasSelection():
                    text = self._text_from_position_to_line_start(cursor)
                    if text and not text.strip(' '):
                        self._backspace(cursor)
                        res = True

            cursor.endEditBlock()
            self._text_edit.ensureCursorVisible()
        return res


class PygmentsLanguage:
    """
    Basic pygments language.
    Subclass for special behavior or use `name` to get default behavior.
    """
    name = None
    supports_indent = False
    line_by_line = False

    def __init__(self, name=None):
        if name is not None:
            if self.name:
                raise ValueError('Can not change language name')
            self.name = name

        if self.name is None:
            raise NotImplementedError('Language must be named')

        try:
            self._lexer = _pygments().lexers.get_lexer_by_name(
                self.name, stripall=True)
            self._valid = True
        except _pygments().util.ClassNotFound:
            self._lexer = _pygments().lexers.special.TextLexer()
            self._valid = False

    def get_tokens(self, text):
        return list(self._lexer.get_tokens_unprocessed(text))

    def get_style(self, style):
        try:
            res = _pygments().styles.get_style_by_name(style), not self._valid
        except _pygments().util.ClassNotFound:
            # Returning True will block highlight.
            res = _pygments().styles.get_style_by_name('default'), True
        return res

    def get_indent(self, text: str) -> int:
        """Number of spaces of indentation per level."""
        return 4

    def get_newline_indent(self, text: str, pos: Tuple[int, int]
                           ) -> Tuple[int, int]:
        raise NotImplementedError()

    def get_drop_sub_pattern(self) -> Optional[Tuple[bytes, bytes]]:
        return None


class PygmentsLineByLineLanguage(PygmentsLanguage):
    line_by_line = True
    """
    Base class for Line by line pygments languages.
    Any multi line tokens, e.g. comments have to be handled by
    subclassing and re-implementing the necessary parts of the interface.
    """
    def __init__(self, name: str = None):
        super().__init__(name=name)
        self._token_starts = self._context_tokens()
        self._token_ends = {
            v: k for v, k in
            self._token_starts.items()}
        self._token_list = list(self._token_starts)

    def token_from_index(self, index):
        return self._token_list[index]

    def index_from_token(self, token):
        return self._token_list.index(token)

    def end(self, start):
        return self._token_starts[start]

    def start(self, end):
        return self._token_ends[end]

    def is_start(self, token):
        return token in self._token_starts

    def start_prefix(self, start):
        return f'{start[1]}\n'

    def _context_tokens(self):
        """
        Returns
        -------
        dict(tuple(Token, str), tuple(Token, str))
            Return dict of line spanning start and end markers.
        """
        return {}


class PythonLanguage(PygmentsLineByLineLanguage):
    name = 'python'
    supports_indent = True

    def _context_tokens(self):
        double_multiline = (
            _pygments().token.Token.Literal.String.Double, '"""')
        single_multiline = (
            _pygments().token.Token.Literal.String.Single, "'''")
        return {
            double_multiline: double_multiline,
            single_multiline: single_multiline,
        }

    def start_prefix(self, start):
        return f'_={start[1]}\n'

    def get_indent(self, text: str) -> int:
        return code_edit.get_default_indent()

    def get_newline_indent(self, text: str, pos: Tuple[int, int]
                           ) -> Tuple[int, int]:
        return code_edit.get_newline_indent(text, pos)

    def get_drop_sub_pattern(self) -> Tuple[bytes, bytes]:
        return b'\t', b' ' * code_edit.get_default_indent()


class JsonLanguage(PygmentsLineByLineLanguage):
    name = 'json'

    def get_tokens(self, text):
        # Pygments return KeyWord.Constant for some tokens that are not
        # supported by the json module. These are replaced by error tokens.
        constant = _pygments().token.Token.Keyword.Constant
        error = _pygments().token.Token.Error
        res = []
        for token_start, token_type, value in super().get_tokens(text):
            if token_type == constant and value not in (
                    'true', 'false', 'null'):
                token_type = error
            res.append((token_start, token_type, value))
        return res


class TokenIndexUserData(QtGui.QTextBlockUserData):
    def __init__(self, index):
        super().__init__()
        self._index = index

    @property
    def index(self):
        return self._index


class PygmentsHighlighter(QtGui.QSyntaxHighlighter):
    """
    Basic Pygments Highlighter, will lex the file after every change.
    """
    def __init__(self, text_edit_widget, language: PygmentsLanguage):
        super().__init__(text_edit_widget.document())
        style = settings.get_code_editor_theme()
        self._language = language
        self._style, self._highlighting = language.get_style(style)
        self._tokens = None

        # Set background color from style
        palette = text_edit_widget.palette()
        palette.setColor(
            QtGui.QPalette.Base, QtGui.QColor(self._style.background_color))
        text_edit_widget.setPalette(palette)

    def _qt_format_for_token(self, token):
        styles = self._style.style_for_token(token)
        f = QtGui.QTextCharFormat()
        if styles['color'] is not None:
            f.setForeground(QtGui.QBrush(QtGui.QColor(
                '#' + styles['color'])))
        if styles['bgcolor'] is not None:
            f.setBackground(QtGui.QBrush(QtGui.QColor(
                '#' + styles['bgcolor'])))
        if styles['bold']:
            f.setFontWeight(QtGui.QFont.Bold)
        if styles['italic']:
            f.setFontItalic(True)
        return f

    def text_changed(self):
        self.rehighlight()

    def _parse_document(self):
        text = self.document().toPlainText()
        self._tokens = self._language.get_tokens(text)

    def rehighlight(self):
        # Prevent highlighting calling itself
        if self._highlighting:
            return
        try:
            self._highlighting = True
            self._parse_document()
            return super().rehighlight()
        finally:
            self._highlighting = False

    def rehighlightBlock(self, block):
        return self.rehighlight()

    def highlightBlock(self, text):
        if self._tokens is None:
            self._parse_document()

        current_block = self.currentBlock()
        block_start = self.previousBlockState() + 1
        block_end = block_start + len(text)
        previous_block = current_block.previous()
        token_index = 0

        if previous_block:
            user_data = previous_block.userData()
            if user_data:
                token_index = user_data.index

        for i in range(token_index, len(self._tokens)):
            token_start, token_type, value = self._tokens[i]
            if token_start > block_end:
                break

            # Constrain token to block limits
            token_start = max(token_start, block_start)
            token_end = min(token_start + len(value), block_end)
            token_length = token_end - token_start

            # Skip tokens that are completely outside of this block
            if token_length <= 0:
                continue

            self.setFormat(token_start - block_start, token_length,
                           self._qt_format_for_token(token_type))
            token_index = i

        # Adding one for the inevitable trailing newline character
        self.setCurrentBlockState(self.previousBlockState() + len(text) + 1)
        current_block.setUserData(TokenIndexUserData(token_index))


class PygmentsLineByLineHighlighter(PygmentsHighlighter):
    """
    Line by line Pygments Highlighter.
    Lexes one row at a time and tries to avoid unnecessary re-processing
    for improved editing performance.
    """
    def __init__(self, text_edit_widget, language: PygmentsLineByLineLanguage):
        super().__init__(text_edit_widget, language)

    def text_changed(self):
        # Rehighlight is not needed in the line-by-line case.
        pass

    def rehighlightBlock(self, block):
        return super(PygmentsHighlighter, self).rehighlightBlock(block)

    def highlightBlock(self, text):
        # BlockState:
        #  n == -1: Not set
        #  n ==  0: No outgoing context
        #  n  >  1: token_from_index(n - 1)
        prev_state = self.previousBlockState()
        context_start = None
        context_end = None
        prefix = 0

        if prev_state > 0:
            context_start = self._language.token_from_index(prev_state - 1)
            context_end = self._language.end(context_start)
            prefix_text = self._language.start_prefix(context_start)
            text = f'{prefix_text}{text}'
            prefix = len(prefix_text)

        tokens = self._language.get_tokens(text)

        for token_start, token_type, value in tokens:
            token_start -= prefix
            token_end = token_start + len(value)

            if token_end >= 0:
                context_key = (token_type, value)

                if context_start:
                    if context_key == context_end:
                        context_start = None
                        context_end = None
                    else:
                        token_type = context_start[0]
                elif self._language.is_start(context_key):
                    context_start = context_key
                    context_end = self._language.end(context_key)

                self.setFormat(token_start, len(value),
                               self._qt_format_for_token(token_type))

        if context_start:
            self.setCurrentBlockState(
                self._language.index_from_token(context_start) + 1)
        else:
            self.setCurrentBlockState(0)


def _pygments_language_factory(language_name):
    line_by_line_languages = {x.name: x for x in [
        PythonLanguage, JsonLanguage]}
    language_cls = line_by_line_languages.get(language_name)
    if not language_cls:
        language = PygmentsLanguage(language_name)
    else:
        language = language_cls()
    return language


def _pygments_highlighter_factory(text_edit_widget, language):
    if language.line_by_line:
        res = PygmentsLineByLineHighlighter(
            text_edit_widget, language)
    else:
        res = PygmentsHighlighter(text_edit_widget, language)
    return res


def pygments_highlighter_factory(text_edit_widget, language_name):
    return _pygments_highlighter_factory(
        text_edit_widget, _pygments_language_factory(
            language_name))


class BaseLineCodeEdit(CodeEditMixin, BaseLineTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ValidationError(Exception):
    pass


class ValidatedLineEditBase(QtWidgets.QLineEdit):
    """Abstract base class for validated Line edit widgets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tooltip = ''
        self._validation_tooltip = ''
        self._builder = None
        self._base_builder = None
        self.textChanged.connect(self._handleTextChanged)
        self._value = None
        self._valid = False
        self._keep_last_valid_value = True

    def setBuilder(self, builder):
        """
        Parameters
        ----------
        builder : Callable[[int], Any]
            Builder builds typed value from string line and performs
            validation. Can raise ValidationError to indicate invalid input.
        """
        self._builder = builder

    def setToolTip(self, tooltip):
        self._tooltip = tooltip
        self._update_tooltip()

    def toolTip(self):
        return self._tooltip

    def _update_tooltip(self):
        tooltip = "\n\n".join(
            filter(bool, [self._tooltip, self._validation_tooltip]))
        super().setToolTip(tooltip)

    def _build(self, text):
        value = self._base_builder(text)
        if self._builder is not None:
            value = self._builder(value)
        return value

    def _handleTextChanged(self, text):
        tooltip = ''
        valid = False
        try:
            value = self._build(text)
            if value != self._value:
                self._value = value
                self.valueChanged.emit(value)
            valid = True
        except ValidationError as v:
            if self._keep_last_valid_value:
                tooltip = f'Error: {v}\nValue: {self._value}'
            else:
                tooltip = f'Error: {v}'

        except Exception:
            pass
        self._validation_tooltip = tooltip
        self._update_tooltip()
        palette = self.palette()
        if valid:
            palette = QtGui.QPalette()
        else:
            if prim.is_osx():
                # Special-case handling for MacOS.
                # For some reason, changing the background color of LineEdits
                # does not work. See:
                # https://bugreports.qt.io/browse/QTBUG-73183
                # https://bugreports.qt.io/browse/QTBUG-72662
                # https://bugreports.qt.io/browse/QTBUG-72428
                palette.setColor(
                    self.foregroundRole(), colors.DANGER_TEXT_NORMAL_BG_COLOR)
            else:
                palette.setColor(
                    self.foregroundRole(), colors.DANGER_TEXT_COLOR)
                palette.setColor(self.backgroundRole(), colors.DANGER_BG_COLOR)

        self.setPalette(palette)
        self._valid = valid

    def value(self):
        """
        Returns
        -------
        Any
            The stored value. Converted by applying builders on the text.
            Not necessarily the same as what is currently shown in the text
            box.
        """
        return self._value

    def valid(self):
        return self._valid

    def set_keep_last_valid_value(self, enabled):
        self._keep_last_valid_value = enabled


class ValidatedIntLineEdit(ValidatedLineEditBase):
    """Signal valueChanged is emitted when the stored value is changed."""
    valueChanged = qt_compat2.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_builder = self._valid_int_builder

    def _valid_int_builder(self, text):
        try:
            return int(text)
        except Exception:
            raise ValidationError(
                '"{}" is not a valid int value.'.format(text))


class ValidatedFloatLineEdit(ValidatedLineEditBase):
    """Signal valueChanged is emitted when the stored value is changed."""
    valueChanged = qt_compat2.Signal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_builder = self._valid_float_builder

    def _valid_float_builder(self, text):
        try:
            return float(text)
        except Exception:
            raise ValidationError(
                '"{}" is not a valid floating point value.'.format(text))


class ValidatedTextLineEdit(ValidatedLineEditBase):
    """Signal valueChanged is emitted when the stored value is changed."""
    valueChanged = qt_compat2.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_builder = self._valid_text_builder

    def _valid_text_builder(self, text):
        try:
            return str(text)
        except Exception:
            raise ValidationError(
                '"{}" is not a valid text value.'.format(text))


class ValidatedSpinBoxBase(QtWidgets.QAbstractSpinBox):
    """Signal valueChanged is emitted when the stored value is changed."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max = None
        self._min = None
        self._step = 1
        self._value = None

    def sizeHint(self):
        res = super().sizeHint()
        line_edit = self.lineEdit()
        if line_edit:
            res = res.expandedTo(line_edit.sizeHint())
        return res

    def _init_line_validator(self):
        def bounded_validator(value):
            if self._max is not None and value > self._max:
                raise ValidationError(
                    '"{}" is greater than upper bound: "{}".'.format(
                        value, self._max))

            if self._min is not None and value < self._min:
                raise ValidationError(
                    '"{}" is smaller than lower bound: "{}".'.format(
                        value, self._min))
            return value

        self.lineEdit().setBuilder(bounded_validator)

    def setLineEdit(self, line_edit):
        super().setLineEdit(line_edit)
        line_edit.valueChanged.connect(self._handleValueChanged)
        self._init_line_validator()

    def setMaximum(self, value):
        self._max = value

    def setMinimum(self, value):
        self._min = value

    def setSingleStep(self, value):
        self._step = value

    def setValue(self, value):
        if self._max is not None and value > self._max:
            value = self._max
        if self._min is not None and value < self._min:
            value = self._min

        line_edit = self.lineEdit()
        line_edit.setText(str(value))

    def value(self):
        return self._value

    def stepEnabled(self):
        state = QtWidgets.QAbstractSpinBox.StepNone
        if self._value is not None:
            if self._max is None or self._value < self._max:
                state |= QtWidgets.QAbstractSpinBox.StepUpEnabled
            if self._min is None or self._value > self._min:
                state |= QtWidgets.QAbstractSpinBox.StepDownEnabled
        return state

    def stepBy(self, steps):
        self.setValue(self._value + steps * self._step)

    def _handleValueChanged(self, value):
        self._value = value
        self.valueChanged.emit(value)


class ValidatedFloatSpinBox(ValidatedSpinBoxBase):
    valueChanged = qt_compat2.Signal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._decimals = None
        line_edit = ValidatedFloatLineEdit(parent=self)
        super().setLineEdit(line_edit)

    def setValue(self, value):
        if self._decimals is not None:
            value = float(round(value, self._decimals))
        super().setValue(value)

    def setMaximum(self, value):
        if value is None:
            self._max = None
        else:
            self._max = float(value)

    def setMinimum(self, value):
        if value is None:
            self._min = None
        else:
            self._min = float(value)

    def setDecimals(self, value):
        self._decimals = value


class ValidatedIntSpinBox(ValidatedSpinBoxBase):
    valueChanged = qt_compat2.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        line_edit = ValidatedIntLineEdit(parent=self)
        super().setLineEdit(line_edit)

    def setValue(self, value):
        super().setValue(value)


class ValidatedComboBoxBase(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max = None
        self._min = None
        self._value = None
        self.currentIndexChanged[int].connect(self._handleIndexChanged)
        self.setEditable(True)

    def _init_line_validator(self):
        def bounded_validator(value):
            if self._max is not None and value > self._max:
                raise ValidationError(
                    '"{}" is greater than upper bound: "{}".'.format(
                        value, self._max))

            if self._min is not None and value < self._min:
                raise ValidationError(
                    '"{}" is smaller than lower bound: "{}".'.format(
                        value, self._min))
            return value

        self.lineEdit().setBuilder(bounded_validator)

    def setLineEdit(self, line_edit):
        super().setLineEdit(line_edit)
        line_edit.valueChanged.connect(self._handleValueChanged)
        self._init_line_validator()

    def setMaximum(self, value):
        self._max = value

    def setMinimum(self, value):
        self._min = value

    def setValue(self, value):
        if self._max is not None and value > self._max:
            value = self._max
        if self._min is not None and value < self._min:
            value = self._min

        line_edit = self.lineEdit()
        line_edit.setText(str(value))

    def sizeHint(self):
        res = super().sizeHint()
        line_edit = self.lineEdit()
        if line_edit:
            res = res.expandedTo(line_edit.sizeHint())
        return res

    def value(self):
        return self._value

    def _handleValueChanged(self, value):
        self._value = value
        self.valueChanged.emit(value)

    def _handleIndexChanged(self, index):
        line_edit = self.lineEdit()
        text = line_edit.text()
        line_edit.setText(text)


class ValidatedTextComboBox(ValidatedComboBoxBase):
    valueChanged = qt_compat2.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        line_edit = ValidatedTextLineEdit(parent=self)
        super().setLineEdit(line_edit)


class ValidatedFloatComboBox(ValidatedComboBoxBase):
    valueChanged = qt_compat2.Signal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._decimals = None
        line_edit = ValidatedFloatLineEdit(parent=self)
        super().setLineEdit(line_edit)

    def setValue(self, value):
        if self._decimals is not None:
            value = round(value, self._decimals)
        super().setValue(value)

    def setDecimals(self, value):
        self._decimals = value


class ValidatedIntComboBox(ValidatedComboBoxBase):
    valueChanged = qt_compat2.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        line_edit = ValidatedIntLineEdit(parent=self)
        super().setLineEdit(line_edit)

    def setValue(self, value):
        super().setValue(value)


class NonEditableComboBox(QtWidgets.QComboBox):
    valueChanged = qt_compat2.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEditable(False)
        self.currentIndexChanged[int].connect(self._handleIndexChanged)

    def value(self):
        return self.currentText()

    def _handleIndexChanged(self, index):
        self.valueChanged.emit(self.value())


class DateTimeWidget(QtWidgets.QDateTimeEdit):
    valueChanged = qt_compat2.Signal(datetime.datetime)
    datetime_format = "yyyy-MM-ddTHH:mm:ss"

    def __init__(self, value=None, datetime_format=None, parent=None):
        super().__init__(parent=parent)
        if datetime_format:
            self.datetime_format = datetime_format

        self.setDisplayFormat(self.datetime_format)
        self.setCalendarPopup(True)
        if value is not None:
            self.setValue(value)
        self.dateTimeChanged.connect(self._datetime_changed)

    def value(self):
        qdatetime = self.dateTime()
        return prim.parse_isoformat_datetime(
            qdatetime.toString(QtCore.Qt.ISODateWithMs))

    def setValue(self, value):
        qdatetime = QtCore.QDateTime.fromString(
            value.isoformat(), QtCore.Qt.ISODateWithMs)
        self.setDateTime(qdatetime)

    def _datetime_changed(self, value):
        value = prim.parse_isoformat_datetime(
            value.toString(QtCore.Qt.ISODateWithMs))
        self.valueChanged.emit(value)


# leave for debugging widgets
if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()

    test_widget = ToggleablePrefixLineEdit(placeholder='enter filename',
                                           prefix_states=('rel', 'abs'),
                                           parent=widget)
    # test_widget.textChanged.connect(lambda a: test_widget.set_state(a == ''))

    other_widget = ClearButtonLineEdit(parent=widget)

    normal_widget = QtWidgets.QLineEdit(widget)

    layout.addWidget(test_widget)
    layout.addWidget(other_widget)
    layout.addWidget(normal_widget)

    widget.setLayout(layout)
    widget.show()
    widget.raise_()

    # print(test_widget.rect().height())
    # print(other_widget.rect().height())
    # print(normal_widget.rect().height())

    sys.exit(application.exec_())


class UndoStack(QtCore.QObject):
    """
    A simple undo stack which saves a list of states and allows moving
    between those states.

    The signal state_changed is emitted every time the current state of the
    undo stack changes.
    """
    state_changed = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._undo_stack = []
        self._undo_index = 0

        self._undo_action = QtGui.QAction(
            QtGui.QIcon(prim.get_icon_path('actions/edit-undo-symbolic.svg')),
            'Undo')
        self._undo_action.setShortcut(QtGui.QKeySequence.Undo)
        self._undo_action.setToolTip('Undo')
        self._undo_action.triggered.connect(self._undo)

        self._redo_action = QtGui.QAction(
            QtGui.QIcon(prim.get_icon_path('actions/edit-redo-symbolic.svg')),
            'Redo')
        self._redo_action.setShortcut(QtGui.QKeySequence.Redo)
        self._redo_action.setToolTip('Redo')
        self._redo_action.triggered.connect(self._redo)

    @property
    def undo_action(self):
        """
        Return a QAction for undo which can be used in menus and toolbars.

        The QAction is automatically enabled/disabled as needed.
        """
        return self._undo_action

    @property
    def redo_action(self):
        """
        Return a QAction for redo which can be used in menus and toolbars.

        The QAction is automatically enabled/disabled as needed.
        """
        return self._redo_action

    def add_undo_state(self, new_state):
        """
        Store a new state on the undo stack.

        If the new state is equal to the current state, the new state is
        ignored and the undo stack isn't modified. Otherwise any states ahead
        of the current state are discarded and new_state becomes the new
        current state.

        This method does not emit state_changed. The reasoning behind this is
        that this method is usually called after the model has already been
        updated, so we don't want to trigger another update of the model.

        Returns True if the new state was added and False otherwise.
        """
        if not isinstance(new_state, str):
            raise TypeError(f"Undo state must be str not {type(new_state)}")
        if (not len(self._undo_stack)
                or new_state != self._undo_stack[self._undo_index]):
            self._undo_stack = self._undo_stack[:self._undo_index + 1]
            self._undo_stack.append(new_state)
            self._undo_index = len(self._undo_stack) - 1
            self._update_enabled_undo_redo_actions()
            return True
        return False

    def _undo(self):
        """Move the undo stack pointer back one step."""
        if self.can_undo():
            self._undo_index -= 1
            self._update_enabled_undo_redo_actions()
            self.state_changed.emit(self._undo_stack[self._undo_index])

    def _redo(self):
        """Move the undo stack pointer forward one step."""
        if self.can_redo():
            self._undo_index += 1
            self._update_enabled_undo_redo_actions()
            self.state_changed.emit(self._undo_stack[self._undo_index])

    def can_undo(self):
        """Return True if is currently possible to undo."""
        return self._undo_index > 0

    def can_redo(self):
        """Return True if is currently possible to redo."""
        return self._undo_index + 1 < len(self._undo_stack)

    def _update_enabled_undo_redo_actions(self):
        """Set the appropriate enabled state for the undo/redo buttons."""
        self._undo_action.setEnabled(self.can_undo())
        self._redo_action.setEnabled(self.can_redo())


class HLine(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(self.HLine)
        self.setFrameShadow(self.Sunken)


class VLine(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(self.VLine)
        self.setFrameShadow(self.Sunken)


class FormLayout(QtWidgets.QFormLayout):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Override the default platform depended sizing and alignment rules,
        # to get a Sympathy specific layout
        self.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)


class ReadOnlyLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setReadOnly(True)
        palette = self.palette()
        palette.setColor(
            self.foregroundRole(), palette.color(
                palette.Disabled, self.foregroundRole()))
        self.setPalette(palette)
        self.setFocusPolicy(QtCore.Qt.NoFocus)


class ClickableHtmlLabel(QtWidgets.QLabel):
    """
    HTML label with clickable links with can be handled.
    Connect linkActivated(string) to handle clicks.
    WordWrap is enabled by default.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setTextFormat(QtCore.Qt.RichText)
        self.setWordWrap(True)
        self.setOpenExternalLinks(False)


class HtmlTreeView(QtWidgets.QTreeView):
    """
    TreeView capable of displaying HTML text.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Workaround, primarily for Windows. If highlightedText is opaque we
        # assume that it is not used. This also relates to why transparent
        # backgrounds are used in stylesheets.
        highlight_opaque = self.palette().highlightedText().isOpaque()
        self._highlight_role = QtGui.QPalette.HighlightedText
        if highlight_opaque:
            self._highlight_role = QtGui.QPalette.Text
        highlighter = item_delegates.HtmlItemDelegate(
            highlight_role=self._highlight_role, parent=self)
        self.setItemDelegate(highlighter)
