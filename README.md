# RPAL Interpreter

## Introduction

Welcome to the RPAL Interpreter project! This is a comprehensive implementation of an interpreter for the Right-reference Pedagogic Algorithmic Language (RPAL), built using Python. The project is structured into several key components, each playing a crucial role in the interpretation process.

This project includes the following components:

- **Lexical Analyzer**: This is the first step in our interpretation process. It scans the RPAL source code and converts it into a stream of tokens. Each token represents a meaningful unit of the program, such as a keyword, identifier, or operator.

- **Parser**: The parser takes the stream of tokens produced by the lexical analyzer and constructs an Abstract Syntax Tree (AST). The AST represents the syntactic structure of the RPAL program, with each node corresponding to a programming construct.

- **Standardizer**: The standardizer transforms the AST into a standardized AST. This step ensures that the tree is in a form that can be easily executed by the CSE machine.

- **CSE Machine**: The Control Stack Environment (CSE) machine executes the standardized AST. It simulates the runtime environment of the program, managing function calls and variable bindings.

## Setup

Before running the scripts, please follow these setup instructions:

1. Clone this repository to your local machine.

2. Install Python (if not already installed). You can download Python from [here](https://www.python.org/downloads/).

3. No additional Python packages are required to install. The project uses only built-in Python libraries.

## File Structure
```
project/
├── myrpal.py
├── Makefile
├── input.txt
└── inputs/
    ├── t1.txt
    └── t2.txt
    .
    .
    .
    └── t10.txt
```
- `myrpal.py`: The main script for processing RPAL files.    
- `Makefile`: A makefile to simplify running the script with different options.
- `input.txt`: The input given in the project description.
- `inputs/`: A directory containing example input files.

## Usage with Makefile

The `Makefile` provides different targets to run the script with different options. 

#### Printing Final Output
To run the RPAL program and print the final output, use the run target. You need to specify the path to the input file using the file variable
```
make run file=path/to/your/input.txt
```
Example:
```
make run file=inputs/t1.txt
```

#### Printing  Abstract Syntax Tree(AST)
To print only the Abstract Syntax Tree (AST), use the ast target.
```
make ast file=path/to/your/input.txt
```

#### Printing Standardized Abstract Syntax Tree(SAST)
To print only the standardized Abstract Syntax Tree (SAST), use the sast target.
```
make sast file=path/to/your/input.txt
```

## Usage with Direct Python Commands

You can also run the scripts directly using the python command with the appropriate switches.

#### Printing Final Output
```
python myrpal.py path/to/your/input.txt
```

#### Printing Abstract Syntax Tree(AST)
```
python myrpal.py path/to/your/input.txt -ast
```

#### Printing Standardized Abstract Syntax Tree(SAST)
```
python myrpal.py path/to/your/input.txt -sast
```

## Cleaning Up
To remove all `__pycache__` directories and Python cache files in your repository, you can use the `make clean` command.

## Troubleshooting

#### Python was not found
If you encounter an error stating that Python was not found, please ensure that Python is installed on your system and that it is added to your system's PATH environment variable.

If you are using the commannd as `python` try using `python3`. Some Linux distributions use `python3` instead of `python`.

#### File Not Found
If the input file specified in the command is not found, double-check the path to the file. Ensure that the path is correct and the file exists.