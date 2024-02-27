import pytest
from ibroadcastdl import dl


class _iBroadcastDLDummy(dl.iBroadcastDL):
    def _login(self, username, password):
        self.status = {"user": {"token": "dummy", "id": "dummy"}}


@pytest.fixture()
def iBroadcastDLDummy():
    return _iBroadcastDLDummy
