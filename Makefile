
# FIXME: calls to setup.py directly are now deprected, so I need to fix the --version usage
#	https://packaging.python.org/en/latest/guides/modernize-setup-py-project/

testdir := .

####

test:
	python3 -m unittest discover

demo:
	python3 demo-runner.py

pre-release-checks:
	pyroma .

####

tagged-commit: version != python3 setup.py --version
tagged-commit:
	git diff | grep '^+__version__'
	git add .
	git commit -m "Release $(version)"
	git tag -a -m "Release $(version)" "$(version)"
	@echo
	@echo "Now do a release, and then remember to push!"

release: export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release: pre-release-checks
	test '$(shell python3 setup.py --version)' = '$(shell git describe)'
	test ! -d dist
	pyproject-build
	check-wheel-contents dist
	twine check dist/*
	twine upload dist/*
	mv -i *.egg-info dist/.
	mv dist dist.$$(date +%Y-%m-%d.%H%M%S)

####

image-to-run += test-in-container-3.8-slim-bullseye
image-to-run += test-in-container-3.9-slim-bullseye
image-to-run += test-in-container-3.10-slim-bullseye
image-to-run += test-in-container-3.11-slim-bullseye
image-to-run += test-in-container-3.12-slim-bookworm
image-to-run += test-in-container-3.13-slim-bookworm
image-to-run += test-in-container-3.14-slim-trixie

test-in-container: $(image-to-run)
	@echo
	@echo "=============================================================="
	@echo "Successfully tested all versions with ephemerun:"
	@echo "$^" | tr ' ' '\n'
	@echo "=============================================================="
	@echo

test-in-container-%:
	@echo
	@echo "=============================================================="
	@echo "Testing with docker.io/library/python:$*"
	@echo "=============================================================="
	@echo
	ephemerun \
		-i "docker.io/library/python:$*" \
		-v "`pwd`:/root/src:ro" \
		-W "/root" \
		-S "cp -air ./src/* ." \
		-S "pip --no-cache-dir install ." \
		-S "python -m unittest discover $(testdir)" \
