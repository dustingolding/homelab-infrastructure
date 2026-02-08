.PHONY: docs docs-check

docs:
	python3 scripts/gen-namespace-docs.py

docs-check:
	python3 scripts/gen-namespace-docs.py --check
