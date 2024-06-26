# 语义分析

[English](./README.md) | [中文](./README-zhcn.md)

## 项目说明

本项目旨在实现一个基于Python的语义分析器，用于对特定语法规则和输入文件进行解析和翻译。

项目采用Python 3.10.12开发，并在WSL2 (Ubuntu 22.04)环境下运行。

## 文件结构

```bash
.
├── datas
│   ├── full-sdt                # 完整的语法制导翻译（SDT）的输入文件
│   ├── grammar.txt             # 语法定义文件
│   ├── sample.in               # 示例输入文件
│   ├── sample.out              # 示例输出文件
│   └── sdt.txt                 # 语法制导翻译规则文件
├── err-log.txt                # 错误日志文件，用于记录程序运行时发生的错误
├── full-log.txt               # 完整的日志文件，记录程序的详细运行信息
├── main.py                    # 主程序文件，包含项目的主要逻辑
├── makefile                   # 构建脚本文件，用于自动化执行编译和测试任务
├── models
│   └── semantic.py             # 语义分析模块，包含语法分析中的语义处理逻辑
├── outputs
│   └── parse_tree.html         # 语法分析树的输出文件，HTML格式
├── test_driver.py             # 测试驱动程序，执行项目的测试用例
├── tests
│   ├── array                   # 数组相关的测试用例
│   ├── codes
│   │   ├── array               # 数组代码示例
│   │   ├── calc                # 计算器代码示例
│   │   ├── expr                # 表达式代码示例
│   │   ├── flow                # 流程控制代码示例
│   │   ├── full                # 完整的代码示例
│   │   ├── full-sdt-while      # 带有while语句的完整语法制导翻译示例
│   │   └── function            # 函数代码示例
│   ├── ez-calculator           # 简易计算器的测试用例
│   ├── ez-declaration          # 简易声明的测试用例
│   ├── increment-translation   # 增量翻译的测试用例
│   ├── reverse-polish          # 逆波兰表达式的测试用例
│   └── sample_sdt              # 示例语法制导翻译的测试用例
├── tmp
│   ├── code                    # 临时存放的代码文件
│   ├── error.out               # 临时的错误输出文件
│   ├── grammar.txt             # 临时的语法定义文件
│   ├── input                   # 临时的输入文件
│   ├── test.py                 # 临时的测试文件
│   └── tokens.out              # 临时的词法分析输出文件
└── utils
    ├── display.py              # 显示模块，包含显示语法分析树等功能
    └── reader.py               # 读取模块，包含读取输入文件等功能
```

## 主程序命令行参数

- `filename`: 必填位置参数，用于指定输入的文法文件。
- `-m`, `--mode`: 指定解析器的工作模式，可选值为'lr0','slr1','lr1'，默认为'lr1'。
- `-w`, `--watch`: 开启监视模式，实时解析目标文件的更改。
- `-d`, `--debug`: 开启调试模式。
- `-o`, `--output-path`: 指定输出文件的路径，默认为'./outputs/'。
- `-s`, `--source`: 加载源代码文件，将文件输入到词法分析器中，生成Token流，然后使用语法分析器解析它们。

## 输入文件设计 - 带有语义文法的定义

设计一个规范化的输入文件格式是实现带有语义动作的语法分析的关键。通过引入全局函数/变量的定义以及使用特定符号包裹语义动作，可以使语法定义更加简洁易懂，同时也便于后续的解析和处理。

以下是输入文件的格式说明:

```
'''
预先定义的全局函数/变量
'''

产生式头 -> 产生式体 <<代码片段>> 产生式体
```

### 部分说明

1. **预先定义的全局函数/变量**: 在文件的开头部分，可以使用`'''`来包裹全局函数和变量的定义。这些全局函数和变量可以在后续的语义动作中使用。

2. **产生式定义**:
   ```
   产生式头 -> 产生式体 <<代码片段>> 产生式体
   ```

在语义分析的语句中，为了避免混淆语法中的花括号`{}`，我们使用尖括号`<< >>`来包裹语义动作的代码。每一条产生式的定义包括产生式头和产生式体，并可以嵌入语义动作。

**示例:**
```
'''
def add(x, y):
    return x + y

global_var = 10
'''

E -> E '+' T <<result = add(E1.val, T.val)>>
```

## 四元式设计

四元式是一种用于表示中间代码的数据结构，它由四个部分组成，分别是操作符、操作数1、操作数2和结果。四元式的设计可以帮助我们更好地理解程序的执行过程，同时也方便后续的优化和翻译。

在这个项目中，我们使用 asm-ish 四元式来表示语义分析的结果，以便于后续的翻译和执行。

本实验生成的中间代码所涉及到的四元式指令的说明如下:

| 指令名 | 参数1 | 参数2 | 结果 | 描述 |
|--------|-------|-------|------|------|
| MUL    | 第一个操作数 | 第二个操作数 | 存储结果的地址 | 执行乘法运算 |
| ADD    | 第一个操作数 | 第二个操作数 | 存储结果的地址 | 执行加法运算 |
| MOV    | 源操作数  | 无    | 目标地址  | 将源操作数的值移动到目标地址 |
| PUSH   | 要压入栈的值 | 无    | 无    | 将值压入栈 |
| CALL   | 函数标识符 | 无    | 函数调用地址 | 调用函数 |
| JMP    | 无    | 无    | 跳转目标标签 | 无条件跳转到指定标签 |
| RET    | 返回地址  | 无    | 无    | 从函数返回 |
| JE     | 比较操作数1 | 比较操作数2 | 跳转目标标签 | 如果相等则跳转 |
| JNE    | 比较操作数1 | 比较操作数2 | 跳转目标标签 | 如果不相等则跳转 |
| JL     | 比较操作数1 | 比较操作数2 | 跳转目标标签 | 如果小于则跳转 |
| JLE    | 比较操作数1 | 比较操作数2 | 跳转目标标签 | 如果小于或等于则跳转 |
| JGE    | 比较操作数1 | 比较操作数2 | 跳转目标标签 | 如果大于或等于则跳转 |
| JG     | 比较操作数1 | 比较操作数2 | 跳转目标标签 | 如果大于则跳转 |
| SUB    | 第一个操作数 | 第二个操作数 | 存储结果的地址 | 执行减法运算 |
| DIV    | 第一个操作数 | 第二个操作数 | 存储结果的地址 | 执行除法运算 |
| MOD    | 第一个操作数 | 第二个操作数 | 存储结果的地址 | 执行取模运算 |
| NOT    | 源操作数  | 无    | 存储结果的地址 | 执行逻辑非运算 |
| NEG    | 源操作数  | 无    | 存储结果的地址 | 执行取负运算 |
| INC    | 源操作数  | 增量值  | 存储结果的地址 | 执行加1运算 |
| DEC    | 源操作数  | 减量值  | 存储结果的地址 | 执行减1运算 |

## 运行程序

本实验代码仅在 Ubuntu 22.04 上测试通过，其他环境可能无法正常运行。

你可以通过运行 `make demo` 来执行本项目的演示。运行后程序会监控 `tmp/input` 和 `tmp/code` 文件的变化，并实时解析它的内容。

其中, `tmp/input` 文件用于存放输入的文法文件，`tmp/code` 文件用于存放需要解析的代码文件。

在 `/tests` 目录下，我们提供了一些测试用例，你可以通过运行 `make test` 来执行这些测试用例。

用例包括

- `ez-calculator`: 简易计算器的测试用例
- `ez-declaration`: 简易声明的测试用例
- `increment-translation`: 增量翻译的测试用例
- `reverse-polish`: 逆波兰表达式的测试用例
- `sample_sdt`: 示例语法制导翻译的测试用例
- `array`: 数组相关的测试用例
- `calc`: 计算器代码示例
- `expr`: 表达式代码示例
- `flow`: 流程控制代码示例
- `function`: 函数代码示例