.PHONY: dist run clean

all: dist

.venv:
	python -m venv --upgrade .
	touch .venv

.setup: .venv requirements.txt
	./bin/pip install -r requirements.txt
	touch .setup

run:
	./bin/python -m pyhedron

clean:
	rm -rf __pycache__
	rm -rf pyhedron/__pycache__
	rm dist/*
	rm .venv
	rm .setup

dist: .setup pyproject.toml readme.rst pyhedron/__init__.py Makefile LICENSE
	./bin/python -m build
