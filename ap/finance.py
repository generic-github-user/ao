# This script contains financial tools for tracking my assets and guiding
# decision-making. It is meant to be sufficiently general to support many types
# of currencies, accounts, and transactions. Its main features include an
# efficient and extensible Lark-based parser for human-readable ledgers,
# convenience classes for scripting and analysis, and intuitive rule-based
# automation for tagging, organization, etc. It will eventually provide
# extensive tooling for data processing, plotting, and related tasks.

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

class Token:
    def __init__(self, source: lark.Token, parent=None):
        self.parent: Node = parent
        self.source: lark.Token = source
        for attr in 'type value line column'.split():
            setattr(self, attr, getattr(self.source, attr))
            self.length = len(self.source)

    def text(self): return self.value

    def __str__(self):
        return f'Token <{self.type}, {self.line}:{self.column}> {self.value}'


class Node:
    def __init__(self, source: lark.Tree, parent=None, depth=0, root=None):
        self.parent: Node = parent
        self.root = root if root else self
        self.children = []
        self.source = source
        self.value = None

        self.meta = self.source.meta
        self.type = self.source.data
        self.depth = depth


        for c in self.source.children:
            #print(c)
            if isinstance(c, lark.Tree): self.children.append(
                    Node(c, self, self.depth+1, root=self.root if self.root else self))
            elif c is None: self.children.append(c)
            else:
                assert isinstance(c, lark.Token), c
                self.children.append(Token(c))

    def text(self):
        return ''.join(c.text() for c in self.children)

    def find(self, value, recursive=True):
        #if isinstance(value, callable):
        if callable(value):
            result = [c for c in self.children if value(c)]
        else:
            result = [c for c in self.children if c == value]

        if recursive:
            #for c in self.children if isinstance(c, Node):
            for c in self.children:
                if isinstance(c, Node):
                    result.extend(c.find(value))
        return result
    def __str__(self):
        return f'Node <{self.type}> ({self.depth})' + '\n' + '\n'.join('  '*self.depth + str(n) for n in self.children)


class Transaction(Node):
    def __init__(self, source: lark.Tree, *args, **kwargs):
        super().__init__(source, *args, **kwargs)
        self.amount = self[0]
        for attr in 'status omitted'.split():
            matches = list(filter(lambda x: isinstance(x[0], Pair), x[0].key == attr, self.children))
            if matches:
                setattr(self, attr, matches[0][0].value)

    #def __str__(self):
        #return f'Transaction\n'+'\n'.join('  '*self.depth + )
with open('ledger-grammar.lark', 'r') as grammar:
    parser = Lark(grammar.read(), parser='lalr', lexer='contextual', postlex=TreeIndenter())
    #parser = Lark(grammar.read(), parser='earley', lexer='basic', postlex=TreeIndenter())

with open(ledger, 'r') as f:
    parsed = parser.parse(f.read())
print(parsed.pretty()[:2000])
tree = Node(parsed)
print(tree)

