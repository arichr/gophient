# Gophient
![Downloads counter](https://shields.io/github/downloads/arichr/gophient/total?style=flat-square)
![Stars counter](https://shields.io/github/stars/arichr/gophient?style=flat-square)
![License](https://shields.io/github/license/arichr/gophient?style=flat-square)

Gophient is a library, that adds Gopher support for Python. You can browse the Gopherspace, follow links, download content by writing less code for your application.
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
