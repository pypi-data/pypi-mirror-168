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
import tokenize
from collections import deque
from io import BytesIO
from typing import Tuple, List, Optional
from token import (
    INDENT,
    DEDENT,
    OP,
    NAME,
    NL,
)

_open_op = '([{'
_close_op = ')]}'
_indent_columns = 4


def _get_tokens(text):
    return tokenize.tokenize(BytesIO(text.encode('utf8')).readline)


def _get_indent_info(text, pos):
    def indent_tokens(tokens):
        try:
            for t in tokens:
                yield t
        except Exception:
            # Will fail if ending is incomplete, etc.
            pass
    tokens = _get_tokens(text)
    stack = deque()
    pos_row, pos_col = pos
    pos_row += 1
    next_token = None

    for t in indent_tokens(tokens):
        next_token = t
        t_end_row, t_end_col = t.end
        t_start_row, t_start_col = t.start

        if pos_row > t_end_row:
            stack.append(t)
        elif pos_row == t_end_row and pos_col >= t_end_col:
            if len(t.string) or t.line:
                stack.append(t)
        else:
            break

        if pos_row < t_start_row or (
                pos_row == t_start_row and pos_col <= t_start_col):
            break
    return stack, next_token


def _safe_pop(deque):
    try:
        return deque.pop()
    except IndexError:
        pass


class TokenParse:
    """
    Simple parse of a limited set of token types.

    Collects tokens required to determine the indentation level after the last
    token in `stack`.  Closed OPs, and dedented indentation levels are removed
    from `self.ops` and `self.indents`.
    """

    def __init__(self, stack):
        indent = deque()
        ops = deque()
        keywords = deque()
        last_t = None
        last_keyword = None

        for t in stack:
            token_type = t.type
            if token_type == INDENT:
                indent.append(t)
            elif token_type == DEDENT:
                _safe_pop(indent)
            elif token_type == OP:
                token_string = t.string
                if token_string in _open_op:
                    ops.append([t])
                elif token_string in _close_op:
                    _safe_pop(ops)
                elif not ops and token_string == ':':
                    last_keyword = _safe_pop(keywords)
            elif token_type == NAME:
                token_string = t.string
                if token_string in (
                        'class',
                        'def',
                        'else',
                        'except',
                        'finally',
                        'for',
                        'if',
                        'try',
                        'while',
                        'with',
                ):
                    if not t.line[:_start_col(t)].strip():
                        keywords.append(t)
                elif _is_lambda(t):
                    keywords.append(t)

            last_t = t

        self._indents = list(indent)
        self._ops = list(ops)
        self.last_token = last_t
        self.last_keyword = last_keyword

    @property
    def op_groups(self):
        """
        Return list of list of OP tokens in effect at the end of
        the token stack, used to build the object.

        Each sub list starts with an opening OP and can contain
        multiple `,` OPs and even NL tokens (not an OP) that are
        contained within the opening OP context.
        """
        return self._ops

    @property
    def indents(self):
        """
        Return list indentation tokens in effect at the end of
        the token stack.
        """
        return self._indents


def _start_col(token):
    return token.start[1]


def _end_col(token):
    return token.end[1]


def _end_row(token):
    return token.end[0]


def _leading_space(token):
    line = token.line
    return len(line) - len(line.lstrip(' '))


def _same_line(token1, token2):
    return token1.start[0] == token2.start[0]


def _is_open(op):
    return op.type == OP and op.string in _open_op


def _is_close(op):
    return op.type == OP and op.string in _close_op


def _is_colon(op):
    return op.type == OP and op.string == ':'


def _is_lambda(name):
    return name.type == NAME and name.string == 'lambda'


def _level_indent(levels, indent):
    return max(0, levels) * indent


def _should_indent_after_colon_op(op, last_keyword):
    return _is_colon(op) and last_keyword and not _is_lambda(last_keyword)


def _get_indent_col(stack, next_token, pos):
    indent_columns = _indent_columns
    indent_column = 0
    indent_column_after = None
    token_parse = TokenParse(stack)
    indents = token_parse.indents
    op_groups = token_parse.op_groups
    last_token = token_parse.last_token
    last_keyword = token_parse.last_keyword

    if indents:
        indent_column = _end_col(indents[-1])

    open_levels = 0
    last_op_group = None
    last_open = None

    for op_group in op_groups:
        last_op_group = op_group
        last_open = last_op_group[0]
        open_levels += 1

    if not last_token:
        pass

    elif last_op_group:
        # Inside at least one unfinished context.
        indent_column = _leading_space(last_token)
        if _is_open(last_token):
            if next_token and _is_close(next_token) and _same_line(
                    last_token, next_token):
                # {|}, (|), [|]
                # => set indent after with one less level.
                # Reduce one indent for the close marker.
                indent_column_after = indent_column

            # After open level. Indent to indent_column.
            indent_column += _level_indent(1, indent_columns)
        else:
            if last_token.type == NL:
                indent_column = pos[1]
            elif _same_line(last_open, last_token):
                indent_column = _end_col(last_open)
            else:
                indent_column = _leading_space(last_token)

    elif _should_indent_after_colon_op(last_token, last_keyword):
        # Entering a new block.
        indent_column = _leading_space(last_keyword) + indent_columns

    return indent_column, indent_column_after


def get_newline_indent(text: str, pos: Tuple[int, int]
                       ) -> Tuple[int, Optional[int]]:
    """
    Return the indentation column for a new opened line after pos and
    an optional value for indenting the following line used if the next
    token after pos is a closing OP, like `)`.
    """
    return _get_indent_col(*_get_indent_info(text, pos), pos)


def get_indents(text: str) -> List[int]:
    """
    Return all distinct indentation levels (columns) used in text.
    """
    indents = {}
    for t in _get_tokens(text):
        if t.type == INDENT:
            indents[t.end[1]] = None
    if not indents:
        indents[_indent_columns] = None

    return list(indents.keys())


def get_default_indent() -> int:
    """
    Return the default indentation.
    """
    return _indent_columns
