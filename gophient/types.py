"""gophient.types - Types for gophient."""
from __future__ import annotations
import socket
import urllib.parse
from typing import ByteString, Union
from dataclasses import dataclass

from gophient import const, exc


@dataclass
class Item:
    """Line of a server response."""

    _client: 'Gopher' = None
    raw_type: str = ''
    pretty_type: str = ''
    desc: str = ''
    path: str = ''
    host: str = ''
    port: int = 70

    @classmethod
    def parse(cls, client: Item, raw: ByteString, encoding: str = 'utf-8') -> Union[Item, None]:
        """Parse a raw `ByteString`.

        Args:
            client (Gopher): Related client
            raw (ByteString): Data to parse
            encoding (str): Server encoding

        Returns:
            Union[Item, None]
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
            path=parts[1],
            host=parts[2],
            port=int(parts[3]),
        )

    def merge_messages(self, item: Item, encoding: str = 'utf-8') -> None:
        """Merge two informational messages.

        Args:
            item (Item): Item
            encoding (str): Encoding for CRLF sequence
        """
        if self.raw_type == 'i' and item.raw_type == 'i':
            self.desc += const.EOL.decode(encoding) + item.desc
        else:
            raise exc.TypeMismatch(item.pretty_type, self.pretty_type)


    def follow(self, encoding: str = 'utf-8') -> Union[list[Item], list, ByteString]:
        """Follow the link.

        Args:
            encoding (str): Request encoding

        Returns:
            Union[list[Item], list, ByteString]
        """
        return self._client.request((self.host, self.path), self.port, encoding)


    def __str__(self) -> str:
        """Return a string representation of the Item.

        Returns:
            str
        """
        if self.raw_type == 'i':
            return self.desc

        if self.raw_type == 'ꬰ':
            return 'File'

        return (
            f'{self.desc} ({self.pretty_type}) - '
            f'{self.path} on {self.host}:{self.port}'
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
        path: str,
        query: Union[str, ByteString, None] = None,
        encoding: str = 'utf-8',
    ) -> bytes:
        """Prepare a payload.

        Args:
            path (str): Path
            query (Union[str, ByteString, None]): Query
            encoding (str): encoding

        Returns:
            bytes
        """
        if isinstance(query, str):
            query = bytes(urllib.parse.quote(query, safe=''), encoding)
        elif query is None:
            query = b''

        path = bytes(path, encoding)
        return b''.join((path, b'?', query, const.EOL))

    def parse_response(self, resp: ByteString, encoding: str = 'utf-8') -> Union[list[Item], list, ByteString]:
        """Parse the server response.

        Args:
            resp (ByteString): Response
            encoding (str): Server encoding

        Returns:
            Union[list[Item], list, ByteString]
        """
        pretty_resp = []
        for item in resp.split(const.EOL):
            item = Item.parse(self, item, encoding)
            if not item:
                continue

            if item.raw_type == 'ꬰ':
                return resp

            if item.raw_type == 'i' and pretty_resp:
                if pretty_resp[-1].raw_type == 'i':
                    pretty_resp[-1].merge_messages(item, encoding)
                    continue

            pretty_resp.append(item)

        return pretty_resp

    def request(
        self,
        url: tuple[str, str],
        port: int = 70,
        query: Union[str, ByteString, None] = None,
        encoding: str = 'utf-8',
    ) -> Union[list[Item], list, ByteString]:
        """Request an address.

        Args:
            url (tuple[str, str]): Tuple of a host and a path
            port (int): Port
            query (Union[str, ByteString, None]): Query

        Returns:
            Union[list[Item], list, ByteString]
        """
        if len(url) > 1:
            host, path = url
        else:
            host, path = url[0], '/'

        sock = self._open_socket()
        with sock:
            socket.timeout(self.timeout)
            sock.connect((host, port))
            payload = self._prepare_payload(path, query, encoding)
            sock.sendall(payload)

            resp = bytearray()
            packet = b'packet'
            while packet:
                packet = sock.recv(1024)
                resp.extend(packet)

        return self.parse_response(resp)
