SHELL:=/bin/bash

env:
	python3 -m venv nenv && source ./nenv/bin/activate

clean:
	rm -rf ./nenv && \
	rm -rf dist/ && \
	rm -rf build/ && \
	rm -rf .pytest_cache/ && \
	rm -rf .hypothesis

format:
	black  --line-length 80 ./src

lint:
	pylint *py

test:
	pytest tests/unit_tests/*

integration-test:
	pytest tests/integration_tests/*
