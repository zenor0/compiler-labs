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

    # Dump state table and state names
    state_table = lr0.dump_table()
    state_names = lr0.dump_state_names()

    # Print state table
    print("State Table:")
    for state_hash, transitions in state_table.items():
        print(f"State {state_names[state_hash]}:")
        for symbol, behavior in transitions.items():
                print(f"    {symbol}: {behavior}")

    # Print state names
    print("\nState Names:")
    for state_hash, name in state_names.items():
        print(f"{name}: {state_hash}")

    lr_parser = LR1(productions)
    print([x.states for x in lr_parser.states])
    print(lr_parser.state_transition)

    json_representation = lr_parser.to_json()

    # Print JSON representation
    print(json_representation)
    with open("lr_parser.json", "w") as json_file:
        json_file.write(json_representation)

    data = json.loads(json_representation)

    # 构建nodeDataArray
    nodeDataArray = []
    for state, state_data in data['states'].items():
        text = '\n'.join(state_data['items'])
        nodeDataArray.append({'key': state_data['name'], 'text': text})

    # 构建linkDataArray
    linkDataArray = [{'from': transition['state_from'], 'to': transition['state_to'], 'text': transition['by_sym_key']}
                     for transition in data['state_transition']]

    print("var nodeDataArray = [")
    for node in nodeDataArray:
        text = " ".join([f"'{line}'" for line in node['text'].split("\n")])
        print(f"\t{{ key: {node['key']}, text: {text} }},")
    print("];")

    print("var linkDataArray = [")
    for link in linkDataArray:
        print(f"\t{{ from: {link['from']}, to: {link['to']}, text: '{link['text']}' }},")
    print("];")
