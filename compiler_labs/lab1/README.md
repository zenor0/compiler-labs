# Lab1 Lexical Parser

[English](./README.md) | [中文](./README-zhcn.md)

## Introduction

This lab is to implement a lexical parser for a simple language. The language is a subset of C language. The lexical parser is to recognize the tokens in the input file and output the tokens with their corresponding lexemes.

## Features

1. The lexical parser are able to recognize the following tokens:
   - Keywords: `int`, `char`, `if`, `else`, `while`, `for`, `return`
   - Operators: `+`, `-`, `*`, `/`, `=`, `==`, `!=`, `>`, `<`, `>=`, `<=`
   - Separators: `;`, `,`, `(`, `)`, `{`, `}`
   - Identifiers: a sequence of letters, digits, and underscores, starting with a letter or an underscore
   - Constants: a sequence of digits
    - Characters: a character enclosed in single quotes
    - Strings: a sequence of characters enclosed in double quotes
    - Comments: a sequence of characters enclosed in `/*` and `*/`

2. Verbose mode support.

3. The lexical parser will output the tokens with their corresponding lexemes to the output file.


## Requirements

- Python 3.6 or later
- pytest


## Usage

To run the lexical parser, use the following command:

```bash
python3 main.py <input_file>
```

The output will be written to `<input_file>.out` and symbol table will be written to `<input_file>.sym`.

You can also use the `-v` option to enable the verbose mode:

```bash
python3 main.py -v <input_file>
```

In hello world case, you may see output like this:

```txt
zenor0@DESKTOP-ZENOR0 ~/c/lab1 (main)> python3 main.py -v ./tmp/input
[04/11/24 23:45:16] DEBUG    Verbose mode enabled.            main.py:29
                    DEBUG    Input file: ./tmp/input          main.py:30
                    INFO     File './tmp/input' loaded.       main.py:35
                    DEBUG    Parsing done.                    main.py:46
                    DEBUG    Showing token table:             main.py:47
          Token Table           
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Type       ┃ Value           ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ KEYWORD    │ int             │
│ IDENTIFIER │ main            │
│ DELIMITER  │ (               │
│ DELIMITER  │ )               │
│ DELIMITER  │ {               │
│ IDENTIFIER │ printf          │
│ DELIMITER  │ (               │
│ STRING     │ "Hello, World!" │
│ DELIMITER  │ )               │
│ DELIMITER  │ ;               │
│ KEYWORD    │ return          │
│ NUMBER     │ 0               │
│ DELIMITER  │ ;               │
│ DELIMITER  │ }               │
└────────────┴─────────────────┘
                    INFO     Tokens saved to ./tmp/input.out  main.py:61
                    INFO     Symbol table saved to            main.py:82
                             ./tmp/input.sym                            
                    DEBUG    Symbol Table:                    main.py:85
     Symbol Table      
┏━━━━━━━━━━━━┳━━━━━━━━┓
┃ Type       ┃ Value  ┃
┡━━━━━━━━━━━━╇━━━━━━━━┩
│ KEYWORD    │ int    │
│ KEYWORD    │ return │
│ IDENTIFIER │ main   │
│ IDENTIFIER │ printf │
│ NUMBER     │ 0      │
└────────────┴────────┘
                    INFO     Done. exiting...                 main.py:98
```
To run the test cases, use the following command:

```bash
python3 -m pytest
```

## Example

Input file:

```c
int main()
{
    int i;
    int j;
    int cnt;
    i=385+9*11;
    j=50;
    cnt=0;
    While (true)  
    {      
	cnt=cnt+1;
        if (i == j)
	    break;
	else if (i>j)
	    j=j+1;
	else
	    j=j-1;
    }
}
```

Output file:

```txt
<int>
<id, main>
<(>
<)>
<{>
<int>
<id, i>
<;>
<int>
<id, j>
<;>
<int>
<id, cnt>
<;>
<id, i>
<=>
<num, 385>
<+>
<num, 9>
<*>
<num, 11>
<;>
<id, j>
<=>
<num, 50>
<;>
<id, cnt>
<=>
<num, 0>
<;>
<while>
<(>
<true>
<)>
<{>
<id, cnt>
<=>
<id, cnt>
<+>
<num, 1>
<;>
<if>
<(>
<id, i>
<==>
<id, j>
<)>
<break>
<;>
<else>
<if>
<(>
<id, i>
<>>
<id, j>
<)>
<id, j>
<=>
<id, j>
<+>
<num, 1>
<;>
<else>
<id, j>
<=>
<id, j>
<->
<num, 1>
<;>
<}>
<}>

```

Symbol table:

```txt
KEYWORD int
KEYWORD while
KEYWORD true
KEYWORD if
KEYWORD break
KEYWORD else
IDENTIFIER main
IDENTIFIER i
IDENTIFIER j
IDENTIFIER cnt
NUMBER 385
NUMBER 9
NUMBER 11
NUMBER 50
NUMBER 0
NUMBER 1

```


