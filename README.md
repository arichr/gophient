# Gophient
[![repo style: chr](https://img.shields.io/badge/repo%20style-chr-blueviolet?logo=github&style=flat)](https://github.com/arichr/python-template)
[![PyPI](https://img.shields.io/pypi/v/gophient?style=flat&logo=python&logoColor=white)](https://pypi.org/project/gophient/)
[![Maintainability](https://api.codeclimate.com/v1/badges/d83cf869ea9fa8d05a6f/maintainability)](https://codeclimate.com/github/arichr/gophient/maintainability)
![Vulnerabilities](https://img.shields.io/snyk/vulnerabilities/github/arichr/yakusubot?style=flat&logo=snyk)

Gophient is client library for the Gopherspace. It doesn't require any dependencies and is easy to use.

[![Read documentation](https://img.shields.io/badge/read-documentation-green?style=for-the-badge&logo=python&logoColor=white)](https://arichr.github.io/gophient/)

## Features
 * Browse the Gopherspace
 * Follow links
 * Download content

## Examples
### Get weather from Floodgap
```python
import gophient

client = gophient.Gopher()
weather = client.request('gopher.floodgap.com', 'groundhog/ws')
print(weather)
```
### Search by Veronica
```python
import gophient

client = gophient.Gopher()
results = client.request('gopher.floodgap.com', 'v2/vs', query='plan 9')
print(results)
```
### Download files
```python
import gophient

client = gophient.Gopher()
apk = client.request('gopher.floodgap.com', 'overbite/files/OverbiteAndroid025.apk')
with open('app.apk', 'wb') as apk_file:
  apk_file.write(apk)
```
