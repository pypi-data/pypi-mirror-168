
**flit_pytest_circleci_template** is a sample project to show how to use:
* [flit](https://github.com/pypa/flit) to build a python package, configured in pyproject.toml
* [pytest](https://docs.pytest.org/) to test a python package, configured in pyproject.toml
* [circleci](https://circleci.com/) for to build  the python package, test it, and publish to [pypi](https://pypi.org/) automatically.

# Getting Ready
To proceed with your own package and publishing to pypi:
* copy the .circleci folder to your project and add to your git repo.  Currently it has only one file config.yml that configures the build pipeline for a python project.  Here is the [.circleci/config.yml](.circleci/config.yml)  and [pyproject.toml](./pyproject.toml) for this project.
* Create the pyproject.toml as normally required to build your package with flit.  Include in test dependencies pytest and any other python packages that need to be installed for testing:
```
[project.optional-dependencies]
test = [
    "pytest >=7.1.2",
]
```
* Add testpaths to [tool.pytest.ini_options] identifying where your tests are located.  Specifying minversion and addopts is also recommended:
```
[tool.pytest.ini_options]
minversion = "7.1.2"
addopts = "--capture=tee-sys "

testpaths= [
    "test",
]
```

When you are satisifed with your tests, review the config.yml and see if there are any obvious changes you require.  You may not need any but you might elect 
to update to the latest [python orb](https://circleci.com/developer/orbs?query=circleci%2Fpython) or specific [python image](https://circleci.com/developer/images/image/cimg/python) you would like to use to build and test your python package.

The publish step will normally fail if there is already a package in  [pypi](https://pypi.org/) with the same version number.  Which is desired behavior.
When you are ready to publish, increase the version number (in pyproject.toml or __init__.py depending on how the project is set up.).

** You can elect to publish to [testpypi](https://test.pypi.org/) by tweaking the twine command in config.yml **

# Configure [circleci](https://circleci.com/)

Create a [circleci](https://circleci.com/) account if you don't have one and add your  github repository as a project. Get the build at least running.

Using Project Settings, add Environment variables  ```TWINE_USERNAME``` and ```TWINE_PASSWORD```.  These are the credentials you use to publish to [pypi](https://pypi.org/) or [testpypi](https://test.pypi.org/).  Until you set those variables, the publish stop obviously will fail, but the package build and test steps should work.




# License

You can do whatever you want with the code in this repository and apply whatever license you want to copies or modifications in your own project. This project is mean to be a helpful starting point for people who want to get circleci to build and publish python packages. 

