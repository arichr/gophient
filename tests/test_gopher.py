"""Tests for gophient."""
import gophient


def test_connectivity():
    """Test connectivity to servers."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com')
    assert resp


def test_link_following():
    """Test link following."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com')
    # We combine informational messages if they are placed together.
    # In that case resp[1] is guranteed to be a link.
    new_resp = resp[1].follow()
    assert resp and new_resp and resp != new_resp


def test_file_downloading():
    """Test file downloading."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com', 'recent')
    assert isinstance(resp, bytearray)


def test_items_type():
    """Test items' type."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com')
    assert resp[0].pretty_type == 'Informational message'


def test_searching():
    """Test searching on Veronica."""
    client = gophient.Gopher()
    resp = client.request('gopher.floodgap.com', 'v2/vs', query='cat')
    assert '?cat forward=' in resp[-1].path
