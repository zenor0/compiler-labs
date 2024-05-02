import sys

import argparse
import logging

from rich import print
from rich.logging import RichHandler
from rich.columns import Columns

from models import *
from models.lr0 import LR0
from models.slr1 import SLR1
from models.lr1 import LR1
from utils import display
from utils import reader

logger = logging.getLogger('rich')
logger.setLevel(logging.INFO)
rich_handler = RichHandler()
logger.addHandler(rich_handler)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Grammar Parser')
    
    ap.add_argument('filename', type=str, help='input grammar file')
    ap.add_argument('-m', '--mode', type=str, help='mode', default='lr1')
    ap.add_argument('-s', '--save-binary', type=str, help='save binary file', default=False)
    ap.add_argument('-l', '--load-binary', type=str, help='load binary file', default=False)
    ap.add_argument('-p', '--parse', type=str, help='parse string', default=False)
    ap.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    ap.add_argument('-o', '--output-path', type=str, help='output file path', default='./outputs/')
    ap.add_argument('-t', '--stdout', action='store_true', help='print to stdout')
    
    args = ap.parse_args()

    filename = args.filename
    mode = args.mode.lower()
    save_binary = args.save_binary
    load_binary = args.load_binary
    output_path = args.output_path
    verbose = args.verbose
    stdout = args.stdout
    parse = args.parse
    
    
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled.")
        logger.debug(f"Input file: {filename}")
    
    try:
        with open(filename, "r") as f:
            grammar_raw = f.read()
            logger.info(f"File '{filename}' loaded.")
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        sys.exit(1)
        
    # start to parse grammar
    if load_binary:
        with open(output_path + load_binary, 'rb') as f:
            binary = f.read()
            grammar = Grammar.load(binary)
        logger.info(f"Grammar loaded from {load_binary}")
    else:
        productions = reader.read_grammar(grammar_raw)
        match mode:
            case 'lr0':
                grammar = LR0(productions)
            case 'slr1':
                grammar = SLR1(productions)
            case 'lr1':
                grammar = LR1(productions)
            case _:
                logger.error(f"Invalid mode: {mode}")
                sys.exit(1)
    
    logger.info("Parsing done.")
    logger.info("Grammar info:")
    info = display.get_all_info(grammar)
    print(info)
    
    if save_binary:
        binary = grammar.dump()
        with open(output_path + save_binary, 'wb') as f:
            f.write(binary)
        
        logger.info(f"Grammar saved to {save_binary}")
        
    if stdout:
        print(display.get_all_info(grammar))

    if parse:
        logger.info(f"Parsing string: {parse}")
        logger.debug("Parsing...")
        result, stack = grammar.parse_node(parse)
        
        result_table = display.get_parse_table(grammar.dump_state_names(), result)
        print(result_table)
        logger.info("Parsing done.")
    
    
    logger.info('Done. Exiting...')