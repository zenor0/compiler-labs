
from compiler_labs.lab2.models import Node, Symbol, Production

from compiler_labs.lab2.models.lr1 import LR1
from compiler_labs.lab3.models import Snippet

import logging
logger = logging.getLogger('rich')


def run_snippet_on_node(node: Node, snippet: Snippet, global_functions: dict[str, callable]):
    symbol_info_list = {str(node.production.head): [node]}
    # Assuming the order of the children is the same as the order of the body
    for i, symbol in enumerate(node.production.body):
        if symbol not in symbol_info_list:
            symbol_info_list[str(symbol)] = []
        symbol_info_list[str(symbol)].append(node.children[i])
    
    for key, value in symbol_info_list.items():
        if len(value) == 1:
            symbol_info_list[key] = value[0]
    
    try:
        exec(snippet.code, global_functions, symbol_info_list)
        logger.debug(symbol_info_list)
    except Exception as e:
        # show_node_debug(node)
        logger.error(f"Error executing snippet: {e}, {snippet} in production {node.production}")
        # raise e

def top_down_traverse(node: Node, semantic_productions: list[Production], global_functions: dict[str, callable]):
    if not node.production:
        return
    try:
        match_semantic_production = next(filter(lambda x: x.equal(node.production), semantic_productions))
    except:
        print(semantic_productions)
        logger.error(f"Production {node.production} not found in semantic productions")
        raise Exception(f"Production {node.production} not found in semantic productions")
    logger.debug(f"Matched production: {match_semantic_production}, {node.production}")
    node_symbol_mapping = {}
    cnt = 0
    for i, symbol in enumerate(match_semantic_production.body):
        if isinstance(symbol, Symbol):
            node_symbol_mapping[(symbol, i)] = node.children[cnt]
            cnt += 1
    
    
    for i, item in enumerate(match_semantic_production.body):
        logger.debug(f"Item: {item}")
        if isinstance(item, Snippet):
            run_snippet_on_node(node, item, global_functions)
        elif isinstance(item, Symbol):
            top_down_traverse(node_symbol_mapping[(item, i)], semantic_productions, global_functions)
        else:
            raise Exception(f"Invalid type {item}")
