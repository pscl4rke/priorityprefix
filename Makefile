

test:
	python3 -m unittest discover

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
