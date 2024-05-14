from models import lr0,Symbol,Production,Grammar
from utils import reader


def test_lr0():
    grammar = """
    S -> B B
    B -> a B
    B -> b
    """
    
    production = reader.read_grammar(grammar)
    parser = lr0.LR0(production)
    
    expected_productions = [
        Grammar([
            Production(Symbol("S'"), [Symbol('·'), Symbol('S')]),
            Production(Symbol('S'), [Symbol('·'), Symbol('B'), Symbol('B')]),
            Production(Symbol('B'), [Symbol('·'), Symbol('a'), Symbol('B')]),
            Production(Symbol('B'), [Symbol('·'), Symbol('b')])
        ]),
        Grammar([
            Production(Symbol("S'"), [Symbol('S'), Symbol('·')])
        ]),
        Grammar([
            Production(Symbol('S'), [Symbol('B'), Symbol('·'), Symbol('B')]),
            Production(Symbol('B'), [Symbol('·'), Symbol('a'), Symbol('B')]),
            Production(Symbol('B'), [Symbol('·'), Symbol('b')])
        ]),
        Grammar([
            Production(Symbol('B'), [Symbol('a'), Symbol('·'), Symbol('B')]),
            Production(Symbol('B'), [Symbol('·'), Symbol('a'), Symbol('B')]),
            Production(Symbol('B'), [Symbol('·'), Symbol('b')])
        ]),
        Grammar([
            Production(Symbol('B'), [Symbol('b'), Symbol('·')])
        ]),
        Grammar([
            Production(Symbol('S'), [Symbol('B'), Symbol('B'), Symbol('·')])
        ]),
        Grammar([
            Production(Symbol('B'), [Symbol('a'), Symbol('B'), Symbol('·')])
        ])
    ]
    for state, expected_production in zip(parser.states, expected_productions):
        productions = []
        for item,production in zip(state.states,expected_production):
            assert str(production) == str(item)
    

    expected_state_transition = [
        (parser.states[0],"S",parser.states[1]),
        (parser.states[0],"B",parser.states[2]),
        (parser.states[0],"a",parser.states[3]),
        (parser.states[0],"b",parser.states[4]),
        (parser.states[2],"B",parser.states[5]),
        (parser.states[2],"a",parser.states[3]),
        (parser.states[2],"b",parser.states[4]),
        (parser.states[3],"B",parser.states[6]),
        (parser.states[3],"a",parser.states[3]),
        (parser.states[3],"b",parser.states[4]),

    ]
    assert parser.state_transition == expected_state_transition
