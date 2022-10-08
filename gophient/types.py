"""gophient.types - Types for gophient."""
import socket
import urllib.parse
from dataclasses import dataclass, field
from typing import ByteString, List, Union

from gophient import const, exc


@dataclass
class Item:
    """Line of a server response."""

    raw_type: str = field(compare=False, repr=False)
    pretty_type: str = field(compare=False)
    port: int = 70
    host: str = ''
    path: str = ''
    desc: str = ''
    _client: 'Gopher' = None

    @classmethod
    def parse(cls, client: 'Gopher', raw: ByteString) -> Union['Item', None]:
        """Parse a raw `ByteString`.

        Args:
            client (Gopher): Related client
            raw (ByteString): Data to parse

        Returns:
            Union[Item, None]
        """
        if raw in (b'.', b''):
            return None  # Optional part of the specification

        try:
            raw = raw.decode(client.encoding)
            parts = raw[1:].split(const.SEPARATOR)
            if len(parts) < 4:
                raise ValueError('The server returned a file or a broken response.')
        except ValueError:
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

    def merge_messages(self, item: 'Item') -> None:
        """Merge two informational messages.

        Args:
            item (Item): Item

        Raises:
            TypeMismatchError: Can't merge items with wrong types
        """
        if self.raw_type == 'i' and item.raw_type == 'i':
            self.desc += const.EOL.decode(self._client.encoding) + item.desc
        else:
            raise exc.TypeMismatchError(item.pretty_type, self.pretty_type)

    def follow(self) -> Union[List['Item'], list, ByteString]:
        """Follow the link.

        Returns:
            Union[List[Item], list, ByteString]
        """
        return self._client.request(self.host, self.path, self.port, self._client.encoding)

    def __str__(self) -> str:
        """Return a string representation of the Item.

        Returns:
            str
        """
        if self.raw_type == 'i':
            return self.desc

        if self.raw_type == 'ꬰ':
            return f'File ({self.path} on {self.host}:{self.port})'

        return f'{self.desc} ({self.pretty_type}) - {self.path} on {self.host}:{self.port}'


class Gopher:
    """Class for Gopher client."""

    def __init__(self, timeout: int = 10, encoding: str = 'utf-8'):
        """Initialize a client.

        Args:
            timeout (int): Socket timeout
            encoding (str): Encoding for packets. Defaults to `'utf-8'`
        """
        self.timeout = timeout
        self.encoding = encoding

    def _open_socket(self) -> socket.socket:
        """Open a `socket.socket`.

        Returns:
            socket.socket
        """
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _prepare_payload(self, path: str, query: Union[str, ByteString, None] = None) -> bytes:
        """Prepare a payload.

        Args:
            path (str): Path
            query (Union[str, ByteString, None]): Query. Defaults to `None`.

        Returns:
            bytes
        """
        if isinstance(query, str):
            query = bytes(urllib.parse.quote(query, safe=''), self.encoding)
        elif query is None:
            query = b''

        path = bytes(path, self.encoding)
        return b''.join((path, b'?', query, const.EOL))

    def parse_response(self, resp: ByteString) -> Union[List[Item], list, ByteString]:
        """Parse the server response.

        Args:
            resp (ByteString): Response

        Returns:
            Union[List[Item], list, ByteString]
        """
        pretty_resp = []
        for item in resp.split(const.EOL):
            item = Item.parse(self, item)
            if not item:
                continue

            if item.raw_type == 'ꬰ':
                return resp

            if item.raw_type == 'i' and pretty_resp:
                if pretty_resp[-1].raw_type == 'i':
                    pretty_resp[-1].merge_messages(item)
                    continue

            pretty_resp.append(item)

        return pretty_resp

    def request(
        self,
        host: str,
        path: str = '/',
        port: int = 70,
        query: Union[str, ByteString, None] = None,
    ) -> Union[List[Item], list, ByteString]:
        """Request an address.

        Args:
            host (str): Host to connect to
            path (str): Path. Defaults to `'/'`
            port (int): Port
            query (Union[str, ByteString, None]): Query

        Returns:
            Union[List[Item], list, ByteString]
        """
        sock = self._open_socket()
        with sock:
            socket.timeout(self.timeout)
            sock.connect((host, port))
            payload = self._prepare_payload(path, query)
            sock.sendall(payload)

            resp = bytearray()
            packet = b'packet'
            while packet:
                packet = sock.recv(1024)
                resp.extend(packet)

        return self.parse_response(resp)
