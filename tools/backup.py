import os.path
import shutil
import datetime

from rich.console import Console

console = Console()

from argparse import ArgumentParser


def main():
    parser = ArgumentParser(
        prog="Backup tool", description="Creates backups from world folder"
    )

    parser.add_argument("-n", "--name", help="name of the output file", default=None)
    parser.add_argument(
        "-f",
        "--backup_folder",
        help="specify the output backups folder",
        default="backups",
    )
    parser.add_argument(
        "-w",
        "--world-folder",
        help="specify where the world folder is located",
        default="server/world",
    )

    args = parser.parse_args()

    archive_name = args.name
    if archive_name is None:
        archive_name = get_archive_name(args.backup_folder)
    else:
        archive_name = os.path.join(args.backup_folder, archive_name)

    with console.status("[bold yellow]Creating backup..."):
        make_backup(
            archive_name=archive_name,
            backups_folder=args.backup_folder,
            world_folder=args.world_folder,
        )

    console.print(f"[bold green]Created backup at {archive_name}")


def get_archive_name(backups_folder: str) -> str:
    now = datetime.datetime.now()

    # Example output: "backup_2026-06-06_17-00"
    return now.strftime(f"{backups_folder}/backup_%Y-%m-%d_%H-%M")


def make_backup(archive_name: str, backups_folder: str, world_folder: str):
    if not os.path.exists(backups_folder):
        console.print("[bold yellow]Created backups folder")
        os.mkdir(backups_folder)

    shutil.make_archive(archive_name, "zip", world_folder)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[bold red]Backup interrupted!")
