from models import Action, END_OF_INPUT, Symbol, Grammar, Node
from utils.hash import get_hash_digest

import pandas as pd
from pandas import DataFrame

def _get_action_table(table, state_name, symbols, productions: list):
    action_table = DataFrame(columns=["State"] + [str(symbol) for symbol in symbols['terminals']])
    
    count = 0
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
        action_table.loc[count] = action_row
        count += 1
    return action_table

def get_action_table(grammar : Grammar):
    table, _ = grammar.dump_table()
    state_name = grammar.dump_state_names()
    symbols = {'terminals': grammar._terminals, 'non_terminals': grammar._non_terminals}
    productions = grammar.productions
    return _get_action_table(table, state_name, symbols, productions)
        

def _get_goto_table(table, state_name, symbols):
    goto_table = DataFrame(columns=["State"] + [str(symbol) for symbol in symbols['non_terminals']])
    
    count = 0
    for state, actions in table.items():
        row = [state_name[state]]
        for symbol in symbols['non_terminals']:
            if symbol in actions:
                if actions[symbol].action == Action.GOTO:
                    row.append(state_name[actions[symbol].value])
            else:
                row.append('')
        goto_table.loc[count] = row
        count += 1
    return goto_table
        

def get_goto_table(grammar : Grammar):
    table, _ = grammar.dump_table()
    state_name = grammar.dump_state_names()
    symbols = {'terminals': grammar._terminals, 'non_terminals': grammar._non_terminals}
    return _get_goto_table(table, state_name, symbols)

def _get_first_table(first_set):
    first_table = DataFrame(columns=["sym", "First Set"])
    for symbol, first in first_set.items():
        first_table.loc[str(symbol)] = [str(symbol), ', '.join([str(x) for x in first])]
    return first_table


def get_first_table(grammar : Grammar):
    return _get_first_table(grammar.get_first_set())

def _get_follow_table(follow_set):
    follow_table = DataFrame(columns=["sym", "Follow Set"])
    for symbol, follow in follow_set.items():
        follow_table.loc[str(symbol)] = [str(symbol), ', '.join([str(x) for x in follow])]
    return follow_table

    
    
    follow_table = Table(title="Follow Set")
    follow_table.add_column("sym", justify="left", style="cyan", no_wrap=True)
    follow_table.add_column("Follow Set", justify="left", style="green")
    
    for symbol, follow in follow_set.items():
        follow_table.add_row(str(symbol), ', '.join([str(x) for x in follow]))
    return follow_table

def get_follow_table(grammar : Grammar):
    return _get_follow_table(grammar.get_follow_set())

def _get_grammar_table(productions):
    grammar_table = DataFrame(columns=["Production"])
    for index, production in enumerate(productions):
        grammar_table.loc[index] = [str(production)]
    return grammar_table

    
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
    
    output_path = './tmp/outputs/'
    action_table.to_csv(output_path+'action_table.csv', index=False)
    goto_table.to_csv(output_path+'goto_table.csv', index=False)
    first_table.to_csv(output_path+'first_table.csv', index=False)
    follow_table.to_csv(output_path+'follow_table.csv', index=False)
    grammar_table.to_csv(output_path+'grammar_table.csv', index=False)
    
    
    
    

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
