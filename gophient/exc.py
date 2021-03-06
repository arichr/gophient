"""Exceptions for gophient."""

class GopherException(Exception):
    """Main class for all `gophient` exceptions."""

class TypeMismatch(GopherException):
    """Items' types mismatch."""

    def __init__(self, got: str, expected: str):
        """Initialize an exception.

        Args:
            got (str): Item type
            expected (str): Expected type
        """
        super().__init__()
        self.got = got
        self.expected = expected
        self.message = f'Expected {self.expected!r} (got {self.got!r}).'

    def __str__(self) -> str:
        """Return a string representation of an exception.

        Returns:
            str
        """
        return self.message

    def __repr__(self) -> str:
        """Return an object representation.

        Returns:
            str
        """
        return f'<TypeMismatch message={self.message!r}>'
