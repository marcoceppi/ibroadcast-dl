"""CLI module"""

import json
from pathlib import Path
from importlib.metadata import version

import typer
from rich.progress import (
    Progress,
    MofNCompleteColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    SpinnerColumn,
)
from typing_extensions import Annotated

from ibroadcastdl.dl import iBroadcastDL
from ibroadcastdl.exceptions import IncompleteDownload


app = typer.Typer(rich_markup_mode="rich")


@app.command(
    epilog=f"Version {version('ibroadcast-dl')}. Made with :star2: [link=https://github.com/marcoceppi/ibroadcast-dl]github.com/marcoceppi/ibroadcast-dl[/link]"
)
def download(
    username: Annotated[
        str,
        typer.Option(
            "-u", "--username", envvar="IBROADCAST_USERNAME", help="iBroadcast Username"
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "-p",
            "--password",
            prompt=True,
            hide_input=True,
            envvar="IBROADCAST_PASSWORD",
            help="iBroadcast Password",
        ),
    ],
    parallel: Annotated[int, typer.Option("--parallel", "-x", min=1, max=50)] = 50,
    metadata_file: Annotated[
        Path,
        typer.Option(
            "--metadata-file", "-m", help="Path to store iBroadcast-DL metadata"
        ),
    ] = ".ibdl",
    output: Annotated[Path, typer.Argument(help="Download files to")] = Path.cwd(),
):
    """Download iBroadcast Library"""
    output.mkdir(parents=True, exist_ok=True)
    metadata_file = output / metadata_file
    metadata = {"offset": 0, "total": 0}
    if metadata_file.exists():
        metadata = json.load(metadata_file.open())

    ib = iBroadcastDL(username, password)
    if len(ib.tracks) <= metadata["total"]:
        print("Already up to date")
        raise typer.Exit()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
    ) as progress:
        task = progress.add_task("Downloading...", total=len(ib.tracks))
        progress.update(task, completed=metadata["offset"])
        while not progress.finished:
            try:
                ib.download_library(metadata["offset"], parallel, output)
            except IncompleteDownload:
                print("Incomplete download detected, retrying...")
                continue
            metadata["offset"] += parallel
            metadata_file.write_text(json.dumps(metadata, indent=2))
            progress.update(task, advance=parallel)

        metadata["total"] = len(ib.tracks)
        metadata_file.write_text(json.dumps(metadata, indent=2))
