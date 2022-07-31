import lark
from lark import Lark
from lark.indenter import Indenter

from config import *

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 2

with open('ledger-grammar.lark', 'r') as grammar:
    parser = Lark(grammar.read(), parser='lalr', lexer='contextual', postlex=TreeIndenter())
    #parser = Lark(grammar.read(), parser='earley', lexer='basic', postlex=TreeIndenter())

with open(ledger, 'r') as f:
    parsed = parser.parse(f.read())
print(parsed.pretty()[:20000])
