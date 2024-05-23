import sys
sys.path.append('..')

from compiler_labs.lab3.models import Snippet
from compiler_labs.lab2.models import Production, Symbol
import re

PRODUCTION_RE = r'\s*(\S+)\s*->\s*(.+)\n'
COMMENT_RE = r"//.*"
OR_PRODUCTION_RE = r"\s*(\S+)\s*->\s*(.+)([.|\s|\n]* \| \s*)(.+)"
REPLACE_RE = r"\n\1 -> \2 \n\1 -> \4\n"


FUNC_DEFINITION_RE = r"'''([\s\S]*)'''"
FUNC_SNIPPET_RE = r"<<(.*?)>>"  # non-greedy match

def read_semantic_grammar(raw : str, no_snippet=False) -> list[Production]:
    # remove comments
    raw = re.sub(COMMENT_RE, "", raw)
    
    while re.search(OR_PRODUCTION_RE, raw, re.MULTILINE):
        raw = re.sub(OR_PRODUCTION_RE, REPLACE_RE, raw, re.MULTILINE)
    
    match = re.search(FUNC_DEFINITION_RE, raw, re.MULTILINE)
    raw = re.sub(FUNC_DEFINITION_RE, "", raw)
    
    functions = {}
    if match:
        exec(match.group(1), functions)
    
    if no_snippet:
        raw = re.sub(FUNC_SNIPPET_RE, "", raw)
    
    match = re.findall(PRODUCTION_RE, raw)
    # create a list of productions
    productions = []
    for prod in match:
        head = Symbol(prod[0])
        body_str = prod[1]
        match = re.findall(FUNC_SNIPPET_RE, body_str)
        code_snippets = [x for x in match]
        body_str = re.sub(FUNC_SNIPPET_RE, "<CODE>", body_str)
        
        body = []
        cnt = 0
        for x in body_str.split():
            if x != '<CODE>':
                body.append(Symbol(x))
            else:
                body.append(Snippet(code_snippets[cnt]))
                cnt += 1
        productions.append(Production(head, body))
    
    # de-duplicate
    return [x for i, x in enumerate(productions) if productions.index(x) == i], functions