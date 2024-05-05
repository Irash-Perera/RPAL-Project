#!/bin/bash

if [ "$1" == "-ast" ]; then
    python3 ast_driver.py -ast
elif [ "$1" == "-std" ]; then
    python3 std_ast_driver.py -std
else
    python3 output_driver.py
fi