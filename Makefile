VENV = .venv
PY = $(VENV)/bin/python
CONFIG = config.json

.PHONY:
	install run debug clean lint lint-strict

install:
	python3 -m venv $(VENV)
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install flake8 mypy pytest

run:
	$(PY) pac-man.py $(CONFIG)

debug:
	$(PY) -m pbd pac-man.py $(CONFIG)

clean:
	find . -path ./$(VENV) -prune -o -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	$(PY) -m flake8 . 
	$(PY) -m mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	$(PY) -m flake8 .
	$(PY) -m mypy . --strict
