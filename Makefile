# The most high-level and bootstrap tasks
# All tasks are specified in `tasks.py`

.PHONY: help install update test lint release tasks

help:
	@echo "See Makefile for available targets."

install:
	# NOTE: can't use invoke as it might not be installed yet
	pip install -r requirements.txt

update:
	pip install -r requirements.txt

test:
	invoke test

lint:
	pylint ./flocs

release:
	invoke release

tasks:
	invoke build_tasks
