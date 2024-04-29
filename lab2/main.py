from models.lr0 import LR0
from models.slr1 import SLR1
from utils import reader
from utils import disp

from rich import print
from rich.layout import Layout

if __name__ == '__main__':
    grammar = """
    S -> B B
    B -> a B
    B -> b
    """
    
    grammar = """
    E -> a A
    E -> b B
    A -> c A
    A -> d
    B -> c B
    B -> d
    """
    
    grammar = """
    S -> A B
    A -> a B a
    A -> <epsilon>
    B -> b A b
    B -> <epsilon>
    """
    
    productions = reader.read_grammar(grammar)
    
    lr0 = SLR1(productions)
    
    action_table = disp.get_action_table(lr0)
    goto_table = disp.get_goto_table(lr0)
    first_table = disp.get_first_table(lr0)
    follow_table = disp.get_follow_table(lr0)
    grammar_table = disp.get_grammar_table(lr0)
    
    layout = Layout()
    
    layout.split_row(
        Layout(grammar_table, name="Grammar"),
        Layout(first_table, name="First Set"),
        Layout(follow_table, name="Follow Set"),
        Layout(action_table, name="Action Table"),
        Layout(goto_table, name="GOTO Table")
    )
    
    print(layout)
    