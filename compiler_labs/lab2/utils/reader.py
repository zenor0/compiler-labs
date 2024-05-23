from compiler_labs.lab2.models import Production, Symbol
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


COMMENT_RE = r"//.*"
OR_PRODUCTION_RE = r"\s*(\S+)\s*->\s*(.+)([.|\s|\n]* \| \s*)(.+)"
REPLACE_RE = r"\n\1 -> \2 \n\1 -> \4\n"

def read_grammar(raw : str) -> list[Production]:
    # remove comments
    raw = re.sub(COMMENT_RE, "", raw)
    
    while re.search(OR_PRODUCTION_RE, raw, re.MULTILINE):
        raw = re.sub(OR_PRODUCTION_RE, REPLACE_RE, raw, re.MULTILINE)
    
    match = re.findall(PRODUCTION_RE, raw)
    
    # create a list of productions
    productions = []
    for prod in match:
        head = Symbol(prod[0])
        body = [Symbol(x) for x in prod[1].split()]
        productions.append(Production(head, body))
    
    # de-duplicate
    return [x for i, x in enumerate(productions) if productions.index(x) == i]