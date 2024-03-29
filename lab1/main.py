import sys
from lexical import LexicalParser, _TOKEN_TYPE
import warnings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Usage: python3 {sys.argv[0]} <filename>')
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, "r") as f:
        code = f.read()
    parser = LexicalParser(code)
    tokens = parser.parse()

    # save to file
    with open(filename+'.out', "w") as f:
        for token in tokens:
            f.write(str(token)+"\n")
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
