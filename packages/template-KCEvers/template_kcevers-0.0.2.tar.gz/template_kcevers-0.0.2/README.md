# Template for building a Python package

Mark all directories as "Sources Root".

> py -m pip install --upgrade pip
> python -m pip install --upgrade pip-tools

### Use pipreqs to make a requirements.txt file based on all packages in environment
> pipreqs /path/to/package
> pipreqs --force # To overwrite existing requirements.txt file

### Use piptools to make a requirements.txt file based on dependencies specified in setup.py/setup.cfg/pyproject.toml (https://github.com/jazzband/pip-tools)
> python -m pip install pip-tools
> pip-compile -o requirements.txt pyproject.toml

To update, run:
> pip-compile --output-file=requirements.txt pyproject.toml


### Install the package in editable mode (no need to activate the virtual environment in Pycharm, https://setuptools.pypa.io/en/latest/userguide/development_mode.html) 
> cd packaging_tutorial
> pip install -e . # or equivalently, --editable rather than -e

## Publish on Pypi
For full instructions, follow https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/.

- Build source distribution and wheel (better than running "python setup.py sdist bdist_wheel"); 
> py -m pip install --upgrade build
> python -m build

- Before trying to upload your distribution, you should check to see if your brief / long descriptions provided in setup.py are valid. You can do this by running twine check on your package files:
> py -m pip install --upgrade twine
> twine check dist/*

- It's also highly recommended to
- first upload your package on TestPyPi (https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-your-project-to-pypi):
> py -m twine upload --repository testpypi dist/*

- Check whether the installation worked
> py -m pip install --index-url https://test.pypi.org/simple/ --no-deps template_KCEvers

- Upload distribution to PyPi
> twine upload dist/*
