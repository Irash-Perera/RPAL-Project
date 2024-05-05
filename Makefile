PYTHON := python3
FILES := ast_driver.py std_ast_driver.py output_driver.py
PYFILES := $(wildcard *.py)
ARGS :=

all: $(PYFILES)

run:
	./run.sh $(ARGS)

clean:
	rm -rf __pycache__ *.pyc

.PHONY: run clean
