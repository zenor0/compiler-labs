from utils import reader
from models import Production, Symbol

def test_read_raw():
    raw = """
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
    productions = reader.read_grammar(raw)
    
    assert len(productions) == 10
    assert productions[0] == Production(Symbol('S'), [Symbol('A'), Symbol('B')])
    assert productions[1] == Production(Symbol('S'), [Symbol('b'), Symbol('C')])
    assert productions[2] == Production(Symbol('A'), [Symbol(Symbol.EPSILON)])
    assert productions[3] == Production(Symbol('A'), [Symbol('b')])
    assert productions[4] == Production(Symbol('B'), [Symbol(Symbol.EPSILON)])
    assert productions[5] == Production(Symbol('B'), [Symbol('a'), Symbol('D')])
    assert productions[6] == Production(Symbol('C'), [Symbol('A'), Symbol('D')])
    assert productions[7] == Production(Symbol('C'), [Symbol('b')])
    assert productions[8] == Production(Symbol('D'), [Symbol('a'), Symbol('S')])
    assert productions[9] == Production(Symbol('D'), [Symbol('c')])

def test_read_raw_case2():
    raw = """
    expr     -> expr + term | expr - term | term
    term     -> term * unary | term / unary | unary
    unary    -> ! unary | - unary | factor
    factor   -> ( expr ) | loc | id | num | real | true | false
    """
    productions = reader.read_grammar(raw)
    
    assert len(productions) == 16
    assert productions[0] == Production(Symbol('expr'), [Symbol('expr'), Symbol('+'),  Symbol('term')])
    assert productions[1] == Production(Symbol('expr'), [Symbol('expr'), Symbol('-'),  Symbol('term')])
    assert productions[2] == Production(Symbol('expr'), [Symbol('term')])
    assert productions[3] == Production(Symbol('term'), [Symbol('term'), Symbol('*'),  Symbol('unary')])
    assert productions[4] == Production(Symbol('term'), [Symbol('term'), Symbol('/'),  Symbol('unary')])
    assert productions[5] == Production(Symbol('term'), [Symbol('unary')])
    assert productions[6] == Production(Symbol('unary'), [Symbol('!'), Symbol('unary')])
    assert productions[7] == Production(Symbol('unary'), [Symbol('-'), Symbol('unary')])
    assert productions[8] == Production(Symbol('unary'), [Symbol('factor')])
    assert productions[9] == Production(Symbol('factor'), [Symbol('('), Symbol('expr'),  Symbol(')')])
    assert productions[10] == Production(Symbol('factor'), [Symbol('loc')])
    assert productions[11] == Production(Symbol('factor'), [Symbol('id')])
    assert productions[12] == Production(Symbol('factor'), [Symbol('num')])
    assert productions[13] == Production(Symbol('factor'), [Symbol('real')])
    assert productions[14] == Production(Symbol('factor'), [Symbol('true')])
    assert productions[15] == Production(Symbol('factor'), [Symbol('false')])
    