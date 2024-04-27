from models import Symbol, Production, Action, END_OF_INPUT
from models.lr0 import LR0
from rich import print
production_re = r'\s*(\S+)\s*->\s*(.+)\n'

import re

if __name__ == '__main__':
    test_raw = """
    S -> A B | b C
    A -> <epsilon> | A -> b
    B -> <epsilon> | B -> a D
    C -> A D | C -> b
    D -> a S | D -> c
    """
    
    test_grammar = """
    S -> A B 
    S -> b C
    A -> <epsilon>
    A -> b
    B -> <epsilon>
    B -> a D
    C -> A D
    C -> b
    D -> a S
    D -> c
    """

    test_grammar = """
    S -> B B
    B -> a B
    B -> b
    """
    
    # TO-DO
    # break down raw string into single productions
    match = re.findall(production_re, test_grammar)
    
    # create a list of productions
    productions = []
    for prod in match:
        head = Symbol(prod[0])
        body = [Symbol(x) for x in prod[1].split()]
        productions.append(Production(head, body))
        
    # grammar = Grammar(productions)
    # print(grammar)
    
    lr0 = LR0(productions)
    
    lr0_table = lr0.dump_table()
    lr0_state_names = lr0.dump_state_names()
    lr0_grammar = lr0.productions
    lr0_symbols = {'terminals': lr0._terminals, 'non_terminals': lr0._non_terminals}
    
    print(lr0_table)
    print(lr0_state_names)
    print(lr0_grammar)
    
    from rich.table import Table
    table = Table(title="LR(0) Table")
    table.add_column("State", justify="center", style="cyan", no_wrap=True)
    table.add_column("Action", justify="center", style="magenta")
    table.add_column("GOTO", justify="center", style="green")
    
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
        table.add_row(*row)
        action_table.add_row(*action_row)
    print(action_table)
        
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
    print(goto_table)

    # print(action_table)
    # print(goto_table)
    # print(table)