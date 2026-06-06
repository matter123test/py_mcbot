import shutil
import datetime

from rich.console import Console

console = Console()

WORLD_FOLDER = 'server/world'


def make_backup(archive_name):
    shutil.make_archive(archive_name, 'zip', WORLD_FOLDER)


def main():
    now = datetime.datetime.now()

    # Example output: "backup_2026-06-06_17-00"
    archive_name = now.strftime("backups/backup_%Y-%m-%d_%H-%M")

    with console.status("[bold yellow]Creating backup..."):
        make_backup(archive_name)

    console.print(f"[bold green]Created backup at {archive_name}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[bold red]Backup cancelled!")
