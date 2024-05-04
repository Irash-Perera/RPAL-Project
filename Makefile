PYTHON := python
FILES := ast_driver.py std_ast_driver.py output_driver.py
PYFILES := $(wildcard *.py)

all: $(PYFILES)

run_ast: ast_driver.py 
	$(PYTHON) ast_driver.py -ast

run_std_ast: std_ast_driver.py
	$(PYTHON) std_ast_driver.py -std

run_output: output_driver.py
	$(PYTHON) output_driver.py 

clean:
	rm -rf __pycache__ *.pyc

.PHONY: run clean
