from .lexical import LexicalParser, Token, _TOKEN_TYPE
from models import Node

def translation(t: list[Token]) -> list[Node]:
    nodes = []
    
    for token in t:
        if token.type == _TOKEN_TYPE.KEYWORD:
            nodes.append(Node(token.value))
        elif token.type == _TOKEN_TYPE.IDENTIFIER:
            nodes.append(Node('id', token.value))
        elif token.type == _TOKEN_TYPE.NUMBER:
            nodes.append(Node('num', token.value))
        elif token.type == _TOKEN_TYPE.OPERATOR:
            nodes.append(Node(token.value))
        elif token.type == _TOKEN_TYPE.CHAR:
            nodes.append(Node('char', token.value))
        elif token.type == _TOKEN_TYPE.STRING:
            nodes.append(Node('string', token.value))
        else:
            nodes.append(Node(token.value))
    
    return nodes

def parse_source(code: str) -> list[Node]:
    parser = LexicalParser(code)
    tokens = parser.parse()
    return translation(tokens)