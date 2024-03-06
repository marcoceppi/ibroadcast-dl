class iBroadcastDlError(Exception):
    """Base exception for iBroadcastDl library"""


class IncompleteDownload(iBroadcastDlError):
    """Partial or incomplete file downloaded"""
