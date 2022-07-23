"""`pytest` testcases."""
from unittest import TestCase

import gophient  # pylint: disable=import-error


class GopherTest(TestCase):
    """Testcase for `gophient`."""

    def test_connectivity(self):
        """Test connectivity to servers."""
        client = gophient.Gopher()
        resp = client.request(['gopher.floodgap.com'])
        self.assertTrue(resp)

    def test_link_follow(self):
        """Test link following."""
        client = gophient.Gopher()
        resp = client.request(['gopher.floodgap.com'])
        # resp[0] may be an informational message.
        # But we are merging them, so resp[1] is always something else.
        new_resp = resp[1].follow()
        self.assertTrue(resp)
        self.assertNotEqual(resp, new_resp)

    def test_file_download(self):
        """Test file download."""
        client = gophient.Gopher()
        resp = client.request(['gopher.floodgap.com', 'proxy'])
        self.assertTrue(type(resp), bytearray)

    def test_items_type(self):
        """Test items type."""
        client = gophient.Gopher()
        resp = client.request(['gopher.floodgap.com'])
        self.assertEqual(resp[0].pretty_type, 'Informational message')

    def test_veronica_search(self):
        """Test Veronica search."""
        client = gophient.Gopher()
        resp = client.request(['gopher.floodgap.com', 'v2/vs'], query='cat')
        self.assertIn('?cat forward=', resp[-1].path)
