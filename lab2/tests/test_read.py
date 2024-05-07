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
    