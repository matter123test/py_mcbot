from InquirerPy.resolver import prompt
from InquirerPy.base.control import Choice
from papermc import *
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.console import Console
import os
import json

### Globals
DEFAULT_SERVER_FOLDER = "server"
if not os.path.exists(DEFAULT_SERVER_FOLDER):
    os.mkdir(DEFAULT_SERVER_FOLDER)

DEFAULT_SERVER_FILENAME = "server.jar"
DEFAULT_SERVER_FILE_PATH = os.path.join(DEFAULT_SERVER_FOLDER, DEFAULT_SERVER_FILENAME)
DEFAULT_SERVER_CONFIG = os.path.join(DEFAULT_SERVER_FOLDER, "config.json")


### Prompts
supported_versions = get_supported_versions()

version_choices = [
    Choice(value=index, name=item.id) for (index, item) in enumerate(supported_versions)
]

question = [
    {
        "type": "rawlist",
        "name": "version_idx",
        "message": "Select a paper mc version:",
        "choices": version_choices,
    }
]

result = prompt(question)
version_index = result["version_idx"]

version = supported_versions[version_index]  # type: ignore

### Save flags
from dataclasses import asdict

json.dump(asdict(version), open(DEFAULT_SERVER_CONFIG, "w", encoding="utf-8"))

latest_build = get_latest_build_download(version)


def download(url: str, total_size: int, out: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad status codes (404, 500, etc.)

    progress = Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None),  # None makes it scale to fill the terminal width
        "[progress.percentage]{task.percentage:>3.0f}%",
        "•",
        DownloadColumn(),  # Shows "Megabytes / Total Megabytes"
        "•",
        TransferSpeedColumn(),  # Shows "MB/s"
        "•",
        TimeRemainingColumn(),  # Shows "ETA"
    )

    with progress:
        download_task = progress.add_task("Downloading", total=total_size)

        chunk_size = 1024 * 64  # 64 KB chunks
        with open(out, "wb") as dest_file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    dest_file.write(chunk)
                    # Update the progress bar by the number of bytes just written
                    progress.update(download_task, advance=len(chunk))


download(latest_build.url, latest_build.total_size, DEFAULT_SERVER_FILE_PATH)


### Server config
import subprocess

server_jar = os.path.join(DEFAULT_SERVER_FILE_PATH)

os.chdir(DEFAULT_SERVER_FOLDER)

console = Console()
with console.status("[bold green]Configuring server...") as status:
    process = subprocess.run(["java", "-jar", DEFAULT_SERVER_FILENAME, "nogui"])
