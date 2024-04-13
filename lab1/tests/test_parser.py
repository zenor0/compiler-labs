from lexical import LexicalParser, _TOKEN_TYPE, Token

def parse(src):
    lp = LexicalParser(src)
    tokens = lp.parse()
    for token in tokens:
        print(token)
    return tokens


def test_hello_world():
    code = """ int main() {
        printf("Hello, World!");
        return 0;
    } """
    
    tokens = parse(code)
    assert tokens == [
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "main"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "printf"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.STRING,        '"Hello, World!"'),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "return"),
        Token(_TOKEN_TYPE.NUMBER,        "0"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
    ]

def test_lots_delimiters():
    code = """{ { } } }{ { { {   {}())({}[]}}}}"""
    
    tokens = parse(code)
    assert tokens == [
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.DELIMITER,     "["),
        Token(_TOKEN_TYPE.DELIMITER,     "]"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
    ]
    
def test_basic():
    code = """
    #include <stdio.h>

    int main() {
        int a = 5;
        double b = 3.14;
        char c = 'c';
        return 0;
    }

    """
    tokens = parse(code)
    assert tokens == [
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "main"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "5"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "double"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "3.14"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "char"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "c"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.CHAR,          "'c'"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "return"),
        Token(_TOKEN_TYPE.NUMBER,        "0"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
    ]

def test_calculation():
    code = """
#include <stdio.h>

int main() {
    int a = 5, b = 10;
    int sum = a + b;
    int diff = a - b;
    int prod = a * b;
    int quot = b / a;
    int rem = b % a;
    return 0;
}
"""
    tokens = parse(code)
    assert tokens == [
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "main"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "5"),
        Token(_TOKEN_TYPE.DELIMITER,     ","),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "10"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "sum"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.OPERATOR,      "+"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "diff"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.OPERATOR,      "-"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "prod"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.OPERATOR,      "*"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "quot"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.OPERATOR,      "/"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "rem"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.OPERATOR,      "%"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "return"),
        Token(_TOKEN_TYPE.NUMBER,        "0"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
    ]
    
def test_control_flow():
    code = """
#include <stdio.h>

int main() {
    int a = 5, b = 10;
    if (a < b) {
        printf("a is less than b\\n");
    } else if (a > b) {
        printf("a is greater than b\\n");
    } else {
        printf("a is equal to b\\n");
    }
    return 0;
}

    """
    
    assert parse(code) == [
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "main"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "5"),
        Token(_TOKEN_TYPE.DELIMITER,     ","),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "10"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "if"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.OPERATOR,      "<"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "printf"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.STRING,        '"a is less than b\\n"'),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.KEYWORD,       "else"),
        Token(_TOKEN_TYPE.KEYWORD,       "if"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.OPERATOR,      ">"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "printf"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.STRING,        '"a is greater than b\\n"'),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,    ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.KEYWORD,       "else"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "printf"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.STRING,        '"a is equal to b\\n"'),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.KEYWORD,       "return"),
        Token(_TOKEN_TYPE.NUMBER,        "0"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
    ]
    
def test_loops():
    code = """
#include <stdio.h>

int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    int n = 5;
    printf("The factorial of %d is %d\\n", n, factorial(n));
    return 0;
}
"""
    assert parse(code) == [
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "factorial"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "n"),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "result"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "1"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "for"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "i"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "1"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "i"),
        Token(_TOKEN_TYPE.OPERATOR,      "<="),
        Token(_TOKEN_TYPE.IDENTIFIER,    "n"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "i"),
        Token(_TOKEN_TYPE.OPERATOR,      "++"),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "result"),
        Token(_TOKEN_TYPE.OPERATOR,      "*"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.IDENTIFIER,    "i"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.KEYWORD,       "return"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "result"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "main"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "n"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "5"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "printf"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.STRING,        '"The factorial of %d is %d\\n"'),
        Token(_TOKEN_TYPE.DELIMITER,     ","),
        Token(_TOKEN_TYPE.IDENTIFIER,    "n"),
        Token(_TOKEN_TYPE.DELIMITER,     ","),
        Token(_TOKEN_TYPE.IDENTIFIER,    "factorial"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.IDENTIFIER,    "n"),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "return"),
        Token(_TOKEN_TYPE.NUMBER,        "0"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
    ]
    
def test_comments():
    code = """
#include <stdio.h>

// This is a single line comment

/* This is a
   multi-line
   comment */

int main() {
    printf("Hello, World!\\n");
    return 0;
}
"""
    assert parse(code) == [
        Token(_TOKEN_TYPE.KEYWORD,       "int"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "main"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     "{"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "printf"),
        Token(_TOKEN_TYPE.DELIMITER,     "("),
        Token(_TOKEN_TYPE.STRING,        "\"Hello, World!\\n\""),
        Token(_TOKEN_TYPE.DELIMITER,     ")"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.KEYWORD,       "return"),
        Token(_TOKEN_TYPE.NUMBER,        "0"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.DELIMITER,     "}"),
    ]

def test_numbers():
    code = """
a = 123; b=123.456; c=0.123; d=123.0; e=0.0; i=123e4; j=123e-4; k=123e+4; l=123.456e4; m=123.456e-4; n=123.456e+4;
"""
    assert parse(code) == [
        Token(_TOKEN_TYPE.IDENTIFIER,    "a"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "123"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "b"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "123.456"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "c"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "0.123"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "d"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "123.0"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "e"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "0.0"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "i"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "123e4"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "j"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "123e-4"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "k"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "123e+4"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "l"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "123.456e4"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "m"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "123.456e-4"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
        Token(_TOKEN_TYPE.IDENTIFIER,    "n"),
        Token(_TOKEN_TYPE.OPERATOR,      "="),
        Token(_TOKEN_TYPE.NUMBER,        "123.456e+4"),
        Token(_TOKEN_TYPE.DELIMITER,     ";"),
    ]

def test_string():
    code = """
"string" "unfinish jskldfadsf;

int i;
    """
        
    assert parse(code) == [
            Token(_TOKEN_TYPE.STRING, '"string"'),
            Token(_TOKEN_TYPE.KEYWORD, "int"),
            Token(_TOKEN_TYPE.IDENTIFIER, "i"),
            Token(_TOKEN_TYPE.DELIMITER, ";"),
        ]
    
def test_char():
    code = """
'c' 'unfinish jskldfadsf;

int i;
    """
        
    assert parse(code) == [
            Token(_TOKEN_TYPE.CHAR, "'c'"),
            Token(_TOKEN_TYPE.KEYWORD, "int"),
            Token(_TOKEN_TYPE.IDENTIFIER, "i"),
            Token(_TOKEN_TYPE.DELIMITER, ";"),
        ]
    
def test_undefined_char():
    code = """
；。。。
    """
        
    assert parse(code) == [
        ]
    