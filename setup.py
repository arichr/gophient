from setuptools import setup, find_packages

setup(
    name='gophient',
    version='0.2',
    url='https://github.com/arichr/gophient',
    license='MIT',
    author='Arisu W.',
    author_email='87308853+arichr@users.noreply.github.com',
    description='Python library to connect to Gopher servers',
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md').read(),
    zip_safe=False)
