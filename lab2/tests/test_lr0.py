from models import lr0
from lab2.utils import reader

def test_lr0():
    grammar = """
    S -> B B
    B -> a B
    B -> b
    """
    
    production = reader.read_grammar(grammar)
    parser = lr0.LR0(production)
    
    # TO-DO
