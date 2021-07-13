import ssl
from unittest import TestCase
from gophient import Gopher, GopherException


class GopherTest(TestCase):
    def runTest(self):
        print('Connection test')
        self.test_connection()
        print('Following links test')
        self.test_follow_links()
        print('Veronica test')
        self.test_veronica()
        print('Raw file (APK) download test')
        self.test_raw_file_download()

    def test_connection(self):
        client = Gopher()

        host = 'gopher.floodgap.com'
        resp = client.get_root(host)

        self.assertEqual(list, type(resp))

    def test_follow_links(self):
        client = Gopher()

        host = 'gopher.quux.org'
        root_resp = client.get_root(host)

        # We combine informational messages at the start,
        # so the second element is not a message for sure.
        item = root_resp[1]
        item_resp = item.follow()

        self.assertEqual(True, (root_resp != item_resp))

    def test_veronica(self):
        # Veronica is a search engine in Gopher
        client = Gopher()

        host = 'gopher.floodgap.com'
        resp = client.request('/v2/vs', host, inputs={'q': 'plan 9'})

        stmt1 = list == type(resp)
        stmt2 = len(resp) > 1

        self.assertEqual(True, (stmt1 and stmt2))

    def test_raw_file_download(self):
        client = Gopher()

        apk = client.request('overbite/files/OverbiteAndroid025.apk', 'gopher.floodgap.com')
        try:
            apk.decode('utf-8')
            error = None
        except UnicodeDecodeError as e:
            error = e

        self.assertEqual(UnicodeDecodeError, type(error))

    def test_fail_ssl_connection(self):
        client = Gopher()
        client.ssl_context = ssl.create_default_context()

        try:
            host = 'gopher.rp.spb.su'
            client.get_root(host)
            error = None
        except GopherException.SSLNotSupported as e:
            error = e

        self.assertEqual(GopherException.SSLNotSupported, type(error))
