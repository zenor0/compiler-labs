import sys

import rich.table
from lexical import LexicalParser, _TOKEN_TYPE
import argparse
import logging
import rich
from rich.logging import RichHandler

# from rich import logging

# set logging format
logger = logging.getLogger('rich')
logger.setLevel(logging.INFO)
rich_handler = RichHandler()
logger.addHandler(rich_handler)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Lexical Parser')
    
    ap.add_argument('filename', type=str, help='input file')
    ap.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    
    args = ap.parse_args()
    filename = args.filename
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled.")
        logger.debug(f"Input file: {filename}")
    
    try:
        with open(filename, "r") as f:
            code = f.read()
            logger.info(f"File '{filename}' loaded.")
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        sys.exit(1)
    
    
    # start to parse code
    parser = LexicalParser(code)
    tokens = parser.parse()
    
    if args.verbose:
        logger.debug("Parsing done.")
        logger.debug("Showing token table:")
        table = rich.table.Table(title="Token Table")
        table.add_column("Type", style="magenta")
        table.add_column("Value", style="green")
        for token in tokens:
            table.add_row(token.type.name, str(token.value))
        console = rich.console.Console()
        console.print(table)
        
        
    # Save tokens to file
    with open(filename+'.out', "w") as f:
        for token in tokens:
            f.write(str(token)+"\n")
    logger.info(f"Tokens saved to {filename}.out")
    
    # print symbol table
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
    
    with open(filename + '.sym', "w") as f:
        for k in keyword_list:
            f.write(f'KEYWORD {k}\n')
        for i in identifier_list:
            f.write(f'IDENTIFIER {i}\n')
        for n in number_list:
            f.write(f'NUMBER {n}\n')
    logger.info(f"Symbol table saved to {filename}.sym")
            
    if args.verbose:
        logger.debug("Symbol Table: ")
        table = rich.table.Table(title="Symbol Table")
        table.add_column("Type", style="magenta")
        table.add_column("Value", style="green")
        for k in keyword_list:
            table.add_row("KEYWORD", k)
        for i in identifier_list:
            table.add_row("IDENTIFIER", i)
        for n in number_list:
            table.add_row("NUMBER", n)
        console.print(table)
        
    
    logger.info("Done. exiting...")