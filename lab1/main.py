import sys
from lexical import LexicalParser

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Usage: python3 {sys.argv[0]} <filename>')
        return

    filename = sys.argv[1]
    with open(filename, "r") as f:
        code = f.read()
    
    parser = LexicalParser(code)
    tokens = parser.parse()
    for token in tokens:
        print(token)

