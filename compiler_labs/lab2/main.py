import sys
import os
import argparse
import logging

from rich import print
from rich.logging import RichHandler
from rich.columns import Columns
from rich.console import Console

from compiler_labs.lab2.models import *
from compiler_labs.lab2.models.lr0 import LR0
from compiler_labs.lab2.models.slr1 import SLR1
from compiler_labs.lab2.models.lr1 import LR1
from compiler_labs.lab2.utils import display
from compiler_labs.lab2.utils import reader
from compiler_labs.lab2.vis import *
from compiler_labs.lab2.middlewares import parse_source

logger = logging.getLogger('rich')
logger.setLevel(logging.INFO)
rich_handler = RichHandler()
logger.addHandler(rich_handler)

tmp_path = './tmp/'

console_width = None
console = Console(record=True, width=console_width)

def visualize_parse_tree(stack, grammar, output_path):
    logger.info("Visualizing parse tree...")
    html, _ = render_parse_tree(stack, grammar)
    with open(output_path + 'parse_tree.html', 'w') as f:
        f.write(html)
    logger.info("Parse tree saved to 'parse_tree.html'")
    
    
def parse_source_code(code, visualize=False, output_path='./outputs/', debug=False):
    console_parse = Console(record=True)
    
    try:
        result, stack = grammar.parse_node(code)
    except ValueError as e:
        raise e

    result_table = display.get_parse_table(grammar.dump_state_names(), result)
    console_parse.print(f'Parsing sentence: {code}')
    console_parse.print(result_table)
    logger.info("Parsing done.")
    
    if visualize:
        visualize_parse_tree(stack, grammar, output_path)

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WatchHandler(FileSystemEventHandler):
    def __init__(self, output_path):
        super().__init__()
        self.output_path = output_path
        self._modified_times = {}

    def on_modified(self, event):
        if event.is_directory:
            return
        current_modified_time = os.path.getmtime(event.src_path)
        if self._modified_times.get(event.src_path) == current_modified_time:
            return
        self._modified_times[event.src_path] = current_modified_time

        logger.info(f'File {event.src_path} has been modified')
        with open(event.src_path, 'r') as f:
            code = f.read()
        
        node_stream, token_stream = parse_source(code)
        
        with open(tmp_path+'tokens.out', 'w') as f:
            for token in node_stream:
                f.write(str(token)+"\n")
        try:
            parse_source_code(node_stream, True, output_path, True)
        except ValueError as e:
            error_message, error_index = e.args
            err_token = token_stream[error_index]
            logger.error(f'{error_message}, {err_token.line}: {err_token.index}')
            
        logger.info('Update done.')



if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Grammar Parser')
    
    ap.add_argument('filename', type=str, help='input grammar file')
    ap.add_argument('-m', '--mode', type=str, help='mode', default='lr1')
    ap.add_argument('-b', '--binary', type=str, help='Save / Load binary grammar file. If file exist then load, otherwise will save it to the location.', default=False)
    ap.add_argument('-w', '--watch', action='store_true', help="watch target file then parse in realtime")
    ap.add_argument('-d', '--debug', action='store_true', help='debug mode')
    ap.add_argument('-o', '--output-path', type=str, help='output file path', default='./outputs/')
    ap.add_argument('-v', '--visualize', action="store_true", help='visualize parse result')
    
    group = ap.add_mutually_exclusive_group()
    group.add_argument('-p', '--parse', type=str, help='Input parse string manually.', default=False)
    group.add_argument('-s', '--source', type=str, help='Load source code file, pipe file into lexical parser, generate token stream then parse them with grammar parser.', default=False)

    args = ap.parse_args()

    filename = args.filename
    mode = args.mode.lower()
    source_file = args.source
    output_path = args.output_path
    debug = args.debug
    parse = args.parse
    visualize = args.visualize
    
    save_binary = False
    load_binary = False
    if args.binary:
        if os.path.exists(args.binary):
            load_binary = args.binary
        else:
            save_binary = args.binary
    
    
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("debug mode enabled.")
        logger.debug(f"Input file: {filename}")
    
    try:
        with open(filename, "r") as f:
            grammar_raw = f.read()
            logger.info(f"File '{filename}' loaded.")
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        sys.exit(1)
    
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
    console.print(info)

    with open(output_path + 'result.txt', 'w') as f:
        print(info, file=f)
    
    if visualize:
        logger.info("Visualizing state machine...")
        html = render_state_machine(grammar)
        
        with open(output_path + 'state_machine.html', 'w') as f:
            f.write(html)
        logger.info("State machine saved to 'state_machine.html'")
    
    if save_binary:
        binary = grammar.dump()
        with open(output_path + save_binary, 'w') as f:
            f.write(binary)
        
        logger.info(f"Grammar saved to {save_binary}")
        
    
    if args.watch:
        path = "./tmp/input"

        event_handler = WatchHandler(output_path)
        observer = Observer()
        observer.schedule(event_handler, source_file)

        logger.info(f"Start monitoring {source_file} for changes...")
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            sys.exit(0)

    if parse:
        parse_source_code(parse, visualize, output_path, debug)
    
    logger.info('Done. Exiting...')
    console.save_svg(output_path+'results.svg', title='文法分析表生成结果')