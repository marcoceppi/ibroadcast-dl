# pylint: disable=invalid-name
"""iBroadcastDL Module"""
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from urllib.parse import urlunsplit, urlencode

import ibroadcast
import requests

SCHEME = "https"
DOMAIN = "download.ibroadcast.com"


def build_url(path: str, query: dict | None = None) -> str:
    """Create a string URL from URLPARTS"""
    query = urlencode(query) if query else ""
    return urlunsplit((SCHEME, DOMAIN, path, query, ""))


class iBroadcastDL(ibroadcast.iBroadcast):
    """iBroadcast Class extension with Download functionality"""

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

        archive = ZipFile(BytesIO(resp.content))
        archive.extractall(dest)
        return resp.headers.get("Response-Count", None)
