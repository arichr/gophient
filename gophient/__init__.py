"""`gophient` - Python library to browse the Gopherspace.

Its code is separated into submodules:
 - `gophient.const` - Constant values like `SEPARATOR` or `TYPES`.
 - `gophient.exc`   - Exceptions that derive from `GopherError`.
 - `gophient.types` - This submodule contains everything you usually work with.
"""
from gophient import const, exc, types
from gophient.types import Gopher

__all__ = ('const', 'exc', 'types', 'Gopher')
