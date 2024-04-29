from rich import print
from rich.table import Table

from models import Action, END_OF_INPUT, Symbol
from models.lr0 import LR0

def get_action_table(grammar : LR0):
    lr0_table = grammar.dump_table()
    lr0_state_names = grammar.dump_state_names()
    lr0_symbols = {'terminals': grammar._terminals, 'non_terminals': grammar._non_terminals}

    action_table = Table(title="Action Table")
    action_table.add_column("State", justify="center", style="cyan", no_wrap=True)
    for symbol in lr0_symbols['terminals']:
        action_table.add_column(str(symbol), justify="center", style="red")
    action_table.add_column(END_OF_INPUT, justify="center", style="red")
    
    for state, actions in lr0_table.items():
        row = [lr0_state_names[state]]
        action_row = [lr0_state_names[state]]
        for symbol in lr0_symbols['terminals'] + [Symbol(END_OF_INPUT)]:
            if symbol in actions:
                if actions[symbol].action == Action.SHIFT:
                    content = f'S{lr0_state_names[actions[symbol].value]}'
                    row.append(content)
                    action_row.append(content)
                elif actions[symbol].action == Action.REDUCE:
                    row.append(f'R{actions[symbol].value}')
                    action_row.append(f'R{actions[symbol].value}')
                elif actions[symbol].action == Action.ACCEPT:
                    row.append('ACC')
                    action_row.append('ACC')
                elif actions[symbol].action == Action.GOTO:
                    row.append(f'G{actions[symbol].value}')
                    action_row.append(f'G{actions[symbol].value}')
            else:
                row.append('')
                action_row.append('')
        action_table.add_row(*action_row)
    return action_table
        

def get_goto_table(grammar : LR0):
    lr0_table = grammar.dump_table()
    lr0_state_names = grammar.dump_state_names()
    lr0_symbols = {'terminals': grammar._terminals, 'non_terminals': grammar._non_terminals}

    goto_table = Table(title="GOTO Table")
    goto_table.add_column("State", justify="center", style="cyan", no_wrap=True)
    for symbol in lr0_symbols['non_terminals']:
        goto_table.add_column(str(symbol), justify="center", style="yellow")
        
    for state, actions in lr0_table.items():
        row = [lr0_state_names[state]]
        for symbol in lr0_symbols['non_terminals']:
            if symbol in actions:
                if actions[symbol].action == Action.GOTO:
                    row.append(lr0_state_names[actions[symbol].value])
            else:
                row.append('')
        goto_table.add_row(*row)
    return goto_table

def get_first_table(grammar : LR0):
    first_set = grammar.get_first_set()
    first_table = Table(title="First Set")
    first_table.add_column("sym", justify="left", style="cyan", no_wrap=True)
    first_table.add_column("First Set", justify="left", style="green")
    
    for symbol, first in first_set.items():
        first_table.add_row(str(symbol), ', '.join([str(x) for x in first]))
    return first_table

def get_follow_table(grammar : LR0):
    follow_set = grammar.get_follow_set()
    follow_table = Table(title="Follow Set")
    follow_table.add_column("sym", justify="left", style="cyan", no_wrap=True)
    follow_table.add_column("Follow Set", justify="left", style="green")
    
    for symbol, follow in follow_set.items():
        follow_table.add_row(str(symbol), ', '.join([str(x) for x in follow]))
    return follow_table

def get_grammar_table(grammar: LR0):
    productions = grammar.productions
    grammar_table = Table(title="Grammar")
    grammar_table.add_column("Production", justify="left", style="cyan", no_wrap=True)
    for production in productions:
        grammar_table.add_row(str(production))
    return grammar_table



def show_grammar(grammar : LR0):
    productions = grammar.dump_productions()
    for production in productions:
        print(production)

