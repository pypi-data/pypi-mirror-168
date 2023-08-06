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
import sys
import re
import html

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from sympathy.utils import prim
from .. import util
from .. import flow
from .. import themes
from . import issues
from .. import settings
from .. interfaces.messages_window import MessageItemRoles as Roles
from .. interfaces.messages_window import DetailsWidget
from .. interfaces.messages_window import Store
from .. credentials import credentials


import sympathy.app.library


class MessageListItem(QtWidgets.QListWidgetItem):
    _colors = None
    _icons = None

    @classmethod
    def icon(cls, level):
        if cls._icons is None:
            theme = themes.get_active_theme()
            cls._icon = {
                util.Levels.exception: theme.exception_msg,
                util.Levels.error: theme.error_msg,
                util.Levels.warning: theme.warning_msg,
                util.Levels.notice: theme.notice_msg,
            }
        return cls._icon[level]

    @classmethod
    def color(cls, level):
        if cls._colors is None:
            theme = themes.get_active_theme()
            cls._colors = {
                util.Levels.exception: theme.exception_msg_color,
                util.Levels.error: theme.error_msg_color,
                util.Levels.warning: theme.warning_msg_color,
                util.Levels.notice: theme.notice_msg_color,
            }
        return cls._colors[level]

    def __init__(self, message):
        def _cleanup(s: str):
            return s.replace('\n', ' ').replace('\r', ' ').replace(
                '\t', ' ').strip()

        def _root_flow_uuid(flode):
            if flode is None:
                return None
            root_flow = flode.root_flow()
            if root_flow is None:
                return None
            return root_flow.namespace_uuid()

        def _full_uuid(flode):
            if flode is None:
                return None
            return flode.full_uuid

        super().__init__()
        self._title = _cleanup(message.title())
        level = message.level()
        time = message.time().strftime("%Y-%m-%d %H:%M:%S")
        level_name = level.name.capitalize()
        tooltip = f'{level_name} message from node "{self._title}"\n{time}'
        root_uuid = _root_flow_uuid(message.node())
        full_uuid = _full_uuid(message.node())

        self.setIcon(QtGui.QIcon(self.icon(level)))
        self.setForeground(QtGui.QBrush(self.color(level)))
        self.setData(QtCore.Qt.ToolTipRole, tooltip)
        self.setData(Roles.message, message)
        self.setData(Roles.root_uuid, root_uuid)
        self.setData(Roles.full_uuid, full_uuid)
        self.setData(Roles.store, Store([]))

    def data(self, role: int):
        if role == QtCore.Qt.DisplayRole:
            if self.data(Roles.archived):
                return f"{self._title} [Archived]"
            return self._title

        return super().data(role)


class MessageList(QtWidgets.QListWidget):
    """Lists errors and output"""

    goto_node_requested = QtCore.Signal(flow.Node)
    cleared = QtCore.Signal()

    def __init__(self, app_core, font, parent=None):
        super().__init__(parent)
        self._item_by_id = {}
        self._app_core = app_core
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self._font = font
        self._context_menu = QtWidgets.QMenu(parent=self)
        self._goto_selected_action = QtGui.QAction('Go to Node', self)

        self._root_uuid = None
        self._show_archived = False
        self._show_level = {
            util.Levels.exception: True,
            util.Levels.error: True,
            util.Levels.warning: True,
            util.Levels.notice: True,
        }

        theme = themes.get_active_theme()
        archive_icon = QtGui.QIcon(theme.archive)
        delete_icon = QtGui.QIcon(theme.delete)
        show_archived_icon = QtGui.QIcon(theme.show_archived)
        self.show_archived_action = QtGui.QAction(
            show_archived_icon, 'Show archived', self)
        self.show_archived_action.setToolTip('Show archived messages')
        self.show_archived_action.setCheckable(True)
        self.show_archived_action.triggered.connect(self.set_show_archived)

        self._report_issue_action = QtGui.QAction(
            QtGui.QIcon(theme.report_issue), 'Report Issue', self)
        self._goto_selected_action.triggered.connect(self._handle_goto_node)
        self._report_issue_action.triggered.connect(self._handle_report_issue)
        self._context_menu.addAction(self._goto_selected_action)

        self._archive_selected_action = QtGui.QAction(
            archive_icon, 'Archive selected', self)
        self._archive_selected_action.triggered.connect(self.archive_selected)
        self._context_menu.addAction(self._archive_selected_action)
        self.archive_all_action = QtGui.QAction(
            archive_icon, 'Archive all messages', self)
        self.archive_all_action.setToolTip('Archive all current messages')
        self.archive_all_action.triggered.connect(self.archive_all)
        self._context_menu.addAction(self.archive_all_action)
        self._remove_selected_action = QtGui.QAction(
            delete_icon, 'Remove selected', self)
        self._remove_selected_action.triggered.connect(self._remove_selected)
        self._context_menu.addAction(self._remove_selected_action)
        self._context_menu.addSeparator()
        self._context_menu.addAction(self._report_issue_action)

        self.setIconSize(QtCore.QSize(16, 16))
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        policy = self.sizePolicy()
        policy.setHorizontalPolicy(policy.Minimum)
        self.setSizePolicy(policy)

        self._goto_selected_action.triggered.connect(self._handle_goto_node)

    def _selected_node_items(self):
        selected_items = self.selectedItems()
        res = []
        for item in selected_items:
            node = item.data(Roles.message).node()
            if node:
                if flow.Type.is_port(node):
                    node = node.node
                else:
                    res.append(node)
        return res

    def _handle_goto_node(self):
        for node in self._selected_node_items():
            self.goto_node_requested.emit(node)

    def _anonymize_traceback(self, string):
        """
        Attempt to cleanup identifying traceback information in File
        paths.
        """
        lines = []
        for line in string.splitlines():
            match = re.match('^(.*)File "([^"]*)"(.*)$', line)
            if match:
                prefix, file_, suffix = match.groups()
                replaced = False
                for name, path in [
                        ('sympathy', prim.sympathy_path()),
                        ('sylib', prim.sylib_path()),
                        ('python_prefix', sys.prefix),
                        ('python_exec_prefix', sys.exec_prefix)]:

                    if file_.startswith(path):
                        file_ = file_.replace(path, name, 1)
                        replaced = True
                        break
                if replaced:
                    lines.append(f'{prefix}File "{file_}"{suffix}')
                else:
                    lines.append(f'{prefix}File "omitted"{suffix}')
            else:
                lines.append(line)
        return '\n'.join(lines)

    def _handle_report_issue(self):

        selected_items = self.selectedItems()
        for item in selected_items:
            message = item.data(Roles.message)
            node = message.node()
            level = message.level()
            description = _message_text(message)
            generated = True

            if _can_show_trace(message):
                # Attempt to cleanup identifying traceback information.
                trace = self._anonymize_traceback(message.trace())
                description = _join(description, trace)

            level_name = level.name.lower() if level else 'behavior'

            subject = 'Unexpected {level} in {node} node'.format(
                level=level_name,
                node=node.library_node_name)
            dialog = issues.IssueReportSender(
                subject=subject, details=description, generated=generated)

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                pass

    def archive_all(self):
        """Archive all currently visible items"""
        for item in self._item_by_id.values():
            if not item.isHidden():
                self._archive_item(item)
        if not self.show_archived_action.isChecked():
            self.cleared.emit()
        self._purge_archived()

    def _archive_item(self, item):
        item.setData(Roles.archived, True)
        self._update_filter_for_item(item)

    def _unarchive_item(self, item):
        item.setData(Roles.archived, False)
        self._update_filter_for_item(item)

    def archive_selected(self):
        for item in reversed(self.selectedItems()):
            self._archive_item(item)
        self._purge_archived()

    def archive_node_messages(self, full_uuid):
        """Archive all messages related to a certain node."""
        for row in reversed(range(self.count())):
            item = self.item(row)
            message = item.data(Roles.message)
            if (message.archive_with_node() and
                    item.data(Roles.full_uuid) == full_uuid):
                self._archive_item(item)
        self._purge_archived()

    def _remove_selected(self):
        for item in reversed(self.selectedItems()):
            if item is self.currentItem():
                self.setCurrentItem(None)
            message = item.data(Roles.message)
            ident = message.id()
            self._item_by_id.pop(ident, None)
            row = self.indexFromItem(item).row()
            self.takeItem(row)

    def _purge_archived(self):
        """Purge old archived messages down to the allowed number."""
        max_archived = settings.instance()['Gui/max_archived_messages']
        if max_archived <= 0:
            return

        archived_count = 0
        for row in reversed(range(self.count())):
            item = self.item(row)
            if item.data(Roles.archived):
                archived_count += 1
                if archived_count > max_archived:
                    if item is self.currentItem():
                        self.setCurrentItem(None)
                    self.takeItem(row)

    @QtCore.Slot(util.DisplayMessage)
    def add_display_message(self, message: util.DisplayMessage):
        message_id = message.id()
        item = self._item_by_id.get(message_id)
        if not item:
            brief = message.brief()
            details = message.details()

            if not (brief or details):
                return None

            item = MessageListItem(message)
            self.addItem(item)
            self._item_by_id[message.id()] = item
            self.scrollToBottom()
            self.setCurrentItem(item)

        # If item already exists but now received more streamed content,
        # unarchive it:
        self._unarchive_item(item)

        return item

    def set_flow(self, flow_):
        if flow_ is None:
            self._root_uuid = None
        else:
            self._root_uuid = flow_.root_flow().namespace_uuid()
        self._update_filter()

    def set_show_archived(self, show_archived):
        self._show_archived = show_archived
        self._update_filter()

    def set_show_errors(self, show_errors):
        self._show_level[util.Levels.exception] = show_errors
        self._show_level[util.Levels.error] = show_errors
        self._update_filter()

    def set_show_warnings(self, show_warnings):
        self._show_level[util.Levels.warning] = show_warnings
        self._update_filter()

    def set_show_output(self, show_output):
        self._show_level[util.Levels.notice] = show_output
        self._update_filter()

    def _update_filter(self):
        for item in self._item_by_id.values():
            self._update_filter_for_item(item)

    def _update_filter_for_item(self, item):
        level = item.data(Roles.message).level()
        hide_archived = not self._show_archived and item.data(Roles.archived)
        hide_flow = item.data(Roles.root_uuid) not in (self._root_uuid, None)
        hide_level = not self._show_level[level]
        hide = hide_archived or hide_flow or hide_level
        item.setHidden(hide)
        if hide and item is self.currentItem():
            self.setCurrentItem(None)

    def contextMenuEvent(self, event):
        def node_exists(node):
            try:
                return self._app_core.get_node(node.full_uuid) is not None
            except Exception:
                return False

        enable_goto = False

        platform_node = False
        for node in self._selected_node_items():
            platform_node = sympathy.app.library.is_platform_node(
                node.library_node)
            enable_goto = node_exists(node)
        self._goto_selected_action.setEnabled(enable_goto)

        self._report_issue_action.setEnabled(platform_node)
        self._context_menu.exec_(event.globalPos())
        super().contextMenuEvent(event)


class DetailsView(QtWidgets.QWidget):

    def __init__(self, details_widgets, parent=None):
        super().__init__(parent=parent)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._stacked = QtWidgets.QStackedWidget()
        self._widgets = {w.type(): w for w in details_widgets}

        for widget in details_widgets:
            self._stacked.addWidget(widget)

        layout.addWidget(self._stacked)
        self.setLayout(layout)

    def add_display_message(self, item, message):
        current = self._stacked.currentWidget()
        widget = self._widgets[message.type()]
        widget.add_display_message(item, message)
        if not current:
            self._stacked.setCurrentWidget(widget)

    def set_item(self, item):
        current = self._stacked.currentWidget()
        message = item.data(Roles.message)
        widget = self._widgets[message.type()]
        widget.update_data(item)
        if widget is not current:
            self._stacked.setCurrentWidget(widget)

    def clear(self):
        self._stacked.setCurrentIndex(0)
        self._stacked.currentWidget().clear()


def _join(brief, details):
    return '\n\n'.join([brief, details])


def _message_text(message):
    res = ''
    brief = str(message.brief() or '')
    details = str(message.details() or '')
    if brief and details:
        res = _join(brief, details)
    elif brief:
        res = brief
    elif details:
        res = details
    return res


class TextMessageDetailsBase(DetailsWidget):

    def __init__(self, font, parent=None):
        super().__init__(parent=parent)
        self._font = font
        self.setFont(self._font)
        self._item = None
        self._view = QtWidgets.QTextBrowser()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        text_interaction_flags = (QtCore.Qt.TextSelectableByMouse |
                                  QtCore.Qt.TextSelectableByKeyboard |
                                  QtCore.Qt.LinksAccessibleByMouse |
                                  QtCore.Qt.LinksAccessibleByKeyboard)
        # TODO: Editable on Mac to workaround a Qt bug that otherwise results
        # in non-working keyboard shortcuts for Copy and Select all actions.
        if prim.is_osx():
            text_interaction_flags |= QtCore.Qt.TextEditable

        self._view.setTextInteractionFlags(text_interaction_flags)
        layout.addWidget(self._view)
        self.setLayout(layout)

    def _format_limit(self, max_chars):
        return (f'\n\nCharacter limit (Preferences -> Advanced): '
                f'{max_chars} reached.')

    def text(self, item):
        message = item.data(Roles.message)
        return _message_text(message)

    def _unsupported_text(self, e, text):
        return (f'Unsupported data, exception: {e}. '
                f'Printable representation:\n'
                f'{repr(text)}')

    def _set_view_text(self, item_text):
        try:
            self._view.setPlainText(item_text)
        except Exception as e:
            item_text = self._unsupported_text(e, item_text)
            self._view.setPlainText(item_text)
        return item_text

    def update_data(self, item):
        self._view.clear()
        item_text = self.text(item)
        item_text = self._set_view_text(item_text)
        item.setData(Roles.text, item_text)
        self._item = item

    def clear(self):
        super().clear()
        self._view.clear()


def _can_show_trace(message):
    level = message.level()
    return (
        (level == util.Levels.exception or
         settings.instance()['Gui/platform_developer']) and bool(
             message.trace()))


class TextMessageDetails(TextMessageDetailsBase):

    _type = 'text'

    _error_label = 'Error'
    _general_label = 'General'

    def __init__(self, font, parent=None):
        super().__init__(font, parent=parent)
        self._show_trace = False
        self._can_show_trace = False
        self._view.setOpenExternalLinks(False)
        self._view.setOpenLinks(False)
        self._view.anchorClicked.connect(self._handle_anchor_clicked)

    def text(self, item):
        res = super().text(item)
        res = html.escape(res)
        pre = 'style="white-space: pre"'
        if self._show_trace:
            message = item.data(Roles.message)
            trace = html.escape(str(message.trace()))
            res = (
                f'<p {pre}>{res}</p>'
                f'<p {pre}><i>{trace}</i></p>'
                f'Show <a href="#show-less">fewer details</a>.'
            )

        elif self._can_show_trace:
            res = (
                f'<p {pre}>{res}</p>'
                f'<p>Show <a href="#show-more">more details</a>.</p>'
            )
        else:
            res = f'<p {pre}>{res}</p>'
        return res

    def _set_view_text(self, item_text):
        try:
            self._view.setText(item_text)
        except Exception as e:
            item_text = self._unsupported_text(e, item_text)
            self._view.setText(item_text)
        return item_text

    def update_data(self, item):
        self._show_trace = False
        message = item.data(Roles.message)
        self._can_show_trace = _can_show_trace(message)
        super().update_data(item)

    def _handle_anchor_clicked(self, url):
        if self._item:
            url_string = url.toString()

            if url_string == '#show-less':
                self._show_trace = False

            elif url_string == '#show-more':
                self._show_trace = True
            self._set_view_text(self.text(self._item))


class StreamMessageDetails(TextMessageDetailsBase):
    _type = 'stream'

    def __init__(self, font, parent=None):
        super().__init__(font, parent=parent)
        self._id = None

    def text(self, item):
        store_data = item.data(Roles.store).data
        res = ''
        max_chars = settings.instance()['max_task_chars']
        if max_chars:
            length = item.data(Roles.length) or 0
            if length >= max_chars:
                store_data = list(store_data)
                store_data.append(self._format_limit(max_chars))

        if store_data:
            res = ''.join(store_data)
        return res

    def update_data(self, item):
        super().update_data(item)
        self._id = item.data(Roles.message).id()

    def add_display_message(self, item, message):
        data = message.brief()
        length = item.data(Roles.length) or 0
        max_chars = settings.instance()['max_task_chars']
        extra = ''

        if max_chars:
            if length < max_chars:
                if length + len(data) >= max_chars:
                    data = data[:max_chars - length]
                    extra = self._format_limit(max_chars)
            else:
                data = ''

        if data:
            length += len(data)
            store = item.data(Roles.store).data
            store.append(data)
            item.setData(Roles.length, length)

        if extra:
            data = data + extra

        if data and self._id is not None and self._id == message.id():
            vscrollbar = self._view.verticalScrollBar()
            vscroll = vscrollbar.value()
            textcursor = self._view.textCursor()
            cursor_start = textcursor.selectionStart()
            cursor_end = textcursor.selectionEnd()
            self._view.moveCursor(QtGui.QTextCursor.End)
            self._view.insertPlainText(data)
            textcursor = self._view.textCursor()
            textcursor.setPosition(cursor_start)
            textcursor.setPosition(cursor_end, QtGui.QTextCursor.KeepAnchor)
            self._view.setTextCursor(textcursor)
            vscrollbar.setValue(vscroll)

    def clear(self):
        super().clear()
        self._id = None
        self._view.clear()


class MessageView(QtWidgets.QWidget):
    """Shows the errors and outputs together with a toolbar."""

    goto_node_requested = QtCore.Signal(flow.Node)

    def __init__(self, app_core, parent=None):
        super().__init__(parent=parent)
        self._app_core = app_core
        self._init_gui()
        self._tasks = set()

    def _init_gui(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self._font = QtGui.QFont('Courier')

        self._message_list = MessageList(
            self._app_core, self._font)
        self._message_list.goto_node_requested.connect(
            self.goto_node_requested)
        self._text_message_details = TextMessageDetails(self._font)
        self._stream_message_details = StreamMessageDetails(self._font)
        details_widgets = [
            self._text_message_details, self._stream_message_details]
        details_widgets.extend([
            widget_cls(self._font)
            for widget_cls in credentials.details_widgets()])
        self._details_widget = details_widgets

        self._details_view = DetailsView(details_widgets)

        for widget in details_widgets:
            widget.requested_remove.connect(self._handle_requested_remove)

        self._message_list.itemSelectionChanged.connect(
            self._selected_items_changed)

        self._message_list.cleared.connect(self._items_cleared)

        theme = themes.get_active_theme()
        self._toolbar = QtWidgets.QToolBar(parent=self)
        self._toolbar.setOrientation(QtCore.Qt.Vertical)
        self._toolbar.setIconSize(QtCore.QSize(16, 16))
        self._toolbar.addAction(self._message_list.archive_all_action)
        self._toolbar.addSeparator()

        # Filters
        error_icon = QtGui.QIcon(theme.error_msg)
        warning_icon = QtGui.QIcon(theme.warning_msg)
        output_icon = QtGui.QIcon(theme.notice_msg)
        self._toolbar.addAction(self._message_list.show_archived_action)
        self.show_errors_action = QtGui.QAction(
            error_icon, 'Show errors', self)
        self.show_errors_action.setToolTip(
            'Show error and exception level messages')
        self.show_errors_action.setCheckable(True)
        self.show_errors_action.setChecked(True)
        self.show_errors_action.triggered.connect(
            self._message_list.set_show_errors)
        self._toolbar.addAction(self.show_errors_action)
        self.show_warnings_action = QtGui.QAction(
            warning_icon, 'Show warnings', self)
        self.show_warnings_action.setToolTip('Show warning level messages')
        self.show_warnings_action.setCheckable(True)
        self.show_warnings_action.setChecked(True)
        self.show_warnings_action.triggered.connect(
            self._message_list.set_show_warnings)
        self._toolbar.addAction(self.show_warnings_action)
        self.show_output_action = QtGui.QAction(
            output_icon, 'Show outputs', self)
        self.show_output_action.setToolTip('Show output level messages')
        self.show_output_action.setCheckable(True)
        self.show_output_action.setChecked(True)
        self.show_output_action.triggered.connect(
            self._message_list.set_show_output)
        self._toolbar.addAction(self.show_output_action)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self._message_list)
        splitter.addWidget(self._details_view)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(self._toolbar)
        layout.addWidget(splitter)
        self.setLayout(layout)

    @QtCore.Slot(flow.Flow)
    def set_flow(self, flow_):
        if flow_ is None:
            self._message_list.set_flow(flow_)
        else:
            self._message_list.set_flow(flow_.flow())

    @QtCore.Slot(util.DisplayMessage)
    def add_display_message(self, message):
        item = self._message_list.add_display_message(message)
        self._details_view.add_display_message(item, message)

    @QtCore.Slot(str, str)
    def add_message(self, title, text):
        self._message_list.add_display_message(
            util.DisplayMessage(title=title, brief=text))

    def _selected_items_changed(self):
        item = None
        for item in self._message_list.selectedItems():
            self._details_view.set_item(item)
        if item is None:
            self._details_view.clear()

    def _items_cleared(self):
        self._details_view.clear()

    def _handle_requested_remove(self, item):
        for item_ in list(self._message_list.selectedItems()):
            if item_ is item:
                self._message_list.archive_selected()
                break

    def clear_node_messages(self, full_uuid):
        self._message_list.archive_node_messages(full_uuid)
