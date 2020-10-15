.PHONY: format
format:
		yapf

.PHONY: pylint
pylint:
		pylint ./**/*.py

.PHONY: mypy
mypy:
		mypy --ignore-missing-imports .
