from rich import print
from rich.table import Table

from models import Action, END_OF_INPUT, Symbol, Grammar, Node
from utils.hash import get_hash_digest

def get_action_table(grammar : Grammar):
    table = grammar.dump_table()
    state_name = grammar.dump_state_names()
    symbols = {'terminals': grammar._terminals, 'non_terminals': grammar._non_terminals}

    action_table = Table(title="Action Table")
    action_table.add_column("State", justify="center", style="cyan", no_wrap=True)
    for symbol in symbols['terminals']:
        action_table.add_column(str(symbol), justify="center", style="red")
    
    for state, actions in table.items():
        row = [state_name[state]]
        action_row = [state_name[state]]
        for symbol in symbols['terminals']:
            if symbol in actions:
                if actions[symbol].action == Action.SHIFT:
                    content = f'S{state_name[actions[symbol].value]}'
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
        

def get_goto_table(grammar : Grammar):
    table = grammar.dump_table()
    state_name = grammar.dump_state_names()
    symbols = {'terminals': grammar._terminals, 'non_terminals': grammar._non_terminals}

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

def get_first_table(grammar : Grammar):
    first_set = grammar.get_first_set()
    first_table = Table(title="First Set")
    first_table.add_column("sym", justify="left", style="cyan", no_wrap=True)
    first_table.add_column("First Set", justify="left", style="green")
    
    for symbol, first in first_set.items():
        first_table.add_row(str(symbol), ', '.join([str(x) for x in first]))
    return first_table

def get_follow_table(grammar : Grammar):
    follow_set = grammar.get_follow_set()
    follow_table = Table(title="Follow Set")
    follow_table.add_column("sym", justify="left", style="cyan", no_wrap=True)
    follow_table.add_column("Follow Set", justify="left", style="green")
    
    for symbol, follow in follow_set.items():
        follow_table.add_row(str(symbol), ', '.join([str(x) for x in follow]))
    return follow_table

def get_grammar_table(grammar: Grammar):
    productions = grammar.productions
    grammar_table = Table(title="Grammar")
    grammar_table.add_column("Production", justify="left", style="cyan", no_wrap=True)
    for production in productions:
        grammar_table.add_row(str(production))
    return grammar_table



def show_grammar(grammar : Grammar):
    productions = grammar.dump_productions()
    for production in productions:
        print(production)


def show_parse_result(grammar: Grammar, result: list):
    state_name_map = grammar.dump_state_names()
    
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


def print_tree(node: Node, level=0):
    if node is None:
        return
    print(' ' * 4 * level + '->', node.symbol)
    for child in node.children:
        print_tree(child, level + 1)
        
def first_traverse(node: Node, method, *args):
    if node is None:
        return
    method(node, *args)
    for child in node.children:
        first_traverse(child, method, *args)

def get_node_info(node: Node, style = None):
    if style == None:
        style = 'fill: "#f8f8f8", stroke: "#4d90fe"'
    return f'{{ key:{get_hash_digest(node)}, text: "{str(node.symbol)}", {style}, parent: {get_hash_digest(node.parent)}}}'

def tree2hash(root: Node):
    dump_table = []
    first_traverse(root, lambda x, table: table.append(get_node_info(x)), dump_table)
    return dump_table