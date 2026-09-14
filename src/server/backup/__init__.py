from dataclasses import dataclass
from datetime import datetime
from config import Server

import dateutil
import os
import shutil
import json


class BackupSystem:
    @dataclass
    class BackupInfo:
        name: str
        full_path: str
        time: datetime

        def toJSON(self) -> str:
            return json.dumps(
                self, default=lambda o: o.__dict__, sort_keys=True, indent=4
            )

    def __init__(self, backups_config: Server.Backups) -> None:
        self.config = backups_config
        self.backups: list[BackupSystem.BackupInfo] = []

        if os.path.exists(self.config.save_file):
            with open(self.config.save_file, "r") as f:
                contents = json.load(f)

                for item in contents:
                    self.backups.append(
                        BackupSystem.BackupInfo(
                            item["name"],
                            item["full_path"],
                            dateutil.parser.parse(item["time"]),
                        )
                    )

            print(f"Loaded backups save file: {self.config.save_file}")

    def create_backup(self):
        print("---BACKUP----")

        if len(self.backups) >= self.config.max_backups:
            oldest = self.backups[0]

            for backup in self.backups:
                # past < present
                if backup.time < oldest.time:
                    oldest = backup

            self.backups.remove(oldest)
            print(f"Removed oldest backup: {oldest.full_path}")
            os.remove(oldest.full_path)

        time = datetime.now()
        name = time.strftime("backup_%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.config.backups_folder, name)

        if not os.path.exists(self.config.backups_folder):
            os.mkdir(self.config.backups_folder)

        full_path = self._make_folder_archive(self.config.world_folder, filename)

        if not full_path:
            print("Backup failed to create")
        else:
            info = BackupSystem.BackupInfo(name, full_path, time)
            print(f"Created backup at: {full_path}")

        self.backups.append(info)

        self._save()

        print("---BACKUP----")

    def _make_folder_archive(
        self, folder_path: str, output_filename: str
    ) -> str | None:
        """Creates an archive, returns True if successful"""

        if not os.path.exists(self.config.backups_folder):
            os.mkdir(self.config.backups_folder)
            print("Created backup folder")

        try:
            return shutil.make_archive(output_filename, "zip", folder_path)
        except shutil.Error as e:
            print(f"Error occurred while creating the archive: {output_filename}: {e}")
            return None

    def _save(self):
        with open("backups.json", "w") as f:
            data = [
                {
                    "name": backup.name,
                    "full_path": backup.full_path,
                    "time": str(backup.time),
                }
                for backup in self.backups
            ]

            json.dump(data, f)
            print("Saved backups.json")
