from models import Symbol, Production, Action, END_OF_INPUT
from models.lr0 import LR0
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
    
    productions = reader.read_grammar(grammar)
    
    lr0 = LR0(productions)
    
    action_table = disp.get_action_table(lr0)
    goto_table = disp.get_goto_table(lr0)
    
    layout = Layout()
    
    layout.split_row(
        Layout(action_table, name="Action Table"),
        Layout(goto_table, name="GOTO Table")
    )
    
    print(layout)
    