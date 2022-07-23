"""gophient.types - Types for gophient."""
import socket
import urllib.parse
from typing import ByteString
from dataclasses import dataclass

from gophient import const


@dataclass
class Item:
    """Line of a server response."""

    _client: object = None
    raw_type: str = ''
    pretty_type: str = ''
    desc: str = ''
    url: str = ''
    host: str = ''
    port: int = 70

    @classmethod
    def parse(cls, client: object, raw: ByteString, encoding: str = 'utf-8') -> object | None:
        """Parse a raw `ByteString`.

        Args:
            client (Gopher): Related client
            raw (ByteString): Data to parse
            encoding (str): Server encoding

        Returns:
            Item | None
        """
        if raw in (b'.', b''):
            return None  # Optional part of the specification

        try:
            raw = raw.decode(encoding)
            parts = raw[1:].split(const.SEPARATOR)
            if len(parts) < 4:
                raise ValueError('Broken response or a file.')
        except (UnicodeDecodeError, ValueError):
            return cls(
                raw_type='ꬰ',  # Broken type to distinguish "unparsable" items
                pretty_type=const.TYPES.get('ꬰ', 'Unknown'),
            )

        return cls(
            _client=client,
            raw_type=raw[0],
            pretty_type=const.TYPES.get(raw[0], 'Unknown'),
            desc=parts[0],
            url=parts[1],
            host=parts[2],
            port=int(parts[3]),
        )

    def merge_messages(self, item: object, encoding: str = 'utf-8') -> None:
        """Merge two informational messages.

        Args:
            item (Item): Item
            encoding (str): Encoding for CRLF sequence
        """
        if self.raw_type == 'i' and item.raw_type == 'i':
            self.desc += const.EOL.decode(encoding) + item.desc
        else:
            raise ...  # TODO:


    def follow(self, encoding: str = 'utf-8') -> list[object] | list | ByteString:
        """Follow the link.

        Args:
            encoding (str): Request encoding

        Returns:
            list[Item] | list | ByteString
        """
        return self._client.request(self.host, self.url, self.port, encoding)


    def __str__(self) -> str:
        """Return a string representation of the Item.

        Returns:
            str
        """
        if self.raw_type == 'i':
            return self.desc
        elif self.raw_type == 'ꬰ':
            return 'File'
        else:
            return (
                f'{self.desc} ({self.pretty_type}) - '
                f'{self.url} on {self.host}:{self.port}'
            )


class Gopher:
    """Class for Gopher client."""

    def __init__(self, timeout: int = 10):
        """Initialize a client.

        Args:
            timeout (int): Socket timeout
        """
        self.timeout = timeout

    def _open_socket(self) -> socket.socket:
        """Open a `socket.socket`.

        Returns:
            socket.socket
        """
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _prepare_payload(
        self,
        url: str,
        query: str | ByteString | None = None,
        encoding: str = 'utf-8',
    ) -> bytes:
        """Prepare a payload.

        Args:
            url (str): URL
            query (str | ByteString | None): Query
            encoding (str): encoding

        Returns:
            bytes
        """
        if isinstance(query, str):
            query = bytes(urllib.parse.quote(query, safe=''), encoding)
        elif query is None:
            query = b''

        url = bytes(url, encoding)
        return b''.join((url, b'?', query, const.EOL))

    def _parse_response(self, resp: ByteString, encoding: str = 'utf-8') -> list[Item] | list | ByteString:
        """Parse the server response.

        Args:
            resp (ByteString): Response
            encoding (str): Server encoding

        Returns:
            list[Item] | list | ByteString
        """
        pretty_resp = []
        for item in resp.split(const.EOL):
            item = Item.parse(self, item, encoding)
            if not item:
                continue
            elif item.raw_type == 'ꬰ':
                return resp
            elif item.raw_type == 'i' and pretty_resp:
                if pretty_resp[-1].raw_type == 'i':
                    pretty_resp[-1].merge_messages(item, encoding)
                    continue
            pretty_resp.append(item)

        return pretty_resp

    def request(
        self,
        host: str,
        url: str = '/',
        port: int = 70,
        query: str | ByteString | None = None,
        encoding: str = 'utf-8',
    ) -> list[Item] | list | ByteString:
        """Request an address.

        Args:
            host (str): Host
            url (str): URL
            port (int): Port
            query (str | ByteString | None): Query

        Returns:
            list[Item] | list | ByteString
        """
        sock = self._open_socket()
        with sock:
            socket.timeout(self.timeout)
            sock.connect((host, port))
            payload = self._prepare_payload(url, query, encoding)
            sock.sendall(payload)

            resp = bytearray()
            packet = b'packet'
            while packet:
                packet = sock.recv(1024)
                resp.extend(packet)

        return self._parse_response(resp)
