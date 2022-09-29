"""Tests for gophient."""
import gophient  # pylint: disable=import-error


def test_connectivity():
    """Test connectivity to servers."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com')
    assert resp


def test_link_follow():
    """Test link following."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com')
    # resp[0] can be an informational message, but since we combine
    # the first of them, resp[1] is always something else.
    new_resp = resp[1].follow()
    assert resp and resp != new_resp


def test_file_download():
    """Test file download."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com', 'recent')
    assert isinstance(resp, bytearray)


def test_items_type():
    """Test items type."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com')
    assert resp[0].pretty_type == 'Informational message'


def test_veronica_search():
    """Test Veronica search."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com', 'v2/vs', query='cat')
    assert '?cat forward=' in resp[-1].path
