

test:
	python3 -m unittest discover

test-all:
	for version in 3.6-slim-bullseye 3.7-slim-bullseye 3.8-slim-bullseye \
				   3.9-slim-bullseye 3.10-slim-bullseye ;\
	do \
		echo ; echo $$version ; echo ;\
		docker build --file Dockerfile.test --build-arg IMAGE="python:$$version" . ;\
	done

demo:
	python3 demo-runner.py

export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release:
	test ! -d dist
	python3 setup.py sdist
	ls -l dist
	twine upload dist/*
	mv *egg-info -i dist
	mv dist dist.$$(date +%Y%m%d.%H%M%S)
