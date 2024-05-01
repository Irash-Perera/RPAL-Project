PYTHON := python
FILES := run_parser.py lexical_analyzer.py parser_1.py
PYFILES := $(wildcard *.py)

# Default target
all: $(PYFILES)


# Target to run the 'run_parser.py' script
run: $(FILES)

	$(PYTHON) run_parser.py

# Clean target
clean:
	rm -rf __pycache__ *.pyc

.PHONY: run clean
