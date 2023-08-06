.PHONY: test create-cp clean-pyc release dist install clean



clean-pyc: ## remove Python file artifacts
	python scripts/clean_pyc.py


clean: clean-pyc
	python scripts/clean_build.py

test:
	cls
	pytest -v __tests 


create-cp: 
	python component_create\main.py

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel

install: clean ## install the package to the active Python's site-packages
	python setup.py install

	