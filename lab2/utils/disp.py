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


def show_grammar(grammar : LR0):
    productions = grammar.dump_productions()
    for production in productions:
        print(production)
    