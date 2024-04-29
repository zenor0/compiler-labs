from models.lr0 import LR0
from models.slr1 import SLR1
from models.lr1 import LR1, END_OF_INPUT, Behavior, Action
from utils import reader
from utils import disp

from rich import print
from rich.layout import Layout
from rich.panel import Panel

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
    
    grammar = """
    E -> E + T
    E -> T
    T -> T * F
    T -> F
    F -> ( E )
    F -> id
    
    """
    
    grammar = """
    S -> B B
    B -> a B
    B -> b
    
    """
    
    productions = reader.read_grammar(grammar)
    
    lr0 = LR1(productions)
    
    action_table = disp.get_action_table(lr0)
    goto_table = disp.get_goto_table(lr0)
    first_table = disp.get_first_table(lr0)
    follow_table = disp.get_follow_table(lr0)
    grammar_table = disp.get_grammar_table(lr0)
    
    upper_layout = Layout()
    lower_layout = Layout()
    
    upper_panel = Panel(upper_layout, title="Grammar")
    lower_panel = Panel(first_table, title="First Set")
    
    upper_layout.split_row(
        grammar_table,
        first_table,
        follow_table,
    )
    lower_layout.split_row(
        action_table, goto_table
    )
    
    layout = Layout()
    layout.split_row(upper_layout, lower_layout)
    
    print(layout)
    
    parse_raw_result = lr0.parse('a a b a b')
    parse_table = disp.show_parse_result(lr0, parse_raw_result)
    
    print(parse_raw_result, parse_table)