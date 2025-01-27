

test:
	python3 -m unittest discover

demo:
	python3 demo-runner.py

export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release: pyversion != python3 setup.py --version
release: gitversion != git describe --tags
release: pre-release-checks
	@echo 'Py version:  $(pyversion)'
	@echo 'Git version: $(gitversion)'
	test '$(pyversion)' = '$(gitversion)'
	test ! -d dist
	python3 setup.py sdist bdist_wheel
	check-wheel-contents dist
	twine check dist/*
	twine upload dist/*
	mv build* *egg-info -i dist
	mv dist dist.$$(date +%Y-%m-%d.%H%M%S)

pre-release-checks:
	pyroma .

####

docker-to-run += test-in-docker-3.6-slim-bullseye
docker-to-run += test-in-docker-3.7-slim-bullseye
docker-to-run += test-in-docker-3.8-slim-bullseye
docker-to-run += test-in-docker-3.9-slim-bullseye
docker-to-run += test-in-docker-3.10-slim-bullseye
docker-to-run += test-in-docker-3.11-slim-bullseye
docker-to-run += test-in-docker-3.12-slim-bookworm
test-in-docker: $(docker-to-run)

test-in-docker-%:
	@echo
	@echo "===================================================="
	@echo "Testing with docker.io/library/python:$*"
	@echo "===================================================="
	@echo
	ephemerun \
		-i "docker.io/library/python:$*" \
		-v "`pwd`:/root/src:ro" \
		-W "/root" \
		-S "cp -air ./src/* ." \
		-S "pip --no-cache-dir install ." \
		-S "python -m unittest discover ." \
