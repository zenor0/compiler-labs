from models import Production, Symbol
import re

PRODUCTION_RE = r'\s*(\S+)\s*->\s*(.+)\n'


test_raw = """
S -> A B | b C
A -> <epsilon> | b
B -> <epsilon> | a D
C -> A D | b
D -> a S | c
"""

test_grammar = """
S -> A B 
S -> b C
A -> <epsilon>
A -> b
B -> <epsilon>
B -> a D
C -> A D
C -> b
D -> a S
D -> c
"""

test_grammar = """
S -> B B
B -> a B
B -> b
"""


import re
from models import Production, Symbol

OR_PRODUCTION_RE = r'\s*(\S+)\s*->\s*.+([.|\s|\n]*\|\s*)(.+)'
def parse_raw(raw: str):

    return raw

def read_grammar(raw : str) -> list[Production]:
    match = re.findall(OR_PRODUCTION_RE, raw)
    while match:
        for m in match:
            raw = raw.replace(m[1]+m[2], f'\n{m[0]} -> {m[2]}', 1)
        match = re.findall(OR_PRODUCTION_RE, raw)
    
    match = re.findall(PRODUCTION_RE, raw)
    
    # create a list of productions
    productions = []
    for prod in match:
        head = Symbol(prod[0])
        body = [Symbol(x) for x in prod[1].split()]
        productions.append(Production(head, body))
    
    # de-duplicate
    return [x for i, x in enumerate(productions) if productions.index(x) == i]