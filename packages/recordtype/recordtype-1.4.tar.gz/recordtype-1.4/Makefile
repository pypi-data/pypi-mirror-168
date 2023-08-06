test:
	py2/bin/python setup.py test
	py3/bin/python setup.py test

venv:
	python -m virtualenv py2
	py2/bin/pip install --upgrade pip
	python3 -m venv py3
	py3/bin/pip install --upgrade pip
	py3/bin/pip install wheel

setup:
	py2/bin/pip install -e .
	py3/bin/pip install -e .

clean:
	rm -rf py2 py3 dist build recordtype.egg-info *.pyc

black:
	~/venvs/global-py3-cygwin/bin/black *.py

build:
	py3/bin/python setup.py sdist bdist_wheel
