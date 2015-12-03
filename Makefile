.PHONY: clean-pyc clean-build docs clean

PYTHON := python2.7

# ---------------------------------------------------------
#  
#  help
#
help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"


# ---------------------------------------------------------
#  
# clean
# 
clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

# ---------------------------------------------------------
#  
#  lint
#
flakes: lint
lint:
	pyflakes tsip/*.py tests/*.py


# ---------------------------------------------------------
#  
#  test
#
test: 
	nosetests -x -v tests/test_structs.py tests/test_llapi.py tests/test_hlapi.py

test_llapi:
	nosetests -x -v tests/$@.py

test_hlapi:
	nosetests -x -v tests/$@.py

tox: 
	tox


#coverage:
#	coverage run --source python-TSIP setup.py test
#	coverage report -m
#	coverage html
#	open htmlcov/index.html

docs:
#	rm -f docs/python-TSIP.rst
#	rm -f docs/modules.rst
#	sphinx-apidoc -o docs/ python-TSIP
#	$(MAKE) -C docs clean
#	$(MAKE) -C docs html
#	open docs/_build/html/index.html

.PHONY: sdist
sdist: 
	$(PYTHON) setup.py $@

.PHONY: bdist
bdist:
	$(PYTHON) setup.py $@

.PHONY: rpm
rpm:
	# native python version
	python setup.py bdist_rpm

.PHONY: wheel
wheel:
	$(PYTHON) setup.py bdist_wheel --universal

.PHONY: info
info:
	$(PYTHON) setup.py egg_info

.PHONY: build
build: 
	$(PYTHON) setup.py build

.PHONY:
upload: sdist bdist wheel
	twine upload dist/*

