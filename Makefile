PYTHON := python
FILES := ast_driver.py std_ast_driver.py output_driver.py
PYFILES := $(wildcard *.py)

all: $(PYFILES)

run_ast: $(FILES)
	$(PYTHON) ast_driver.py -ast

run_std_ast: $(FILES)
	$(PYTHON) std_ast_driver.py -std

run_output: $(FILES)
	$(PYTHON) output_driver.py

clean:
	rm -rf __pycache__ *.pyc

.PHONY: run clean
