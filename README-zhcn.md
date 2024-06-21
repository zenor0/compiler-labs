# 编译原理实验仓库

[![Python](https://img.shields.io/badge/python-3.10.12-blue.svg)](https://www.python.org/downloads/release/python-31012/)
[![WSL2](https://img.shields.io/badge/WSL2-Ubuntu_22.04-orange.svg)](https://docs.microsoft.com/en-us/windows/wsl/install)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

[English](./README.md) | [中文](./README-zhcn.md)

## 概览

本仓库用于存放福州大学编译原理的实验代码.

实验包括

| 实验序号 | 标题     | 内容                                                 |
| -------- | -------- | ---------------------------------------------------- |
| 1        | 词法分析 | 读入源程序，识别单词，输出单词符号表                 |
| 2        | 语法分析 | 根据文法规则，对单词符号表进行语法分析，输出分析结果 |
| 3        | 语义分析 | 对语法分析结果进行语义分析，输出四元式和三地址码     |

## 特性

1. **词法分析器**

   + 正则表达式分析
   + 输出符号表

2. **语法分析器**

   + 支持自定义文法
   + 检测语法冲突(二义性)
   + 可视化
     + 状态机可视化
     + 语法分析树可视化
   + 输出分析结果
     (包括 FIRST集 和 FOLLOW集, ACTION 表 和 GOTO 表)

3. **语义分析器**

   + 支持自定义含有语义动作的文法
   + 支持自定义语义动作函数
   + 支持 Python 语法的文法代码片段
   + 生成 asm-ish 四元式和三地址码
  
## 预览

### 词法分析

![词法分析](./docs/lexer.png)

### 语法分析

![语法分析](./docs/grammar.png)

#### 可视化

![状态机](./docs/dfa.png)

![语法分析树](./docs/parse_tree.png)


## 运行项目

本项目基于 Python 3.10 on WSL 开发，请在运行之前安装相关依赖。

### Linux

如果你是Linux用户可以使用以下命令进行环境的配置

```bash
make
```

该命令将会创建一个虚拟环境，并在其中并在其中依赖的安装，请在安装完成后手动的激活虚拟环境。

### Windows

>[!WARNING]
> （项目未在 Windows 上进行测试，可能存在未知 BUG。）

如果你是Windows用户，且系统中有 `make` 命令，可以使用以下命令进行环境的配置

```bash
make
```

如果没有 `make` 命令，你可以手动执行以下命令

1. 安装虚拟环境

    ```bash
    python -m venv venv
    ```

2. 激活虚拟环境

3. 安装依赖

    ```bash
    pip install -e .
    ```


## 使用方法

在各个实验文件夹下有详细的使用方法，请查看对应的 README.md 文件。

你可以运行

```bash
make demo
```


来运行每个实验提供的演示.

> [!WARNING]
> 在 Windows 系统下, `touch` `mkdir` 等命令可能无法使用, 请根据实际情况手动创建文件夹和文件.


### 词法分析

运行 `make demo` 后, 会启动程序监听 `./tmp/input` 下的源代码文件, 并将词法分析结果输出到 `./outputs` 下.

`input` 为输入文件, `.out` 为输出文件, `.sym` 为符号表文件.


![词法分析](./docs/lexer.png)

### 语法分析

运行 `make demo` 后, 程序会读入 `./data/grammar1.txt` 文件, 输入 Token 流为 `b a a b` 使用 `LR(1)` 模型分析并输出语法分析结果到 `./outputs` 下.

![语法分析](./docs/grammar.png)

同时还会生成状态机和语法分析树的可视化结果。以可交互式网页的形式保存在 `./outputs` 下。

#### 可视化

这是状态机的可视化结果

![状态机](./docs/dfa.png)

这是语法分析树的可视化结果

![语法分析树](./docs/parse_tree.png)

其中, 分析树中会使用不同的颜色来区分不同类型的符号。

### 语义分析

运行 `make demo` 后, 程序会监控 `./tmp/input` 和 `./tmp/grammar.txt` 文件, 并将语义分析结果输出到 `./outputs` 下.

![语义分析](./docs/semantic.png)

