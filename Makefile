.PHONY: format
format:
	yapf

.PHONY: lint
lint: pylint mypy

.PHONY: pylint
pylint:
	pylint ./**/*.py

.PHONY: mypy
mypy:
	mypy --ignore-missing-imports .

.PHONY: package
package:
	pakaman

.PHONY: test
test:
	tox