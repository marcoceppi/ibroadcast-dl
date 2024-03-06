# pylint: disable=invalid-name
"""iBroadcastDL Module"""
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from urllib.parse import urlunsplit, urlencode
from importlib.metadata import version as pkgversion

import ibroadcast
import requests

from ibroadcastdl.exceptions import IncompleteDownload


SCHEME = "https"
DOMAIN = "download.ibroadcast.com"


def build_url(path: str, query: dict | None = None) -> str:
    """Create a string URL from URLPARTS"""
    query = urlencode(query) if query else ""
    return urlunsplit((SCHEME, DOMAIN, path, query, ""))


class iBroadcastDL(ibroadcast.iBroadcast):
    """iBroadcast Class extension with Download functionality"""

    def __init__(
        self,
        username,
        password,
        log=None,
        client="ibroadcast-python",
        version=None,
    ):
        """Initiate a client and login"""
        version = version or pkgversion("ibroadcast-dl")
        super().__init__(username, password, log, client, version)

    def download_library(
        self, offset: int = 0, length: int = 1, dest: Path | None = None
    ) -> int | None:
        """Download Library"""
        query = {
            "user_id": self.user_id(),
            "token": self.token(),
            "offset": offset,
            "length": length,
            "container_type": "library",
            "mode": "downloadlibrary",
            "end_marker": 1,
        }
        resp = requests.get(build_url("/", query))
        if not resp.content.endswith(b"EOF\n"):
            raise IncompleteDownload("download interrupted")

        archive = ZipFile(BytesIO(resp.content.removesuffix(b"EOF\n")))
        archive.extractall(dest)
        return resp.headers.get("Response-Count", None)
