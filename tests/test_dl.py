"""Test ibroadcastdl.dl module"""

from unittest import mock
from zipfile import ZipFile

import pytest

from ibroadcastdl import dl
from ibroadcastdl.exceptions import IncompleteDownload


def test_build_url():
    """test build_url returns a correctly formatted url"""
    assert (
        dl.build_url("/test/foo", {"hello": "world"})
        == "https://download.ibroadcast.com/test/foo?hello=world"
    )

    assert dl.build_url("/", None) == "https://download.ibroadcast.com/"


@mock.patch("ibroadcastdl.dl.ZipFile")
@mock.patch("requests.get")
def test_ibroadcastdl_download_library(m_req, m_zipfile, iBroadcastDLDummy):
    """test iBroadcastDL.download_library makes the correct request"""
    archive: ZipFile = m_zipfile.return_value
    m_req.return_value.content = b"not-an-archiveEOF\n"
    ibdl = iBroadcastDLDummy("test", "test")
    ibdl.download_library(offset=10, length=10, dest="/foo/bar")
    m_req.assert_called_with(
        "https://download.ibroadcast.com/?user_id=dummy&token=dummy&offset=10&length=10&container_type=library&mode=downloadlibrary&end_marker=1"
    )
    archive.extractall.assert_called_with("/foo/bar")


@mock.patch("requests.get")
def test_ibroadcastdl_download_library_incomplete(m_req, iBroadcastDLDummy):
    """test iBroadcastDL.download_library detects incomplete download"""
    m_req.return_value.content = b"not-an-archive"
    ibdl = iBroadcastDLDummy("test", "test")
    with pytest.raises(IncompleteDownload):
        ibdl.download_library(offset=10, length=10, dest="/foo/bar")
