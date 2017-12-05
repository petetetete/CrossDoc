# Contributing

This repository is the source and documentation for a capstone project, so external pull requests will not be accepted. Internally, pull requests will not be required but may be helpful for large or impactful commits.


## Getting Started

Firstly, clone the repository: `git clone https://github.com/petetetete/CrossDoc.git`

Then, to run the program, navigate your shell to the `src` directory, and run the following command:

`python -m cdoc.__main__`


## Code Formatting

To ensure our codebase remains tidy and consistent, we will be follwoing [PEP8 guidelines](https://www.python.org/dev/peps/pep-0008/), with some minor modifications.

Specifically, we will not be using the following rules because they enforce a 4 space tab, while we will be using 2.:

* E111
* E114
* E121

One easy way to ensure this, is to use a linter for your editor of choice. For example, Sublime Text 3's [Anaconda](http://damnwidget.github.io/anaconda/IDE/) implements this, and can be customized with the following settings to match our standards:

```
{
    "pep8": true,
    "pep8_ignore": [
        "E111", "E114", "E121"
    ]
}
```


## Package Updating

Steps to creating and uploading a Pip update:

* Tag release: `git tag <x.y.z> -m <message>`
* Push tag: `git push --tags`
* Setup distributions: `python setup.py sdist`
* Upload to pypi.org: `twine upload dist/*`
    * Upload to test.pypi.org: `twine upload --repository testpypi dist/*`

These steps assume that a .pypirc has already been setup that matches the following pattern:

```
[distutils]
index-servers =
  pypi
  testpypi

[pypi]
username=<username>
password=<password>

[testpypi]
repository=https://test.pypi.org/legacy/
username=<username>
password=<password>
```
