# Copyright (C) 2021  Arisu Wonderland

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import socket
import ssl
import urllib.parse


class GopherException:
    '''
    A parent class for all Gopher exceptions.
    '''
    class UnreachableHost(BaseException):
        '''
        Host is unreachable.
        '''
        def __init__(self, host):
            self.message = self.__doc__.strip() + \
                ' ({})'.format(host)
            super().__init__(self.message)

    class UnavailableNetwork(BaseException):
        '''
        Network connection is unavailable.
        '''
        def __init__(self):
            self.message = self.__doc__.strip()
            super().__init__(self.message)

    class SSLNotSupported(BaseException):
        '''
        SSL connection is not supported by the requested server.
        '''
        def __init__(self, host):
            self.message = self.__doc__.strip() + \
                ' ({})'.format(host)
            super().__init__(self.message)

    class UnexpectedResponse(BaseException):
        '''
        Unexpected response from the server.
        '''
        def __init__(self):
            self.message = self.__doc__.strip()
            super().__init__(self.message)

    class TypeMismatch(BaseException):
        '''
        Types mismatches.
        '''
        def __init__(self):
            self.message = self.__doc__.strip()
            super().__init__(self.message)


class Gopher:
    '''
    Client object. Have 3 constants:
        * EOL - CR LF
        * SEPARATOR - TAB
        * TYPES - Dict of various types of information
    '''
    EOL = '\r\n'
    SEPARATOR = '\t'
    TYPES = {
        # General (Gopher0)
        '0': 'Text file',
        '1': 'Sub-menu',
        '2': 'CCSO Nameserver',
        '3': 'Failure',
        '4': 'BinHex-encoded file',
        '5': 'DOS file',
        '6': 'uuencoded file',
        '7': 'Full-text search',
        '+': 'Mirror or alternate server',
        'g': 'GIF file',
        'I': 'Image file',
        'T': 'Telnet 3270',
        # Gopher+
        ':': 'Bitmap image',
        ';': 'Movie file',
        '<': 'Sound file',
        # etc.
        'd': 'Document file',
        'h': 'HTML file',
        'i': 'Informational message',
        's': 'Sound file'  # Especially WAV files
    }

    def __init__(self, timeout=10, ssl_version=None, ciphers=None):
        '''
        Initialize a client object.
        '''
        self.timeout = timeout
        if ssl_version:
            self.ssl_context = ssl.SSLContext(ssl_version)
            if ciphers:
                self.ssl_context.set_ciphers(ciphers)
        else:
            self.ssl_context = None

    class Item:
        '''
        An item of GopherMap
        '''
        def __init__(self, client, type, desc, path, host, port):
            '''
            Initialize an item of GopherMap.
            '''
            self.client = client
            self.desc = desc if desc != '(NULL)' else None
            self.path = path if path != '(NULL)' else None
            self.host = host if host != '(NULL)' else None
            self.port = int(port) if port != '(NULL)' else None
            self.raw_type = type
            try:
                self.type = Gopher.TYPES[self.raw_type]
            except KeyError:
                # Fallback to 'Informational message' if wasn't understood
                self.desc = self.raw_type + self.desc
                self.raw_type = 'i'
                self.type = Gopher.TYPES[self.raw_type]

        @property
        def url(self):
            if self.raw_type == 'h' and self.path.startswith('URL:'):
                return self.path[4:]

        def merge_messages(self, message):
            '''
            Merge two informational messages. Note, content will be appended to the first one.
            :param message: Informational message
            :type message: Gopher.Item
            '''
            if self.raw_type != 'i' or message.raw_type != 'i':
                raise GopherException.TypeMismatch

            self.desc += Gopher.EOL + message.desc

        def follow(self, encoding='utf-8'):
            '''
            Follow the link of the current item.
            :param encoding: Encoding of the server's responses. (Default: UTF-8)
            :return: bytearray or <Gopher.Item>s
            '''
            resp_parsed = self.client.request(self.path, self.host, self.port, encoding)
            return resp_parsed

        def __str__(self):
            if self.raw_type == 'i':
                return '{type}: {message}'.format(
                    type=self.type,
                    message=self.desc)
            elif self.url:
                return '{desc} (Redirect to {url})'.format(
                    desc=self.desc,
                    url=self.url)
            else:
                return '{desc} ({type}) - {path} on {host}:{port}'.format(
                    desc=self.desc,
                    type=self.type,
                    path=self.path,
                    host=self.host,
                    port=self.port)

        def __repr__(self):
            return '<Item type={} path={} host={} port={}>'.format(
                repr(self.type),
                repr(self.path),
                repr(self.host),
                repr(self.port))

    def _create_socket(self, host: str):
        '''
        Create a socket without SSL.
        :param host: Host IP or domain name.
        :return: socket.socket
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock

    def _create_secure_socket(self, host: str):
        '''
        Create a secure SSL socket.
        :param host: Host IP or domain name.
        :return: socket.socket
        '''
        sock = self._create_socket(host)
        ssock = self.ssl_context.wrap_socket(sock, server_hostname=host)
        return sock, ssock

    def _prepare_data(self, data: str, encoding='utf-8', inputs={}):
        if inputs:
            data += '?'
        for key in inputs:
            data += '{key}={val} '.format(key=key, val=inputs[key])

        urlenc_data = urllib.parse.quote(data, safe='')
        return bytes(urlenc_data + Gopher.EOL, encoding)

    def _send_request(self, sockets: tuple, data: str, host: str, port=70, encoding='utf-8', inputs={}):
        '''
        Make request to a server, but unlike other functions this one won't parse responses!
        :param sockets: List of opened sockets
        :param data: Data to be sended to the remote server. (Note: EOL adds automatically)
        :param host: Host IP or domain name.
        :param port: Port of the running server. (Default: 70)
        :param encoding: Encoding of server's responses. (Default: UTF-8)
        :param inputs: Dict of request input values. (Default: {})
        :return: bytearray
        '''
        sock = sockets[-1]
        try:
            sock.connect((host, port))
        except socket.gaierror:
            raise GopherException.UnavailableNetwork
        except ssl.SSLError:
            raise GopherException.SSLNotSupported(host)
        except (socket.timeout, ConnectionRefusedError):
            raise GopherException.UnreachableHost(host)

        urlenc_data = self._prepare_data(data, encoding, inputs)
        sock.sendall(urlenc_data)

        resp = bytearray()
        packet = True  # Socket bytes container
        while packet:
            try:
                packet = sock.recv(1024)
            except socket.timeout:
                raise GopherException.UnreachableHost(host)
            resp.extend(packet)

        for s in sockets:
            s.close()

        return resp

    def parse_resp(self, resp: bytearray, encoding='utf-8'):
        '''
        Parse response.
        :param encoding: Encoding of the server's responses.
        :return: bytearray or list of <Gopher.Item>s
        '''
        try:
            resp = resp.decode(encoding)
        except UnicodeDecodeError:
            return resp  # This is a binary file
        raw_items = resp.split(Gopher.EOL)

        items = []
        for i in raw_items:
            if not i or i == '.':  # EOF
                break

            parts = i.split(Gopher.SEPARATOR)

            if len(parts) != 4 and not items:
                return resp  # This is a binary file (or invalid response)

            content = parts[0]
            content_type = content[0]
            content_desc = content[1:]

            path = parts[1]

            host = parts[2]
            port = parts[3]

            item = Gopher.Item(self, content_type, content_desc, path, host, port)

            if item.raw_type == 'i' and items:
                if items[-1].raw_type == 'i':
                    items[-1].merge_messages(item)
                    continue

            items.append(item)

        return items

    def request(self, path: str, host: str, port=70, encoding='utf-8', inputs={}):
        '''
        Make request to a server.
        :param path: Path of a needed folder/file.
        :param host: Host IP or domain name.
        :param port: Port of the running server. (Default: 70)
        :param encoding: Encoding of server's responses. (Default: UTF-8)
        :param inputs: Dict of request input values. (Default: {})
        :return: bytearray or list of <Gopher.Item>s
        '''
        sockets = self._create_secure_socket(host) if self.ssl_context else (self._create_socket(host),)
        resp = self._send_request(sockets, path, host, port, encoding, inputs)
        parsed = self.parse_resp(resp, encoding)
        return parsed

    def get_root(self, host, port=70, encoding='utf-8'):
        '''
        Get root of a server.
        :param host: Host IP or domain name.
        :param port: Port of the running server. (Default: 70)
        :param encoding: Encoding of server's responses. (Default: UTF-8)
        :return: bytearray or list of <Gopher.Item>s
        '''
        return self.request('', host, port, encoding)
