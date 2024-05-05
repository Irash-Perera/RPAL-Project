# RPAL Interpreter

## Introduction

Welcome to the RPAL Interpreter project! This is a comprehensive implementation of an interpreter for the Right-reference Pedagogic Algorithmic Language (RPAL), built using Python. The project is structured into several key components, each playing a crucial role in the interpretation process.

This project includes the following components:

- **Lexical Analyzer**: This is the first step in our interpretation process. It scans the RPAL source code and converts it into a stream of tokens. Each token represents a meaningful unit of the program, such as a keyword, identifier, or operator.

- **Parser**: The parser takes the stream of tokens produced by the lexical analyzer and constructs an Abstract Syntax Tree (AST). The AST represents the syntactic structure of the RPAL program, with each node corresponding to a programming construct.

- **Standardizer**: The standardizer transforms the AST into a standardized AST. This step ensures that the tree is in a form that can be easily executed by the CSE machine.

- **CSE Machine**: The Control Stack Environment (CSE) machine executes the standardized AST. It simulates the runtime environment of the program, managing function calls and variable bindings.

## Setup

Before running the `run_parser.py` script, please follow these setup instructions:

1. Clone this repository to your local machine.

2. Install Python (if not already installed). You can download Python from [here](https://www.python.org/downloads/).

## File Structure

The project consists of the following Python scripts:

- `ast_driver.py`: This script generates the abstract syntax tree.
- `std_ast_driver.py`: This script standardizes the abstract syntax tree.
- `output_driver.py`: This script generates the output.

## Running the Scripts

You can run the scripts using the provided Makefile. Here are the available commands:

- `make run`: This command prints the output of the program.
- `make run ARGS=-ast`: This command prints the abstract syntax tree.
- `make run ARGS=-std`: This command prints the standardized abstract syntax tree.

## Cleaning Up

To remove all `__pycache__` directories and Python cache files in your repository, you can use the `make clean` command.