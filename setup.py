"""Setup file for gophient."""
from pathlib import Path

from setuptools import setup

here = Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='gophient',
    version='1.1.0',
    description='Client library for the Gopherspace',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/arichr/gophient',
    author='Arisu W.',
    author_email='arisuchr@riseup.net',
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    keywords='gopher, gophient, client, python3, gopher-client, gopherspace, module, library',
    packages=['gophient'],
    python_requires='>=3.8, <4',
)
