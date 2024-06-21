# 实验1 词法分析器

> [!NOTE]
> 本文档原文为英文。中文版本由GPT翻译。翻译可能存在一些错误或不准确之处。请以英文版本为准。

[English](./README.md) | [中文](./README-zhcn.md)

## 简介

本实验旨在实现一个简单语言的词法分析器。该语言是C语言的一个子集。词法分析器的任务是识别输入文件中的标记，并输出带有相应词素的标记。

## 特性

1. 词法分析器能够识别以下标记：
    - 关键字：`int`、`char`、`if`、`else`、`while`、`for`、`return`
    - 运算符：`+`、`-`、`*`、`/`、`=`、`==`、`!=`、`>`、`<`、`>=`、`<=`
    - 分隔符：`;`、`,`、`(`、`)`、`{`、`}`
    - 标识符：以字母或下划线开头的字母、数字和下划线的序列
    - 常量：数字的序列
    - 字符：用单引号括起来的字符
    - 字符串：用双引号括起来的字符序列
    - 注释：用`/*`和`*/`括起来的字符序列

2. 支持详细模式。

3. 词法分析器将把标记及其相应的词素输出到输出文件。

## 要求

- Python 3.6 或更高版本
- pytest

## 使用方法

要运行词法分析器，请使用以下命令：

```bash
python3 main.py <input_file>
```

输出将被写入`<input_file>.out`，符号表将被写入`<input_file>.sym`。

您还可以使用`-v`选项启用详细模式：

```bash
python3 main.py -v <input_file>
```

在hello world案例中，您可能会看到类似以下的输出：

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

要运行测试用例，请使用以下命令：

```bash
python3 -m pytest
```

## 示例

输入文件：

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

输出文件：

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

符号表：

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

