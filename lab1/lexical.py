import sys
import re
from enum import Enum
import warnings

class _TOKEN_TYPE(Enum):
    KEYWORD      = 1
    DELIMITER    = 2
    IDENTIFIER   = 3
    NUMBER       = 4
    STRING       = 5
    OPERATOR     = 6
    CHAR         = 7

class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
       match self.type:
            case _TOKEN_TYPE.KEYWORD:
                return f"<{self.value}>"
            case _TOKEN_TYPE.DELIMITER:
                return f"<{self.value}>"
            case _TOKEN_TYPE.IDENTIFIER:
                return f"<id, {self.value}>"
            case _TOKEN_TYPE.NUMBER:
                return f"<num, {self.value}>"
            case _TOKEN_TYPE.STRING:
                return "<str, {}>".format(repr(self.value).strip('\''))
            case _TOKEN_TYPE.OPERATOR:
                return f"<{self.value}>"
            case _TOKEN_TYPE.CHAR:
                return f"<{self.value}>"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        return self.type == o.type and self.value == o.value

class LexicalParser:
    """ Lexical parser for C language 
    
    Attributes:
    code (str): the code to be parsed
    tokens (list): list of tokens
    
    Usage:
    parser = LexicalParser(code)
    tokens = parser.parse()
    for token in tokens:
        print(token)

    """
    
    """ Define the keywords, delimiters, operators, etc."""
    _keywords = [
            # data types
            "int", "float", "double", "char", "void",
            # control statements
            "if", "else", "for", "while", "do", "switch", "case", "break", "continue", "return",
            # modifiers
            "const", "static", "extern", "register", "auto", "volatile",
            # storage classes
            "typedef", "struct", "union", "enum",
            # constants
            "true", "false", "NULL",
        ]
    _delimiters = ["(", ")", "{", "}", "[", "]", ";", ",", ".", ":"]
    _single_char_operators = ["+", "-", "*", "/", "%", "=", "!", "&", "|", "^", "~", "<", ">", "?"]
    _double_char_operators = ["++", "--", "==", "!=", "<=", ">=", "&&", "||", "<<", ">>", "->"]

    """ Define the regex patterns for parsing """
    _number_pattern =                re.compile(r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
    _string_pattern =                re.compile(r'"[^"]*"')
    _unfinished_string_pattern =     re.compile(r'"[^"]*')
    _comment_pattern =               re.compile(r"//.*")
    _multi_line_comment_pattern =    re.compile(r"/\*.*?\*/", re.DOTALL)
    _identifier_pattern =            re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")
    _preprocessor_pattern =          re.compile(r"#.*")
    _char_pattern =                  re.compile(r"'.'")
    _unfinished_char_pattern =       re.compile(r"'.")
    _anything_till_delimiter_pattern = re.compile(r"[a-zA-Z_0-9]*[\(\)\{\}\[\];,]")
    
    def __init__(self, code: str) -> None:
        """ Initialize the parser with the code to be parsed
        
        Args:
        code (str): the code to be parsed
        
        """
        self.code = code
        self.tokens = []
    
    def parse(self):
        """ Parse the code and return the list of tokens
        
        Returns:
        list: list of tokens
        """
        
        code = self.code
        
        # preprocess the code
        # remove preprocessor and comments in the code
        code = re.sub(self._preprocessor_pattern, "", code)
        code = re.sub(self._comment_pattern, "", code)
        code = re.sub(self._multi_line_comment_pattern, "", code)
        
        # parse the code
        i = 0
        n = len(code)
        while i < n:
            ch = code[i]
            i += 1
            if ch.isspace():
                continue
            if ch in self._delimiters:
                self.tokens.append(Token(_TOKEN_TYPE.DELIMITER, ch))
            elif ch in self._single_char_operators:
                # check if double char operator
                if i < n and ch + code[i] in self._double_char_operators:
                    self.tokens.append(Token(_TOKEN_TYPE.OPERATOR, ch + code[i]))
                    i += 1
                else:
                    self.tokens.append(Token(_TOKEN_TYPE.OPERATOR, ch))
            elif ch == '"':
                match = re.match(self._string_pattern, code[i-1:])
                if match:
                    self.tokens.append(Token(_TOKEN_TYPE.STRING, match.group()))
                    i += len(match.group()) - 1
                else:
                    match = re.match(self._unfinished_string_pattern, code[i-1:])
                    if match:
                        match = re.search(self._anything_till_delimiter_pattern, code[i-1:])
                        warnings.warn("Unfinished string: %s" % match.group(), Warning)
                        i += len(match.group()) - 1
            elif ch == "'":
                match = re.match(self._char_pattern, code[i-1:])
                if match:
                    self.tokens.append(Token(_TOKEN_TYPE.CHAR, match.group()))
                    i += len(match.group()) - 1
                else:
                    match = re.match(self._unfinished_char_pattern, code[i-1:])
                    if match:
                        match = re.search(self._anything_till_delimiter_pattern, code[i-1:])
                        warnings.warn("Unfinished char: %s" % match.group(), Warning)
                        i += len(match.group()) - 1
            elif ch.isdigit():
                match = re.match(self._number_pattern, code[i-1:])
                if match:
                    self.tokens.append(Token(_TOKEN_TYPE.NUMBER, match.group()))
                    i += len(match.group()) - 1
            elif ch.isalpha() or ch == "_":
                match = re.match(self._identifier_pattern, code[i-1:])
                if match:
                    word = match.group()
                    word = word.lower()
                    if word in self._keywords:
                        self.tokens.append(Token(_TOKEN_TYPE.KEYWORD, word))
                    else:
                        self.tokens.append(Token(_TOKEN_TYPE.IDENTIFIER, word))
                    i += len(match.group()) - 1
            else:
                warnings.warn("Unknown character: %s" % ch, Warning)
        return self.tokens

if __name__ == "__main__":
    code = sys.stdin.read()
    parser = LexicalParser(code)
    tokens = parser.parse()
    for token in tokens:
        print(token)