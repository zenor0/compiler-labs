from typing import List
from enum import Enum
from compiler_labs.lab3.models import Snippet
from compiler_labs.lab2.utils.hash import get_hash_digest
import pickle

import logging
logger = logging.getLogger('rich')

EPSILON = '<epsilon>'
END_OF_INPUT = '$'
DOT = '·'


class Symbol:
    EPSILON = EPSILON
    END = END_OF_INPUT
    def __init__(self, name):
        self.value = name
        self._hash = hash(name)

    def __str__(self):
        if self.value == EPSILON:
            return 'ε'
        return self.value

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return self._hash

class Production:
    def __init__(self, head:Symbol, body: List[Symbol]):
        self.head = head
        self.body = body
        
    def equal(self, other):
        def check_if_snippet(x):
            return not isinstance(x, Snippet)
        lhs_body = [x for x in filter(check_if_snippet, self.body)]
        rhs_body = [x for x in filter(check_if_snippet, other.body)]
        return self.head == other.head and lhs_body == rhs_body

    def __str__(self):
        return str(self.head) + ' -> ' + ' '.join([str(x) for x in self.body])

    def __repr__(self):
        return str(self.head) + ' -> ' + ' '.join([str(x) for x in self.body])

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(str(self.head) + str(self.body))



class Node:
    production: Production
    def __init__(self, symbol: Symbol, value = None):
        self.attr = {}
        
        if isinstance(symbol, str):
            symbol = Symbol(symbol)
        self.symbol = symbol
        self.parent = None
        self.children = []
        self.value = value
        
        self.production = None
        
    def set_production(self, prod: Production):
        self.production = prod
        return prod
    
    def add_child(self, child):
        self.children.append(child)
        
    def set_parent(self, parent):
        self.parent = parent
    
    def __repr__(self):
        return self.symbol.value
    
    def __getattr__(self, name):
        if name in self.attr:
            return self.attr[name]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in ['attr', 'symbol', 'parent', 'children', 'value', 'production']:
            super().__setattr__(name, value)
        else:
            self.attr[name] = value

class Item(Production):
    _hash = None
    _str = None
    def __init__(self, production: Production, dot_index: int, lookahead: List[Symbol] = None):
        super().__init__(production.head, production.body)
        self.__original = production
        if self.body == [Symbol(EPSILON)]:
            self.body = []
        self.dot_index = dot_index
        self.lookahead = lookahead

    def get_production(self):
        return self.__original

    def __str__(self):
        if self._str is None:
            if self.lookahead is None:
                self._str = f'{self.head} -> {" ".join([str(x) for x in self.body[:self.dot_index]] + [DOT] + [str(x) for x in self.body[self.dot_index:]])}'
            else:
                self._str = f'{self.head} -> {" ".join([str(x) for x in self.body[:self.dot_index]] + [DOT] + [str(x) for x in self.body[self.dot_index:]])}, {"".join([str(x) for x in self.lookahead])}'
        
        return self._str
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        if self._hash is None:
            self._hash = hash((self.__original, self.dot_index , str(self.lookahead)))
        return self._hash

    def next_symbol(self):
        if self.dot_index == len(self.body):
            return None
        return self.body[self.dot_index]

    def advance(self):
        if self.dot_index == len(self.body):
            return None
        return Item(self.__original, self.dot_index + 1, self.lookahead)
    
    def is_reduce(self) -> bool:
        return self.dot_index == len(self.body)

class State:
    states : List[Item]
    def __init__(self, kernel: List[Item]):
        self.kernel = kernel
        self.states = kernel.copy()
        self._hash = hash(str(kernel))
    
    def __str__(self):
        return f'{self.states}'
    
    def __repr__(self):
        return get_hash_digest(self)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __hash__(self):
        return self._hash

class Action(Enum):
    SHIFT = 1
    REDUCE = 2
    ACCEPT = 3
    GOTO = 4

class Behavior:
    _hash = None
    def __init__(self, action: Action, value: int):
        self.action = action
        self.value = value
        self._hash = hash((action, value))

    def __str__(self):
        return f'{self.action.name} {self.value}'
    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self):
        return self._hash
    
    def __eq__(self, value: object) -> bool:
        return hash(self) == hash(value)


