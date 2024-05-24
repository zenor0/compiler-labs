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
# FUNC_SNIPPET_RE = r"<<(.*?)>>"  # non-greedy match
FUNC_SNIPPET_RE = r"<<([\s\S]*?)>>"  # non-greedy match and multiline match

CODE_SNIPPET_PLACEHOLDER = "<CODE>"

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
    else:
        match = re.findall(FUNC_SNIPPET_RE, raw)
        # code_snippets = [x for x in match]
        code_snippets = [re.sub(r"\s+", " ", x) for x in match]
        raw = re.sub(FUNC_SNIPPET_RE, CODE_SNIPPET_PLACEHOLDER, raw)
    
    snippet_cnt = 0
    match = re.findall(PRODUCTION_RE, raw)
    # create a list of productions
    productions = []
    for prod in match:
        head = Symbol(prod[0])
        body_str = prod[1]

        body = []
        for x in body_str.split():
            if x != CODE_SNIPPET_PLACEHOLDER:
                body.append(Symbol(x))
            else:
                body.append(Snippet(code_snippets[snippet_cnt]))
                snippet_cnt += 1
        productions.append(Production(head, body))
    
    # de-duplicate
    return [x for i, x in enumerate(productions) if productions.index(x) == i], functions