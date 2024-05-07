from rich import print
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.columns import Columns

from models import Action, END_OF_INPUT, Symbol, Grammar, Node
from utils.hash import get_hash_digest

def _get_action_table(table, state_name, symbols, productions: list):
    action_table = Table(title="Action Table")
    action_table.add_column("State", justify="center", style="cyan", no_wrap=True)
    for symbol in symbols['terminals']:
        action_table.add_column(str(symbol), justify="center", style="red")
    
    for state, actions in table.items():
        action_row = [state_name[state]]
        for symbol in symbols['terminals']:
            if symbol in actions:
                if actions[symbol].action == Action.SHIFT:
                    content = f'S{state_name[actions[symbol].value]}'
                    action_row.append(content)
                elif actions[symbol].action == Action.REDUCE:
                    action_row.append(f'R{productions.index(actions[symbol].value)}')
                elif actions[symbol].action == Action.ACCEPT:
                    action_row.append('ACC')
                elif actions[symbol].action == Action.GOTO:
                    action_row.append(f'G{actions[symbol].value}')
            else:
                action_row.append('')
        action_table.add_row(*action_row)
    return action_table

def get_action_table(grammar : Grammar):
    table, _ = grammar.dump_table()
    state_name = grammar.dump_state_names()
    symbols = {'terminals': grammar._terminals, 'non_terminals': grammar._non_terminals}
    productions = grammar.productions
    return _get_action_table(table, state_name, symbols, productions)
        

def _get_goto_table(table, state_name, symbols):
    goto_table = Table(title="GOTO Table")
    goto_table.add_column("State", justify="center", style="cyan", no_wrap=True)
    for symbol in symbols['non_terminals']:
        goto_table.add_column(str(symbol), justify="center", style="yellow")
        
    for state, actions in table.items():
        row = [state_name[state]]
        for symbol in symbols['non_terminals']:
            if symbol in actions:
                if actions[symbol].action == Action.GOTO:
                    row.append(state_name[actions[symbol].value])
            else:
                row.append('')
        goto_table.add_row(*row)
    return goto_table

def get_goto_table(grammar : Grammar):
    table, _ = grammar.dump_table()
    state_name = grammar.dump_state_names()
    symbols = {'terminals': grammar._terminals, 'non_terminals': grammar._non_terminals}
    return _get_goto_table(table, state_name, symbols)

def _get_first_table(first_set):
    first_table = Table(title="First Set")
    first_table.add_column("sym", justify="left", style="cyan", no_wrap=True)
    first_table.add_column("First Set", justify="left", style="green")
    
    for symbol, first in first_set.items():
        first_table.add_row(str(symbol), ', '.join([str(x) for x in first]))
    return first_table

def get_first_table(grammar : Grammar):
    return _get_first_table(grammar.get_first_set())

def _get_follow_table(follow_set):
    follow_table = Table(title="Follow Set")
    follow_table.add_column("sym", justify="left", style="cyan", no_wrap=True)
    follow_table.add_column("Follow Set", justify="left", style="green")
    
    for symbol, follow in follow_set.items():
        follow_table.add_row(str(symbol), ', '.join([str(x) for x in follow]))
    return follow_table

def get_follow_table(grammar : Grammar):
    return _get_follow_table(grammar.get_follow_set())

def _get_grammar_table(productions):
    grammar_table = Table(title="Grammar")
    grammar_table.add_column("Production", justify="left", style="cyan", no_wrap=True)
    for production in productions:
        grammar_table.add_row(str(production))
    return grammar_table

def get_grammar_table(grammar: Grammar):
    return _get_grammar_table(grammar.productions)

def get_all_info(grammar: Grammar):
    table, _ = grammar.dump_table()
    state_name = grammar.dump_state_names()
    symbols = {'terminals': grammar._terminals, 'non_terminals': grammar._non_terminals}
    first_set = grammar.get_first_set()
    follow_set = grammar.get_follow_set()
    productions = grammar.productions
    
    action_table = _get_action_table(table, state_name, symbols, productions)
    goto_table = _get_goto_table(table, state_name, symbols)
    first_table = _get_first_table(first_set)
    follow_table = _get_follow_table(follow_set)
    grammar_table = _get_grammar_table(productions)
    
    
    layout = Layout()
    
    layout.split_row(
        Layout(name="left"),
        Layout(name="right"),
    )


    left_layout = Layout()
    right_layout = Layout()
    
    left_layout.split_row(
        grammar_table,
        first_table,
        follow_table,
    )
    right_layout.split_row(
        action_table, goto_table
    )
    
    column =  Columns([grammar_table, first_table, follow_table, action_table, goto_table])
    return column
    upper_panel = Panel(left_layout, title="Grammar")
    lower_panel = Panel(right_layout, title="Table")
    layout['left'].update(upper_panel)
    layout['right'].update(lower_panel)
    
    return layout

def show_grammar(grammar : Grammar):
    productions = grammar.dump_productions()
    for production in productions:
        print(production)


def get_parse_table(state_name_map: dict, result: list):
    table = Table(title="Parse Result")
    table.add_column("State", justify="left", style="cyan", no_wrap=True)
    table.add_column("Symbol", justify="left", style="yellow", no_wrap=True)
    table.add_column("Input", justify="right", style="yellow")
    table.add_column("Action", justify="left", style="green")
    
    for obj in result:
        state_list = [state_name_map[x] for x in obj['state']]
        state = ' '.join(state_list)
        symbol = ' '.join([str(x) for x in obj['symbol']]) if obj['symbol'] else ''
        input = ' '.join([str(x) for x in obj['input']])
        action = obj['action']
        table.add_row(str(state), str(symbol), str(input), action)
    return table
