<<<<<<< HEAD
<<<<<<< HEAD
# Python template
![repo style: chr](https://img.shields.io/badge/repo%20style-chr-blueviolet?logo=github&style=flat-square)

Python template for various projects.

This branch (`minimal`) is kept minimal as possible. To stay updated with my latest changes use the `arichr` branch.

## For which projects..?
This template was built upon these statements:
 * You target Python `>=3.8, <4.0`
 * You use `google` style for docstrings ([pylint on PyPi](https://pypi.org/project/pylint/))
 * You use [flake8](https://pypi.org/project/flake8/) with [wemake-python-styleguide](https://pypi.org/project/wemake-python-styleguide/)
 * You commit LF line endings (see [.pylintrc](https://github.com/arichr/python-template/blob/main/.pylintrc#L28) and [.gitattributes](https://github.com/arichr/python-template/blob/main/.gitattributes))
 * You always document your code (see [.pylintrc](https://github.com/arichr/python-template/blob/main/.pylintrc#L23))
 * 79 symbols per line is enough for you (see [.pylintrc](https://github.com/arichr/python-template/blob/main/.pylintrc#L34))

## What should I do next?
I think, you should:
 * Add a license
 * Initialize Git on your local machine
 * Make a great README
 * Initialize [poetry](https://pypi.org/project/poetry/)
 * Use [codecov](https://pypi.org/project/codecov/)

You may also want to do this:
 * Create `Dockerfile` (and `docker-compose.yml`)
 * Create `requirements.txt` for users without installed Poetry
 * Start working with [Portray](https://pypi.org/project/portray/) / [MkDocs](https://pypi.org/project/mkdocs/) / [Sphinx](https://pypi.org/project/Sphinx/) / etc.

## Publishing / Deploying
 * Configure CI/CD to lint, test and check your code
 * Configure CI/CD to generate wheels as artifacts and/or publish them on PyPi

## Links
### Linting:
 * [flake8 documentation](https://flake8.pycqa.org/en/latest/index.html)
 * [Google guidelines](https://google.github.io/styleguide/pyguide.html)
 * [pylint documentation](https://pylint.pycqa.org/en/latest/index.html)
 * [Google .pylintrc](https://google.github.io/styleguide/pylintrc)
### Documentation
 * [MkDocs](https://www.mkdocs.org/)
 * [Sphinx documentation](https://www.sphinx-doc.org/en/master/index.html)
 * [Portray](https://timothycrosley.github.io/portray/)
### Packaging
 * [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

## Contribute!
I really appreciate any contributions to my repositories! If you know some tools, libraries that are not listed here feel free to create an issue and a PR.
=======
# gophient
Gopher library for Python
>>>>>>> 1d5518b (Initial commit)
=======
# Gophient
![Downloads counter](https://shields.io/github/downloads/arichr/gophient/total?style=flat-square)
![Stars counter](https://shields.io/github/stars/arichr/gophient?style=flat-square)
![Latest release version](https://img.shields.io/github/v/tag/arichr/gophient?label=latest&style=flat-square)
![License](https://shields.io/github/license/arichr/gophient?style=flat-square)

Gophient is a library, that adds Gopher support for Python. You can browse the Gopherspace, follow links, download content by writing less code for your application.
# Dependencies
None! All library, that were used, are already a part of Python.
# Examples
## Get weather from Floodgap Gopher
```python
import gophient

client = gophient.Gopher()
weather = client.request('groundhog/ws', 'gopher.floodgap.com')
print(weather)
```
## Search by using Veronica
```python
import gophient

client = gophient.Gopher()
results = client.request('v2/vs', 'gopher.floodgap.com', 
  inputs={'q': 'plan 9'})
print(results)
```
## Download files from Gopher
```python
import gophient

client = gophient.Gopher()
apk = client.request('overbite/files/OverbiteAndroid025.apk', 'gopher.floodgap.com')
with open('app.apk', 'wb') as apk_file:
  apk_file.write(apk)
```
# License
Licensed by MIT.
>>>>>>> fbb9fd9 (Update README.md)
