# The most high-level and bootstrap tasks
# All tasks are specified in `tasks.py`

.PHONY: help install update test check release

help:
	@echo "See Makefile for available targets."

install:
	# NOTE: can't use invoke as it might not be installed yet
	pip install -r requirements.txt

update:
	pip install -r requirements.txt

test:
	invoke test

check:
	echo TBD

release:
	invoke release
