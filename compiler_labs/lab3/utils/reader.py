import sys
sys.path.append('..')

from lab2.models import Production, Symbol
import re

PRODUCTION_RE = r'\s*(\S+)\s*->\s*(.+)\n'
COMMENT_RE = r"//.*"
OR_PRODUCTION_RE = r"\s*(\S+)\s*->\s*(.+)([.|\s|\n]* \| \s*)(.+)"
REPLACE_RE = r"\n\1 -> \2 \n\1 -> \4\n"


FUNC_DEFINITION_RE = r"'''([\s\S]*)'''"
FUNC_SNIPPET_RE = r"<(.+)>"

def read_semantic_grammar(raw : str) -> list[Production]:
    # remove comments
    raw = re.sub(COMMENT_RE, "", raw)
    
    while re.search(OR_PRODUCTION_RE, raw, re.MULTILINE):
        raw = re.sub(OR_PRODUCTION_RE, REPLACE_RE, raw, re.MULTILINE)
    
    match = re.search(FUNC_DEFINITION_RE, raw, re.MULTILINE)
    raw = re.sub(FUNC_DEFINITION_RE, "", raw)
    
    functions = {}
    if match:
        exec(match.group(1), functions)
    
    for key, value in functions.items():
        print(key)   
    
    match = re.findall(PRODUCTION_RE, raw)
    # create a list of productions
    productions = []
    for prod in match:
        head = Symbol(prod[0])
        body = [Symbol(x) for x in prod[1].split()]
        productions.append(Production(head, body))
    
    # de-duplicate
    return [x for i, x in enumerate(productions) if productions.index(x) == i]