<p align="center">
    <h1 align="center">Gophient</h1>
    <p align="center">
    <a href="https://pypi.org/project/gophient/"><img alt="PyPI" src="https://img.shields.io/pypi/v/gophient?style=flat&logo=python&logoColor=white"></a>
    <a href="https://codeclimate.com/github/arichr/gophient/maintainability"><img alt="Maintainability" src="https://api.codeclimate.com/v1/badges/d83cf869ea9fa8d05a6f/maintainability"></a>
</p>
    <p align="center">Python library to browse the Gopherspace</p>
    <p align="center">
        <a href="https://arichr.github.io/gophient/"><img alt="Read documentation" src="https://img.shields.io/badge/read-documentation-green?style=for-the-badge&logo=python&logoColor=white"></a>
    </p>
</p>

**Features:**

* Light
* Easy to use
* Comes without dependencies

## Getting started

1. Install Gophient:
```console
pip install gophient
```
2. Create a `gophient.Gopher` instance and make requests ([see examples below](#examples))

## Examples

### Get weather from Floodgap

```python
import gophient

client = gophient.Gopher()
weather = client.request('gopher.floodgap.com', 'groundhog/ws')
print(weather)
```

### Search on Veronica

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
