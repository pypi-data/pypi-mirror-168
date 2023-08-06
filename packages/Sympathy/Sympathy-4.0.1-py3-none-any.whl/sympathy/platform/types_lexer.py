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
# flake8: noqa
# types_lexer.py. This file automatically created by PLY (version 3.11). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('ALIAS', 'ARROW', 'COLON', 'COMMA', 'EOL', 'EQUALS', 'IDENTIFIER', 'LABRACKET', 'LBRACE', 'LBRACKET', 'LPAREN', 'RABRACKET', 'RBRACE', 'RBRACKET', 'RPAREN', 'TABLE', 'TEXT'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_IDENTIFIER>[A-Za-z][A-Za-z0-9-_]*)|(?P<t_EOL>[\\n\\r]+)|(?P<t_LPAREN>\\()|(?P<t_RPAREN>\\))|(?P<t_LBRACKET>\\[)|(?P<t_RBRACKET>\\])|(?P<t_LBRACE>\\{)|(?P<t_RBRACE>\\})|(?P<t_ARROW>->)|(?P<t_EQUALS>=)|(?P<t_LABRACKET><)|(?P<t_RABRACKET>>)|(?P<t_COLON>:)|(?P<t_COMMA>,)', [None, ('t_IDENTIFIER', 'IDENTIFIER'), (None, 'EOL'), (None, 'LPAREN'), (None, 'RPAREN'), (None, 'LBRACKET'), (None, 'RBRACKET'), (None, 'LBRACE'), (None, 'RBRACE'), (None, 'ARROW'), (None, 'EQUALS'), (None, 'LABRACKET'), (None, 'RABRACKET'), (None, 'COLON'), (None, 'COMMA')])]}
_lexstateignore = {'INITIAL': ' '}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
