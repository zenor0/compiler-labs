# 实验1 词法分析

## 引言

本实验旨在实现一个简单语言的词法解析器。该语言是 C 语言的一个子集。词法解析器的任务是识别输入文件中的标记（tokens）并输出这些标记及其对应的词素（lexemes）。

## 特性

1. 词法解析器能够识别以下标记：
   - 关键字：`int`、`char`、`if`、`else`、`while`、`for`、`return`
   - 操作符：`+`、`-`、`*`、`/`、`=`、`==`、`!=`、`>`、`<`、`>=`、`<=`
   - 分隔符：`;`、`,`、`(`、`)`、`{`、`}`
   - 标识符：以字母或下划线开头，后接字母、数字和下划线的序列
   - 常量：数字序列
   - 字符：单引号内的一个字符
   - 字符串：双引号内的字符序列
   - 注释：`/*` 和 `*/` 之间的字符序列

2. 支持啰嗦模式 (verbose)。

3. 词法解析器将把标记及其对应的词素输出到输出文件中。

## 要求

- Python 3.6 或更高版本
- pytest

## 使用方法

要运行词法解析器，请使用以下命令：

```bash
python3 main.py <输入文件>
```

输出将写入 `<输入文件>.out`，符号表将写入 `<输入文件>.sym`。

您还可以使用 `-v` 选项启用啰嗦模式：

```bash
python3 main.py -v <输入文件>
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