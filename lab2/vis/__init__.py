from models import Symbol, Node, Grammar, EPSILON
from utils.hash import get_hash_digest

import json
from jinja2 import Environment, FileSystemLoader


def first_traverse(node: Node, method, *args):
    if node is None:
        return
    method(node, *args)
    for child in node.children:
        first_traverse(child, method, *args)

def format_node(node: Node, grammar: Grammar, style = None):
    if style == None:
        style = {'fill': '#f8f8f8', 'stroke': '#4d90fe'}
        
    style_sheet = {
        'terminal': {'fill': 'white', 'stroke': 'green'},
        'non-terminal': {'fill': 'white', 'stroke': 'blue'},
        'start': {'fill': 'black', 'stroke': 'black', 'color': 'white'},
        'epsilon': {'fill': 'white', 'stroke': 'white'},
    }
    if node.symbol == grammar.productions[1].head:
        style = style | style_sheet['start']
    elif node.symbol == EPSILON:
        style = style | style_sheet['epsilon']
    elif node.symbol in grammar._terminals:
        style = style | style_sheet['terminal']
    elif node.symbol in grammar._non_terminals:
        style = style | style_sheet['non-terminal']
    else:
        style = style | {'fill': 'grey', 'stroke': 'black'}
    
    return {'key': get_hash_digest(node), 'text': str(node.symbol), 'parent': get_hash_digest(node.parent)} | style

def tree2hash(root: Node, grammar: Grammar):
    dump_table = []
    first_traverse(root, lambda x, table: table.append(format_node(x, grammar)), dump_table)
    return dump_table

def render_parse_tree(node_stack: Node | list[Node], grammar: Grammar):
    node_list = []
    for list in [tree2hash(node, grammar) for node in node_stack]:
        node_list += list

    node_list.reverse()
    env = Environment(loader=FileSystemLoader('./vis/templates'))
    template = env.get_template('tree.html')
    return template.render({ 'nodes': json.dumps(node_list) }), node_list

def render_parse_tree_vis(node_stack: Node | list[Node]):
    nodes = []
    edges = []
    for node in node_stack:
        node_table = []
        edge_table = []
        
        def node_table_append(node: Node, nodes, edges):
            nodes.append({'id': get_hash_digest(node), 'label': str(node.symbol)})
            if node.parent is not None:
                edges.append({'from': get_hash_digest(node.parent), 'to': get_hash_digest(node)})

        first_traverse(node, node_table_append, node_table, edge_table)
        nodes.extend(node_table)
        edges.extend(edge_table)

    env = Environment(loader=FileSystemLoader('./vis/templates'))
    template = env.get_template('tree_visjs.html')
    return template.render({ 'nodes': nodes, 'edges': edges }), (nodes, edges)

def render_state_machine(grammar: Grammar):
    states = []
    state_name_map = grammar.dump_state_names()
    for state in grammar.states:
        states.append({"id": state_name_map[state], "label": f"State {state_name_map[state]}" + "\n" + "\n".join(str(x) for x in state.states)})
    
    transitions = []
    for f, s, t in grammar.state_transition:
        transitions.append({"from": state_name_map[f], "to": state_name_map[t], "label": str(s)})

    env = Environment(loader=FileSystemLoader('./vis/templates'))
    template = env.get_template('state_visjs.html')
    return template.render({ 'states': json.dumps(states), 'transitions': json.dumps(transitions) })
