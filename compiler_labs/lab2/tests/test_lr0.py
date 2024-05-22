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
    
    expected_states = [
        { # S0
            "S' -> · S",
            "S -> · B B",
            "B -> · a B",
            "B -> · b"
        },
        { # S1
            "S' -> S ·"
        },
        { # S2
            "S -> B · B",
            "B -> · a B",
            "B -> · b"
        },
        { # S3
            "B -> a · B",
            "B -> · a B",
            "B -> · b",
        },
        { # S4
            "B -> b ·"
        },
        { # S5
            "S -> B B ·"
        },
        { # S6
            "B -> a B ·"
        }
    ]

    for state, expected_state in zip(parser.states, expected_states):
        assert set(str(item) for item in state.states) == expected_state
    

    expected_state_transition = [
        (parser.states[0], "S", parser.states[1]),
        (parser.states[0], "B", parser.states[2]),
        (parser.states[0], "a", parser.states[3]),
        (parser.states[0], "b", parser.states[4]),
        (parser.states[2], "B", parser.states[5]),
        (parser.states[2], "a", parser.states[3]),
        (parser.states[2], "b", parser.states[4]),
        (parser.states[3], "B", parser.states[6]),
        (parser.states[3], "a", parser.states[3]),
        (parser.states[3], "b", parser.states[4]),

    ]
    assert parser.state_transition == expected_state_transition
