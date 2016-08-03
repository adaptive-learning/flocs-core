# The most high-level tasks

FLAGS=$(CURDIR)/.flags

dependencies: $(FLAGS)/dependencies
$(FLAGS)/dependencies: $(FLAGS) requirements.txt
	pip install -r requirements.txt
	touch .flags/dependencies

$(FLAGS):
	mkdir $(FLAGS)

.PHONY: release tag dependencies
