from setuptools import setup, find_packages

setup(
    name='gophient',
    version='1.0.0',
    url='https://github.com/arichr/gophient',
    license='MIT',
    author='Arisu W.',
    author_email='arisuchr@riseup.net',
    description='Python library for connection to Gopher servers',
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md').read(),
    zip_safe=False,
)
