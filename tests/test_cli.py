import tempfile
from unittest import mock
from pathlib import Path
from typer.testing import CliRunner

from ibroadcastdl.cli import app

runner = CliRunner()


def test_app_bad_args():
    """Test bad CLI invocation"""
    result = runner.invoke(app)
    assert result.exit_code == 2


@mock.patch("ibroadcastdl.cli.iBroadcastDL")
def test_app(mibdl):
    """Test normal CLI invocation"""
    mibdl.return_value.tracks = [
        "track 1",
        "track 2",
        "track 3",
        "track 4",
        "track 5",
        "track 6",
    ]

    with tempfile.TemporaryDirectory() as tmpd:
        metadata = Path(tmpd) / ".ibdl"
        metadata.write_text('{"total": 10, "offset": 10}')
        result = runner.invoke(app, ["-u", "test", "-p", "test", "-x", 5, tmpd])
    assert result.exit_code == 0
    mibdl.return_value.download_library.assert_not_called()


@mock.patch("ibroadcastdl.cli.iBroadcastDL")
def test_app_already_up_to_date(mibdl):
    """Test normal CLI invocation already sync"""
    mibdl.return_value.tracks = [
        "track 1",
        "track 2",
        "track 3",
        "track 4",
        "track 5",
        "track 6",
    ]

    with tempfile.TemporaryDirectory() as tmpd:

        result = runner.invoke(app, ["-u", "test", "-p", "test", "-x", 5, tmpd])
    assert result.exit_code == 0
