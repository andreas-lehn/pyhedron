dist: setup.py readme.rst pyhedron/__init__.py Makefile LICENSE
	python setup.py sdist
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*

check:
	twine check dist/*
