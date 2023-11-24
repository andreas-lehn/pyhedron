dist: setup.py readme.rst pyhedron/__init__.py Makefile
	python setup.py sdist
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*