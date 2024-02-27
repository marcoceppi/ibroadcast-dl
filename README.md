# iBroadcast Download / Sync

This project was born from a need to download my library from iBroadcast onto my linux machine. Only the OSX and Windows app support this functionality. This project uses the existing [ibroadcast-python](https://pypi.org/project/ibroadcast/) library and extends the `iBroadcast` class to add a `download_library` method.

In addition to using this as a Python library, it also has a small CLI to help automate doing library downloads.

# Usage

This project can be used as both a Python library and CLI.

## CLI

### Installation

#### pipx

pipx is available for Linux, OSX, and Windows. Follow the [install instructions first for pipx](https://pipx.pypa.io/stable/installation/) then the following:

```
pipx install ibroadcast-dl
```

### Usage

To use the CLI, run the `ibroadcast-dl` command:

```sh
ibroadcast-dl --username ibroadcast@email.tld ~/Music/
```

This will open a progress bar - if your library is large it'll take several hours to sync. If you connection is slow try turing down the number of tracks it downloads at a time (defaults 50) to something around 10:

```sh
ibroadcast-dl -u ibroadcast@email.tld -x 10 ~/Music/
```

## Python Library

The module has the same method sigrnatures and usage as the [`ibroadcast-python`]() library with the addition of a `download_library` method.

```python
>>> import ibroadcastdl
>>> ib = ibroadcastdl.iBroadcastDL("email", "password")
>>> download_dir = "./Music"
>>> offset = 0
>>> while offset < len(ib.tracks):
...     ib.download_library(offset, 50, download_dir)
...     offset = offset + 50
```

This will download the entire library 50 tracks at a time.
