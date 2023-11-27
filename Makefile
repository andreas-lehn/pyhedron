.PHONY: dist run clean

MODULE = pyhedron
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
TWINE = $(VENV)/bin/twine

dist: pyproject.toml readme.rst pyhedron/__init__.py LICENSE $(VENV)/pyvenv.cfg
	$(PYTHON) -m build

run: $(VENV)/pyvenv.cfg
	$(PYTHON) -m $(MODULE)

clean:
	rm -rf __pycache__
	rm -rf $(MODULE)/__pycache__
	rm -rf dist
	rm -rf $(VENV)

$(VENV)/pyvenv.cfg: requirements.txt
	python -m venv --prompt $(MODULE) --upgrade-deps venv
	$(PIP) install -r requirements.txt
