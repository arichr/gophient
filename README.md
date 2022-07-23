# Gophient
[![repo style: chr](https://img.shields.io/badge/repo%20style-chr-blueviolet?logo=github&style=flat-square)](https://github.com/arichr/python-template)
![License](https://shields.io/github/license/arichr/gophient?style=flat-square)
![Downloads counter](https://shields.io/github/downloads/arichr/gophient/total?style=flat-square)
![Stars counter](https://shields.io/github/stars/arichr/gophient?style=flat-square)

Gophient is a library for connecting to Gopher servers. By using it you can:
 * Browse the Gopherspace
 * Follow links
 * Download content

## Features
 * Light
 * Easy to use
 * No dependecies

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

## License
Licensed by MIT.
