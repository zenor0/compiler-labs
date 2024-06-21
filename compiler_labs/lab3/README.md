# Semantic Analysis

> [!NOTE]
> This documentation is originally written in Chinese and translated into English using GPT translation. You may find some sentences awkward or difficult to understand. It's very possibly not your fault. Please refer to the original Chinese version for better understanding.

[English](./README.md) | [中文](./README-zhcn.md)

## Project Description

This project aims to implement a semantic analyzer based on Python, which is used to parse and translate specific syntax rules and input files.

The project is developed using Python 3.10.12 and runs on the WSL2 (Ubuntu 22.04) environment.

## File Structure

```bash
.
├── datas
│   ├── full-sdt                # Input file for full syntax-directed translation (SDT)
│   ├── grammar.txt             # Grammar definition file
│   ├── sample.in               # Sample input file
│   ├── sample.out              # Sample output file
│   └── sdt.txt                 # Syntax-directed translation rules file
├── err-log.txt                # Error log file for recording runtime errors
├── full-log.txt               # Complete log file for recording detailed program execution information
├── main.py                    # Main program file containing the main logic of the project
├── makefile                   # Build script file for automating compilation and testing tasks
├── models
│   └── semantic.py             # Semantic analysis module containing semantic processing logic in syntax analysis
├── outputs
│   └── parse_tree.html         # Output file for syntax analysis tree in HTML format
├── test_driver.py             # Test driver program for executing project test cases
├── tests
│   ├── array                   # Test cases related to arrays
│   ├── codes
│   │   ├── array               # Array code examples
│   │   ├── calc                # Calculator code examples
│   │   ├── expr                # Expression code examples
│   │   ├── flow                # Flow control code examples
│   │   ├── full                # Complete code examples
│   │   ├── full-sdt-while      # Complete syntax-directed translation example with while statement
│   │   └── function            # Function code examples
│   ├── ez-calculator           # Test cases for a simple calculator
│   ├── ez-declaration          # Test cases for simple declarations
│   ├── increment-translation   # Test cases for incremental translation
│   ├── reverse-polish          # Test cases for reverse Polish notation
│   └── sample_sdt              # Test cases for sample syntax-directed translation
├── tmp
│   ├── code                    # Temporary code file storage
│   ├── error.out               # Temporary error output file
│   ├── grammar.txt             # Temporary grammar definition file
│   ├── input                   # Temporary input file
│   ├── test.py                 # Temporary test file
│   └── tokens.out              # Temporary lexical analysis output file
└── utils
    ├── display.py              # Display module containing functions for displaying syntax analysis tree, etc.
    └── reader.py               # Reader module containing functions for reading input files, etc.
```

## Main Program Command Line Arguments

- `filename`: Required positional argument specifying the input grammar file.
- `-m`, `--mode`: Specify the working mode of the parser, with optional values of 'lr0', 'slr1', 'lr1', defaulting to 'lr1'.
- `-w`, `--watch`: Enable watch mode to parse changes in the target file in real time.
- `-d`, `--debug`: Enable debug mode.
- `-o`, `--output-path`: Specify the output file path, defaulting to './outputs/'.
- `-s`, `--source`: Load the source code file, input the file into the lexical analyzer to generate a token stream, and then parse them using the syntax analyzer.

## Input File Design - Syntax with Semantic Actions

Designing a standardized input file format is crucial for implementing syntax analysis with semantic actions. By introducing pre-defined global functions/variables and using specific symbols to wrap the semantic action code, the syntax definition becomes more concise and understandable, and it is also convenient for subsequent parsing and processing.

Here is the format specification of the input file:

```
'''
Pre-defined global functions/variables
'''

Production Head -> Production Body <<Code Snippet>> Production Body
```

### Partial Explanation

1. **Pre-defined global functions/variables**: At the beginning of the file, you can use `'''` to wrap the definitions of global functions and variables. These global functions and variables can be used in subsequent semantic actions.

2. **Production Definition**:
   ```
   Production Head -> Production Body <<Code Snippet>> Production Body
   ```

In the semantic analysis statement, to avoid confusion with curly braces `{}` in the syntax, we use angle brackets `<< >>` to wrap the code of the semantic action. Each production definition includes a production head and a production body, and can embed semantic actions.

**Example:**
```
'''
def add(x, y):
    return x + y

global_var = 10
'''

E -> E '+' T <<result = add(E1.val, T.val)>>
```

## Quadruple Design

A quadruple is a data structure used to represent intermediate code, consisting of four parts: operator, operand1, operand2, and result. The design of quadruples helps us better understand the execution process of the program and facilitates subsequent optimization and translation.

In this project, we use asm-ish quadruples to represent the results of semantic analysis, for the purpose of subsequent translation and execution.

The instructions involved in the intermediate code generated in this experiment are described as follows:

| Instruction | Operand1 | Operand2 | Result | Description |
|-------------|----------|----------|--------|-------------|
| MUL         | First operand | Second operand | Address to store the result | Perform multiplication operation |
| ADD         | First operand | Second operand | Address to store the result | Perform addition operation |
| MOV         | Source operand | - | Destination address | Move the value of the source operand to the destination address |
| PUSH        | Value to push onto the stack | - | - | Push the value onto the stack |
| CALL        | Function identifier | - | Function call address | Call a function |
| JMP         | - | - | Jump target label | Unconditionally jump to the specified label |
| RET         | Return address | - | - | Return from a function |
| JE          | Comparison operand1 | Comparison operand2 | Jump target label | Jump if equal |
| JNE         | Comparison operand1 | Comparison operand2 | Jump target label | Jump if not equal |
| JL          | Comparison operand1 | Comparison operand2 | Jump target label | Jump if less than |
| JLE         | Comparison operand1 | Comparison operand2 | Jump target label | Jump if less than or equal to |
| JGE         | Comparison operand1 | Comparison operand2 | Jump target label | Jump if greater than or equal to |
| JG          | Comparison operand1 | Comparison operand2 | Jump target label | Jump if greater than |
| SUB         | First operand | Second operand | Address to store the result | Perform subtraction operation |
| DIV         | First operand | Second operand | Address to store the result | Perform division operation |
| MOD         | First operand | Second operand | Address to store the result | Perform modulus operation |
| NOT         | Source operand | - | Address to store the result | Perform logical NOT operation |
| NEG         | Source operand | - | Address to store the result | Perform negation operation |
| INC         | Source operand | Increment value | Address to store the result | Perform increment operation |
| DEC         | Source operand | Decrement value | Address to store the result | Perform decrement operation |

## Running the Program

This project code has only been tested on Ubuntu 22.04, and may not run properly on other environments.

You can run `make demo` to execute the demonstration of this project. After running, the program will monitor the changes in the `tmp/input` and `tmp/code` files and parse their contents in real time.

Among them, the `tmp/input` file is used to store the input grammar file, and the `tmp/code` file is used to store the code file to be parsed.

In the `/tests` directory, we provide some test cases that you can run by executing `make test`.

The test cases include:

- `ez-calculator`: Test cases for a simple calculator
- `ez-declaration`: Test cases for simple declarations
- `increment-translation`: Test cases for incremental translation
- `reverse-polish`: Test cases for reverse Polish notation
- `sample_sdt`: Test cases for sample syntax-directed translation
- `array`: Test cases related to arrays
- `calc`: Calculator code examples
- `expr`: Expression code examples
- `flow`: Flow control code examples
- `function`: Function code examples