# High-level tasks

FLAGS=$(CURDIR)/.flags

release:  # (dependencies? -- because of invoke)
	invoke version_remove_dev_flag
	#TBA: git tags
	#TBA: invoke version_increase --level micro
	#TBA: python setup.py sdist upload

tag:
	echo "TODO: invoke increase version"

dependencies: $(FLAGS)/dependencies
$(FLAGS)/dependencies: $(FLAGS) requirements.txt
	pip install -r requirements.txt
	touch .flags/dependencies

$(FLAGS):
	mkdir $(FLAGS)

.PHONY: release tag dependencies
