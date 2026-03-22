
.PHONY: clean-pyc clean-build docs clean

PYTHON := python3
# It's named nosetests3 in python3-nose=1.3.7-8 Ubuntu package.
NOSETEST != type nosetests3 >/dev/null 2>&1 && echo nosetests3 || echo nosetests

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
	$(NOSETEST) -x -v tests/test_*.py

test_llapi:
	$(NOSETEST) -x -v tests/$@.py

test_hlapi:
	$(NOSETEST) -x -v tests/$@.py


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

