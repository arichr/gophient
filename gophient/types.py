"""`gophient.types` - Types that implement the main logic."""
import socket
import urllib.parse
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Union

from gophient import const, exc

if TYPE_CHECKING:
    RequestType = Union[bytes, bytearray, str]
    ResponseType = Union[bytes, bytearray]


@dataclass
class Item:
    """Item of a server response."""

    _client: 'Gopher' = field(repr=False)
    raw_type: str = field(repr=False)
    """The item type. Possible values are `const.TYPES` keys."""
    pretty_type: str = field(hash=False, compare=False)
    """The human-readable item type. Possible values are `const.TYPES` values."""
    port: int = 70
    """The port of a server that this item is pointing to."""
    host: str = ''
    """The IP address or the domain name of a server that this item is pointing to."""
    path: str = ''
    """The path on a server that this item is pointing to."""
    desc: str = ''
    """The item description."""

    @classmethod
    def parse(cls, client: 'Gopher', raw: 'ResponseType') -> Union['Item', None]:
        """Parse a raw `ByteString`.

        Args:
            client (Gopher): Related client
            raw (ByteString): Data to parse

        Returns:
            Union[Item, None]
        """
        if raw == b'.' or raw == b'':
            return None  # Optional part of the specification

        try:
            encoded = raw.decode(client.encoding)
            parts = encoded[1:].split(const.SEPARATOR)
            if len(parts) < 4:
                # Received raw data
                raise ValueError
        except ValueError:  # UnicodeDecodeError is a subclass of ValueError
            return cls(client, '', const.TYPES.get('', 'Unknown'))

        return cls(
            _client=client,
            raw_type=encoded[0],
            pretty_type=const.TYPES.get(encoded[0], 'Unknown'),
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

    def follow(self) -> Union[List['Item'], bytes]:
        """Follow the link.

        Returns:
            A list of `Item` or a server response
        """
        return self._client.request(self.host, self.path, self.port, self._client.encoding)

    def __str__(self) -> str:
        """Return a string representation of `Item`.

        Returns:
            str
        """
        if self.raw_type == 'i':
            return self.desc
        if self.raw_type == '':
            return f'File {self.path} on {self.host}:{self.port}'

        return f'{self.desc} ({self.pretty_type}) - {self.path} on {self.host}:{self.port}'


class Gopher:
    """Gopher client."""

    def __init__(self, timeout: int = 10, encoding: str = 'utf-8'):
        """Initialize a client.

        Args:
            timeout (int): Socket timeout
            encoding (str): Packet encoding
        """
        self.timeout = timeout
        """Socket timeout. Defaults to `10`."""
        self.encoding = encoding
        """Packet encoding. Defaults to `'utf-8'`."""

    def _prepare_payload(self, path: str, query: 'RequestType') -> bytes:
        """Prepare a payload.

        Args:
            path (str): Path
            query (RequestType): Query

        Returns:
            Payload
        """
        enc_query = b''
        if query != '' and isinstance(query, str):
            enc_query = urllib.parse.quote(query, safe='').encode(self.encoding)

        return path.encode(self.encoding) + b'?' + enc_query + const.EOL

    def parse_response(self, resp: 'ResponseType') -> Union[List[Item], 'ResponseType']:
        """Parse the server response.

        Args:
            resp (ResponseType): Server response

        Returns:
            A list of `Item` (can be empty) or `resp`
        """
        pretty_resp = []
        for item in resp.split(const.EOL):
            item = Item.parse(self, item)
            if not item:
                continue

            if item.raw_type == '':
                # Received raw data
                return resp

            if item.raw_type == 'i' and pretty_resp:
                if pretty_resp[-1].raw_type == 'i':
                    pretty_resp[-1].merge_messages(item)
                    continue

            pretty_resp.append(item)

        return pretty_resp

    def request(
        self, host: str, path: str = '/', port: int = 70, query: 'RequestType' = '',
    ) -> Union[list[Item], bytes]:
        """Request an address.

        Args:
            host (str): Server domain or IP address
            path (str): Request path
            port (int): Server port
            query (RequestType): Query

        Returns:
            A list of `Item` (can be empty) or a server response
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with sock:
            socket.timeout(self.timeout)
            sock.connect((host, port))
            payload = self._prepare_payload(path, query)
            sock.sendall(payload)

            resp = bytes()
            packet = b'init'
            while packet:
                packet = sock.recv(1024)
                resp += packet

        return self.parse_response(resp)
