import os

import subprocess
from rich import print
from InquirerPy import prompt
from rich.console import Console

from setup import downloader
from setup.api import LoaderAPI
from setup.api.loaders.fabricmc import FabricMC
from setup.api.loaders.papermc import PaperMC

D_SERVER_FOLDER_PATH = 'test'
D_SERVER_FILENAME = 'server.jar'


def main():
    loader_question = prompt({
        "type": "list",
        "name": "loader",
        "message": "Select a loader:",
        "choices": ["PaperMC", "Fabric"],
    })
    loader_choice = loader_question["loader"]

    loader: LoaderAPI
    if loader_choice == "PaperMC":
        loader = PaperMC()
    elif loader_choice == "Fabric":
        loader = FabricMC()
    else:
        return

    game_versions = loader.get_supported_versions()

    game_version_question = prompt({
        "type": "list",
        "name": "game_version",
        "message": "Select a game version:",
        "choices": game_versions
    })
    game_version_choice = game_version_question["game_version"]

    print(f"Loader: [bold blue]{loader_choice}[/bold blue] Game: {game_version_choice}")

    download_url = loader.get_latest_build_download_url(game_version_choice)

    if not os.path.exists(D_SERVER_FOLDER_PATH):
        os.mkdir(D_SERVER_FOLDER_PATH)

    out_file_path = os.path.join(D_SERVER_FOLDER_PATH, D_SERVER_FILENAME)

    # Because fabric doesn't have a content-length
    if loader_choice == "PaperMC":
        downloader.download_with_progress(download_url, out_file_path)
    else:
        downloader.download_with_spinner(download_url, out_file_path)

    print(f"[bold green]Downloaded {out_file_path}!")

    os.chdir(D_SERVER_FOLDER_PATH)
    console = Console()
    with console.status("[bold green]Configuring server...") as status:
        subprocess.run(
            ["java", "-jar", D_SERVER_FILENAME, "nogui"],
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

    print("[bold green]Complete!")
