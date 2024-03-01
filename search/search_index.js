var __index = {"config":{"lang":["en"],"separator":"[\\s\\-]+","pipeline":["stopWordFilter"]},"docs":[{"location":"index.html","title":"Home","text":"<p> Gophient <p> </p> <p>Python library to browse the Gopherspace</p> <p> </p> </p> <p>Features:</p> <ul> <li>Light</li> <li>Easy to use</li> <li>Comes without dependencies</li> </ul>"},{"location":"index.html#getting-started","title":"Getting started","text":"<ol> <li>Install Gophient: <pre><code>pip install gophient\n</code></pre></li> <li>Create a <code>gophient.Gopher</code> instance and make requests (see examples below)</li> </ol>"},{"location":"index.html#examples","title":"Examples","text":""},{"location":"index.html#get-weather-from-floodgap","title":"Get weather from Floodgap","text":"<pre><code>import gophient\n\nclient = gophient.Gopher()\nweather = client.request('gopher.floodgap.com', 'groundhog/ws')\nprint(weather)\n</code></pre>"},{"location":"index.html#search-on-veronica","title":"Search on Veronica","text":"<pre><code>import gophient\n\nclient = gophient.Gopher()\nresults = client.request('gopher.floodgap.com', 'v2/vs', query='plan 9')\nprint(results)\n</code></pre>"},{"location":"index.html#download-files","title":"Download files","text":"<pre><code>import gophient\n\nclient = gophient.Gopher()\napk = client.request('gopher.floodgap.com', 'overbite/files/OverbiteAndroid025.apk')\nwith open('app.apk', 'wb') as apk_file:\n  apk_file.write(apk)\n</code></pre>"},{"location":"1_-_Installation.html","title":"Installation","text":"<p>You can use Poetry to install Gophient into your current environment:</p> <pre><code>$ poetry add gophient\n</code></pre> <p>Alternatively, you can still use Pip:</p> <pre><code>$ pip install gophient\n</code></pre>"},{"location":"1_-_Installation.html#unstable-versions","title":"Unstable versions","text":"<p>Python wheels are built on every successful commit on <code>main</code> or <code>dev</code>. You can find artifacts here.</p>"},{"location":"2_-_Getting_started.html","title":"Getting started","text":"<p>To start using <code>gophient</code> import it and create a <code>gophient.Gopher</code> instance:</p> <pre><code>import gophient\n\nclient = gophient.Gopher()\n</code></pre> <p>For a full definition of the API see the API reference documentation.</p>"},{"location":"api.html","title":"API Reference","text":"<p><code>gophient</code> - Python library to browse the Gopherspace.</p> Its code is separated into submodules <ul> <li><code>gophient.const</code> - Constant values like <code>SEPARATOR</code> or <code>TYPES</code>.</li> <li><code>gophient.exc</code>   - Exceptions that derive from <code>GopherError</code>.</li> <li><code>gophient.types</code> - This submodule contains everything you usually work with.</li> </ul>"},{"location":"api.html#gophient.types","title":"types","text":"<p><code>gophient.types</code> - Types that implement the main logic.</p>"},{"location":"api.html#gophient.types.RequestType","title":"RequestType  <code>module-attribute</code>","text":"<pre><code>RequestType = Union[bytes, bytearray, str]\n</code></pre>"},{"location":"api.html#gophient.types.ResponseType","title":"ResponseType  <code>module-attribute</code>","text":"<pre><code>ResponseType = Union[bytes, bytearray]\n</code></pre>"},{"location":"api.html#gophient.types.Gopher","title":"Gopher","text":"<pre><code>Gopher(timeout=10, encoding='utf-8')\n</code></pre> <p>Gopher client.</p> <p>Initialize a client.</p> <p>Parameters:</p> Name Type Description Default <code>timeout</code> <code>int</code> <p>Socket timeout</p> <code>10</code> <code>encoding</code> <code>str</code> <p>Packet encoding</p> <code>'utf-8'</code> Source code in <code>gophient/types.py</code> <pre><code>def __init__(self, timeout: int = 10, encoding: str = 'utf-8'):\n    \"\"\"Initialize a client.\n\n    Args:\n        timeout (int): Socket timeout\n        encoding (str): Packet encoding\n    \"\"\"\n    self.timeout = timeout\n    \"\"\"Socket timeout. Defaults to `10`.\"\"\"\n    self.encoding = encoding\n    \"\"\"Packet encoding. Defaults to `'utf-8'`.\"\"\"\n</code></pre>"},{"location":"api.html#gophient.types.Gopher.encoding","title":"encoding  <code>instance-attribute</code>","text":"<pre><code>encoding = encoding\n</code></pre> <p>Packet encoding. Defaults to <code>'utf-8'</code>.</p>"},{"location":"api.html#gophient.types.Gopher.timeout","title":"timeout  <code>instance-attribute</code>","text":"<pre><code>timeout = timeout\n</code></pre> <p>Socket timeout. Defaults to <code>10</code>.</p>"},{"location":"api.html#gophient.types.Gopher.parse_response","title":"parse_response","text":"<pre><code>parse_response(resp)\n</code></pre> <p>Parse the server response.</p> <p>Parameters:</p> Name Type Description Default <code>resp</code> <code>ResponseType</code> <p>Server response</p> required <p>Returns:</p> Type Description <code>Union[List[Item], ResponseType]</code> <p>A list of <code>Item</code> (can be empty) or <code>resp</code></p> Source code in <code>gophient/types.py</code> <pre><code>def parse_response(self, resp: 'ResponseType') -&gt; Union[List[Item], 'ResponseType']:\n    \"\"\"Parse the server response.\n\n    Args:\n        resp (ResponseType): Server response\n\n    Returns:\n        A list of `Item` (can be empty) or `resp`\n    \"\"\"\n    pretty_resp = []\n    for item in resp.split(const.EOL):\n        item = Item.parse(self, item)\n        if not item:\n            continue\n\n        if item.raw_type == '':\n            # Received raw data\n            return resp\n\n        if item.raw_type == 'i' and pretty_resp:\n            if pretty_resp[-1].raw_type == 'i':\n                pretty_resp[-1].merge_messages(item)\n                continue\n\n        pretty_resp.append(item)\n\n    return pretty_resp\n</code></pre>"},{"location":"api.html#gophient.types.Gopher.request","title":"request","text":"<pre><code>request(host, path='/', port=70, query='')\n</code></pre> <p>Request an address.</p> <p>Parameters:</p> Name Type Description Default <code>host</code> <code>str</code> <p>Server domain or IP address</p> required <code>path</code> <code>str</code> <p>Request path</p> <code>'/'</code> <code>port</code> <code>int</code> <p>Server port</p> <code>70</code> <code>query</code> <code>RequestType</code> <p>Query</p> <code>''</code> <p>Returns:</p> Type Description <code>Union[list[Item], bytes]</code> <p>A list of <code>Item</code> (can be empty) or a server response</p> Source code in <code>gophient/types.py</code> <pre><code>def request(\n    self, host: str, path: str = '/', port: int = 70, query: 'RequestType' = '',\n) -&gt; Union[list[Item], bytes]:\n    \"\"\"Request an address.\n\n    Args:\n        host (str): Server domain or IP address\n        path (str): Request path\n        port (int): Server port\n        query (RequestType): Query\n\n    Returns:\n        A list of `Item` (can be empty) or a server response\n    \"\"\"\n    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    with sock:\n        socket.timeout(self.timeout)\n        sock.connect((host, port))\n        payload = self._prepare_payload(path, query)\n        sock.sendall(payload)\n\n        resp = bytes()\n        packet = b'init'\n        while packet:\n            packet = sock.recv(1024)\n            resp += packet\n\n    return self.parse_response(resp)\n</code></pre>"},{"location":"api.html#gophient.types.Item","title":"Item  <code>dataclass</code>","text":"<p>Item of a server response.</p>"},{"location":"api.html#gophient.types.Item.desc","title":"desc  <code>class-attribute</code> <code>instance-attribute</code>","text":"<pre><code>desc = ''\n</code></pre> <p>The item description.</p>"},{"location":"api.html#gophient.types.Item.host","title":"host  <code>class-attribute</code> <code>instance-attribute</code>","text":"<pre><code>host = ''\n</code></pre> <p>The IP address or the domain name of a server that this item is pointing to.</p>"},{"location":"api.html#gophient.types.Item.path","title":"path  <code>class-attribute</code> <code>instance-attribute</code>","text":"<pre><code>path = ''\n</code></pre> <p>The path on a server that this item is pointing to.</p>"},{"location":"api.html#gophient.types.Item.port","title":"port  <code>class-attribute</code> <code>instance-attribute</code>","text":"<pre><code>port = 70\n</code></pre> <p>The port of a server that this item is pointing to.</p>"},{"location":"api.html#gophient.types.Item.pretty_type","title":"pretty_type  <code>class-attribute</code> <code>instance-attribute</code>","text":"<pre><code>pretty_type = field(hash=False, compare=False)\n</code></pre> <p>The human-readable item type. Possible values are <code>const.TYPES</code> values.</p>"},{"location":"api.html#gophient.types.Item.raw_type","title":"raw_type  <code>class-attribute</code> <code>instance-attribute</code>","text":"<pre><code>raw_type = field(repr=False)\n</code></pre> <p>The item type. Possible values are <code>const.TYPES</code> keys.</p>"},{"location":"api.html#gophient.types.Item.__str__","title":"__str__","text":"<pre><code>__str__()\n</code></pre> <p>Return a string representation of <code>Item</code>.</p> <p>Returns:</p> Type Description <code>str</code> <p>str</p> Source code in <code>gophient/types.py</code> <pre><code>def __str__(self) -&gt; str:\n    \"\"\"Return a string representation of `Item`.\n\n    Returns:\n        str\n    \"\"\"\n    if self.raw_type == 'i':\n        return self.desc\n    if self.raw_type == '':\n        return f'File {self.path} on {self.host}:{self.port}'\n\n    return f'{self.desc} ({self.pretty_type}) - {self.path} on {self.host}:{self.port}'\n</code></pre>"},{"location":"api.html#gophient.types.Item.follow","title":"follow","text":"<pre><code>follow()\n</code></pre> <p>Follow the link.</p> <p>Returns:</p> Type Description <code>Union[List[Item], bytes]</code> <p>A list of <code>Item</code> or a server response</p> Source code in <code>gophient/types.py</code> <pre><code>def follow(self) -&gt; Union[List['Item'], bytes]:\n    \"\"\"Follow the link.\n\n    Returns:\n        A list of `Item` or a server response\n    \"\"\"\n    return self._client.request(self.host, self.path, self.port, self._client.encoding)\n</code></pre>"},{"location":"api.html#gophient.types.Item.merge_messages","title":"merge_messages","text":"<pre><code>merge_messages(item)\n</code></pre> <p>Merge two informational messages.</p> <p>Parameters:</p> Name Type Description Default <code>item</code> <code>Item</code> <p>Item</p> required <p>Raises:</p> Type Description <code>TypeMismatchError</code> <p>Can't merge items with wrong types</p> Source code in <code>gophient/types.py</code> <pre><code>def merge_messages(self, item: 'Item') -&gt; None:\n    \"\"\"Merge two informational messages.\n\n    Args:\n        item (Item): Item\n\n    Raises:\n        TypeMismatchError: Can't merge items with wrong types\n    \"\"\"\n    if self.raw_type == 'i' and item.raw_type == 'i':\n        self.desc += const.EOL.decode(self._client.encoding) + item.desc\n    else:\n        raise exc.TypeMismatchError(item.pretty_type, self.pretty_type)\n</code></pre>"},{"location":"api.html#gophient.types.Item.parse","title":"parse  <code>classmethod</code>","text":"<pre><code>parse(client, raw)\n</code></pre> <p>Parse a raw <code>ByteString</code>.</p> <p>Parameters:</p> Name Type Description Default <code>client</code> <code>Gopher</code> <p>Related client</p> required <code>raw</code> <code>ByteString</code> <p>Data to parse</p> required <p>Returns:</p> Type Description <code>Union[Item, None]</code> <p>Union[Item, None]</p> Source code in <code>gophient/types.py</code> <pre><code>@classmethod\ndef parse(cls, client: 'Gopher', raw: 'ResponseType') -&gt; Union['Item', None]:\n    \"\"\"Parse a raw `ByteString`.\n\n    Args:\n        client (Gopher): Related client\n        raw (ByteString): Data to parse\n\n    Returns:\n        Union[Item, None]\n    \"\"\"\n    if raw == b'.' or raw == b'':\n        return None  # Optional part of the specification\n\n    try:\n        encoded = raw.decode(client.encoding)\n        parts = encoded[1:].split(const.SEPARATOR)\n        if len(parts) &lt; 4:\n            # Received raw data\n            raise ValueError\n    except ValueError:  # UnicodeDecodeError is a subclass of ValueError\n        return cls(client, '', const.TYPES.get('', 'Unknown'))\n\n    return cls(\n        _client=client,\n        raw_type=encoded[0],\n        pretty_type=const.TYPES.get(encoded[0], 'Unknown'),\n        desc=parts[0],\n        path=parts[1],\n        host=parts[2],\n        port=int(parts[3]),\n    )\n</code></pre>"},{"location":"api.html#gophient.exc","title":"exc","text":"<p><code>gophient.exc</code> - Client exceptions.</p>"},{"location":"api.html#gophient.exc.GopherError","title":"GopherError","text":"<p>             Bases: <code>Exception</code></p> <p>Base exception for <code>gophient</code>.</p>"},{"location":"api.html#gophient.exc.TypeMismatchError","title":"TypeMismatchError","text":"<pre><code>TypeMismatchError(got, expected)\n</code></pre> <p>             Bases: <code>GopherError</code></p> <p>Items' types mismatch.</p> <p>Initialize an exception.</p> <p>Parameters:</p> Name Type Description Default <code>got</code> <code>str</code> <p>Item type</p> required <code>expected</code> <code>str</code> <p>Expected type</p> required Source code in <code>gophient/exc.py</code> <pre><code>def __init__(self, got: str, expected: str):\n    \"\"\"Initialize an exception.\n\n    Args:\n        got (str): Item type\n        expected (str): Expected type\n    \"\"\"\n    super().__init__()\n    self.got = got\n    self.expected = expected\n    self.message = f'Expected {self.expected!r} (got {self.got!r}).'\n</code></pre>"},{"location":"api.html#gophient.exc.TypeMismatchError.expected","title":"expected  <code>instance-attribute</code>","text":"<pre><code>expected = expected\n</code></pre>"},{"location":"api.html#gophient.exc.TypeMismatchError.got","title":"got  <code>instance-attribute</code>","text":"<pre><code>got = got\n</code></pre>"},{"location":"api.html#gophient.exc.TypeMismatchError.message","title":"message  <code>instance-attribute</code>","text":"<pre><code>message = f'Expected {expected} (got {got}).'\n</code></pre>"},{"location":"api.html#gophient.exc.TypeMismatchError.__repr__","title":"__repr__","text":"<pre><code>__repr__()\n</code></pre> <p>Return an object representation.</p> <p>Returns:</p> Type Description <code>str</code> <p>str</p> Source code in <code>gophient/exc.py</code> <pre><code>def __repr__(self) -&gt; str:\n    \"\"\"Return an object representation.\n\n    Returns:\n        str\n    \"\"\"\n    return f'&lt;TypeMismatchError message={self.message!r}&gt;'\n</code></pre>"},{"location":"api.html#gophient.exc.TypeMismatchError.__str__","title":"__str__","text":"<pre><code>__str__()\n</code></pre> <p>Return a string representation of an exception.</p> <p>Returns:</p> Type Description <code>str</code> <p>str</p> Source code in <code>gophient/exc.py</code> <pre><code>def __str__(self) -&gt; str:\n    \"\"\"Return a string representation of an exception.\n\n    Returns:\n        str\n    \"\"\"\n    return self.message\n</code></pre>"}]}