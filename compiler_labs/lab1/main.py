import sys
import os

import rich.table
from compiler_labs.lab1.lexical import LexicalParser, _TOKEN_TYPE
import argparse
import logging
import rich
from rich import print
from rich.logging import RichHandler
from rich.columns import Columns
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table

logger = logging.getLogger('rich')
logger.setLevel(logging.INFO)
rich_handler = RichHandler()
logger.addHandler(rich_handler)

def change_file_extension(filename, new_ext):
    parts = filename.rsplit('.', 1)
    
    if len(parts) == 2:
        return parts[0] + '.' + new_ext
    else:
        return filename + '.' + new_ext
    
def read_code(filename) -> str:
    logger.debug(f"Read input file: {filename}")
    try:
        with open(filename, "r") as f:
            code = f.read()
            logger.info(f"File '{filename}' loaded.")
            return code
    except:
        logger.error(f"File '{filename}' not found.")
        sys.exit(1)

def create_token_table(tokens) -> Table:
    token_table = Table(title="Token Table")
    token_table.add_column("Type", style="magenta")
    token_table.add_column("Value", style="green")
    for token in tokens:
        token_table.add_row(token.type.name, str(token.value))
        
    return token_table

def create_symbol_table(symbol_list: dict):
    symbol_table = rich.table.Table(title="Symbol Table")
    symbol_table.add_column("Type", style="magenta")
    symbol_table.add_column("Value", style="green")
    for type in symbol_list:
        for value in symbol_list[type]:
            symbol_table.add_row(type, value)
    return symbol_table

def get_symbol_list(tokens):
    keyword_list = {}
    identifier_list = {}
    number_list = {}
    for token in tokens:
        if token.type == _TOKEN_TYPE.KEYWORD:
            keyword_list[token.value] = keyword_list.get(token.value, 0) + 1
        elif token.type == _TOKEN_TYPE.IDENTIFIER:
            identifier_list[token.value] = identifier_list.get(token.value, 0) + 1
        elif token.type == _TOKEN_TYPE.NUMBER:
            number_list[token.value] = number_list.get(token.value, 0) + 1
            
    symbol_list = {}
    symbol_list['KEYWORD'] = [k for k in keyword_list if keyword_list[k] > 0]
    symbol_list['IDENTIFIER'] = [i for i in identifier_list if identifier_list[i] > 0]
    symbol_list['NUMBER'] = [n for n in number_list if number_list[n] > 0]
    return symbol_list

def save_symbols_to_file(symbol_list: dict, filename='code.sym'):
    with open(filename, "w") as f:
        for type in symbol_list:
            for value in symbol_list[type]:
                f.write(f'{type} {value}\n')
    logger.info(f"Symbols saved to {filename}")

def save_tokens_to_file(tokens, filename='code.out'):
    with open(filename, "w") as f:
        for token in tokens:
            f.write(str(token)+"\n")
    logger.info(f"Tokens saved to {filename}")

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
        parser = LexicalParser(code)
        tokens = parser.parse()
        
        token_filename = self.output_path + change_file_extension(event.src_path.split('/')[-1], 'out')
        save_tokens_to_file(tokens, token_filename)
        
        symbol_filename = self.output_path + change_file_extension(event.src_path.split('/')[-1], 'sym')
        save_symbols_to_file(get_symbol_list(tokens), symbol_filename)
        logger.info('Updated')

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Lexical Parser')
    
    ap.add_argument('filename', type=str, help='input file')
    ap.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    ap.add_argument('-o', '--output', type=str, help='output file path', default='./outputs/')
    ap.add_argument('-w', '--watch', action='store_true', help="watch target file then parse in realtime")
    
    args = ap.parse_args()
    filename = args.filename

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled.")
    
    code = read_code(filename)
    
    if args.watch:
        path = "./tmp/input"

        event_handler = WatchHandler(args.output)
        observer = Observer()
        observer.schedule(event_handler, filename)

        logger.info(f"Start monitoring {filename} for changes...")
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            sys.exit(0)
    
    # start to parse code
    parser = LexicalParser(code)
    tokens = parser.parse()
    logger.info('Parse done.')
    
    # Save tokens to file
    token_filename = args.output + change_file_extension(filename.split('/')[-1], 'out')
    save_tokens_to_file(tokens, token_filename)
    
    # print symbol table
    symbol_list = get_symbol_list(tokens)
    
    symbol_filename = args.output + change_file_extension(filename.split('/')[-1], 'sym')
    save_symbols_to_file(symbol_list, symbol_filename)
        
    logger.info("Showing results:")
    syntax = Syntax(code, "c", line_numbers=True, word_wrap=True, code_width=60)
    panel = Panel(syntax, title="Source code")
    columns = Columns([panel, create_token_table(tokens), create_symbol_table(symbol_list)])
    print(columns)
        
    logger.info("Done. exiting...")
    sys.exit(0)