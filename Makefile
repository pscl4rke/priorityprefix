

test:
	python3 -m unittest discover

demo:
	python3 demo-runner.py

pre-release-checks:
	pyroma .

release: export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release: pre-release-checks
	test '$(shell python3 setup.py --version)' = '$(shell git describe)'
	test ! -d dist
	python3 setup.py sdist bdist_wheel
	check-wheel-contents dist
	twine check dist/*
	twine upload dist/*
	mv -i build* *.egg-info dist/.
	mv dist dist.$$(date +%Y-%m-%d.%H%M%S)

####

image-to-run += test-in-container-3.6-slim-bullseye
image-to-run += test-in-container-3.7-slim-bullseye
image-to-run += test-in-container-3.8-slim-bullseye
image-to-run += test-in-container-3.9-slim-bullseye
image-to-run += test-in-container-3.10-slim-bullseye
image-to-run += test-in-container-3.11-slim-bullseye
image-to-run += test-in-container-3.12-slim-bookworm

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
		-S "python -m unittest discover ." \
