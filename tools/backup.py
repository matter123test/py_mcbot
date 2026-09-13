import os.path
import shutil
import datetime

from rich.console import Console

console = Console()

from argparse import ArgumentParser

# Defaults
SERVER_FOLDER = "server"
WORLD_FOLDER = os.path.join(SERVER_FOLDER, "world")
BACKUPS_FOLDER = "backups"

def main():
    parser = ArgumentParser(
        prog="Backup tool", description="Creates backups from world folder"
    )

    parser.add_argument("-n", "--name", help="name of the output file", default=None)
    parser.add_argument(
        "-f",
        "--backup_folder",
        help="specify the output backups folder",
        default=BACKUPS_FOLDER,
    )
    parser.add_argument(
        "-w",
        "--world-folder",
        help="specify where the world folder is located",
        default=WORLD_FOLDER,
    )

    parser.add_argument(
        "--full",
        help="Create a full backup of the server root folder",
        action="store_true"
    )

    args = parser.parse_args()

    archive_name = args.name
    if archive_name is None:
        archive_name = get_archive_name(args.backup_folder)
    else:
        archive_name = os.path.join(args.backup_folder, archive_name)

    world_folder = args.world_folder

    if args.full:
        split = os.path.split(world_folder)
        path = split[0:len(split) - 1]
        world_folder = os.path.join(*path)


    with console.status(f"[bold yellow]Creating {"full " if args.full else ''}backup..."):
        make_backup(
            archive_name=archive_name,
            backups_folder=args.backup_folder,
            world_folder=world_folder,
        )

    console.print(f"[bold green]Created {"full " if args.full else ''}backup at {archive_name}")


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
