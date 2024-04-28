from models import Production, Symbol
import re

PRODUCTION_RE = r'\s*(\S+)\s*->\s*(.+)\n'


test_raw = """
S -> A B | b C
A -> <epsilon> | A -> b
B -> <epsilon> | B -> a D
C -> A D | C -> b
D -> a S | D -> c
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

def read_grammar(raw : str) -> list[Production]:
    # TO-DO
    # break down raw string into single productions
    match = re.findall(PRODUCTION_RE, raw)
    
    # create a list of productions
    productions = []
    for prod in match:
        head = Symbol(prod[0])
        body = [Symbol(x) for x in prod[1].split()]
        productions.append(Production(head, body))
    
    return productions