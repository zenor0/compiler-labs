from models import lr1,Symbol,Production,Grammar
from utils import reader


def test_lr1():
    grammar = """
    S -> B B
    B -> a B
    B -> b
    """
    
    production = reader.read_grammar(grammar)
    parser = lr1.LR1(production)

    expected_states = [
        { # S0
            "S' -> · S, $",
            "S -> · B B, $",
            "B -> · a B, b",
            "B -> · a B, a",
            "B -> · b, a",
            "B -> · b, b"
        },
        { # S1
            "S' -> S ·, $"
        },
        { # S2
            "S -> B · B, $",
            "B -> · a B, $",
            "B -> · b, $"
        },
        { # S3
            "B -> a · B, a",
            "B -> a · B, b",
            "B -> · a B, a",
            "B -> · a B, b",
            "B -> · b, a",
            "B -> · b, b"
        },
        { # S4
            "B -> b ·, a",
            "B -> b ·, b"
        },
        { # S5
            "S -> B B ·, $"
        },
        { # S6
            "B -> a · B, $",
            "B -> · a B, $",
            "B -> · b, $"
        },
        { # S7
            "B -> b ·, $"
        },
        { # S8
            "B -> a B ·, a",
            "B -> a B ·, b"
        },
        { # S9
            "B -> a B ·, $"
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
        (parser.states[2], "a", parser.states[6]),
        (parser.states[2], "b", parser.states[7]),
        (parser.states[3], "B", parser.states[8]),
        (parser.states[3], "a", parser.states[3]),
        (parser.states[3], "b", parser.states[4]),
        (parser.states[6], "B", parser.states[9]),
        (parser.states[6], "a", parser.states[6]),
        (parser.states[6], "b", parser.states[7]),
    ]

    assert parser.state_transition == expected_state_transition
