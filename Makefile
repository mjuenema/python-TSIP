
.PHONY: clean-pyc clean-build docs clean

PYTHON := python3

# ---------------------------------------------------------
#  
#  help
#
help:
	@echo "clean         - remove all build, test, coverage and Python artifacts"
	@echo "clean-build   - remove build artifacts"
	@echo "clean-pyc     - remove Python file artifacts"
	@echo "clean-test    - remove test and coverage artifacts"
	@echo "test          - run tests quickly with the default Python"
	@echo "sdist          - package"


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
#  test
#
test: 
	nosetests -x -v tests/test_structs.py tests/test_llapi.py tests/test_hlapi.py

test_llapi:
	nosetests -x -v tests/$@.py

test_hlapi:
	nosetests -x -v tests/$@.py


.PHONY: sdist
sdist: 
	$(PYTHON) setup.py $@

.PHONY: wheel
wheel:
	$(PYTHON) setup.py bdist_wheel --universal

.PHONY: build
build: 
	$(PYTHON) setup.py build

.PHONY:
release: test clean sdist wheel
	twine upload dist/*

