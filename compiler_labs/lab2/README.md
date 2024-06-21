# Syntax Analysis

> [!NOTE]
> This documentaion is orginally written in Chinese. The English version is translated by GPT. There may be some mistakes or inaccuracy in the translation. Please refer to the Chinese version for the original documentation.

[English](./README.md) | [中文](./README-zhcn.md)

## Description

This project implements a simple syntax analyzer.

## Features

It supports the following grammar models:

1. LR(0)
2. SLR(1)
3. LR(1)

And the following operations:

- Read grammar from a file
- Generate a parser for the read grammar
- Parse strings using the generated parser
- Visualize the parsing result

## System Requirements

This project is developed using Python 3.10.12. You can install the required packages by running the following command in the project's root directory:

```bash
make 
```

After installing the dependencies, please manually activate the virtual environment.

If you are a Windows user, you can also manually install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage

You can run the project demo using the following command:

```bash
make demo
```

Alternatively, you can manually run the project using the following command:

```bash
python3 main.py ./data/grammar1.txt -p "b a a b" -m "LR0" -v
```

