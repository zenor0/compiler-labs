import sys
from lexical import LexicalParser, _TOKEN_TYPE
import argparse
import logging
import rich
# from rich import logging

# set logging format
logging.basicConfig(format='%(levelname)s: \t%(message)s')


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Lexical Parser')
    
    ap.add_argument('filename', type=str, help='input file')
    ap.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    
    args = ap.parse_args()
    filename = args.filename
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled.")
        logging.debug(f"Input file: {filename}")
        logging.debug("-"*20)
    else:
        logging.getLogger().setLevel(logging.INFO)
    
    try:
        with open(filename, "r") as f:
            code = f.read()
            logging.info(f"File '{filename}' loaded.")
    except FileNotFoundError:
        logging.error(f"File '{filename}' not found.")
        sys.exit(1)
    
    
    # start to parse code
    parser = LexicalParser(code)
    tokens = parser.parse()
    
    if args.verbose:
        logging.debug("-"*20)
        logging.debug("Tokens: ")
        logging.debug("-"*20)
        for token in tokens:
            logging.debug(token)
        logging.debug("-"*20)

    # save to file
    with open(filename+'.out', "w") as f:
        for token in tokens:
            f.write(str(token)+"\n")
    logging.info(f"Tokens saved to {filename}.out")
    
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
    logging.info(f"Symbol table saved to {filename}.sym")
            
    if args.verbose:
        logging.debug("-"*20)
        logging.debug("Symbol Table: ")
        logging.debug("-"*20)
        for k in keyword_list:
            logging.debug(f'KEYWORD\t\t {k}')
        for i in identifier_list:
            logging.debug(f'IDENTIFIER\t {i}')
        for n in number_list:
            logging.debug(f'NUMBER\t\t {n}')
        
        logging.debug("-"*20)            
    
    
    logging.info("Done. exiting...")