import requests
from rich.progress import TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, Progress
from rich.console import Console


def download_with_progress(url: str, out_filename: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # 1. Get the total file size from headers (returns None if not present)
    total_size = response.headers.get('content-length')
    if total_size is not None:
        total_size = int(total_size)

    progress = Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.0f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    )

    with progress:
        # 2. Pass the total size to the task
        download_task = progress.add_task("Downloading", total=total_size)

        chunk_size = 1024 * 64  # 64 KB chunks
        with open(out_filename, "wb") as dest_file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    dest_file.write(chunk)
                    progress.update(download_task, advance=len(chunk))


def download_with_spinner(url: str, out_filename: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    console = Console()

    with console.status("[bold blue]Downloading server.jar...") as status:
        chunk_size = 1024 * 64  # 64 KB chunks
        with open(out_filename, "wb") as dest_file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    dest_file.write(chunk)
