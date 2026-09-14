from datetime import datetime
from dataclasses import dataclass
import os
import shutil
import json

@dataclass
class BackupInfo:
    name: str
    full_path: str
    time: datetime

    def toJSON(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)


SERVER_FOLDER = "server"
WORLD_FOLDER = os.path.join(SERVER_FOLDER, "world")
BACKUPS_FOLDER = "backups"

class BackupSystem:
    def __init__(self) -> None:
        self.MAX_BACKUPS = 2
        self.backups: list[BackupInfo] = []

    def create_backup(self):
        print("---BACKUP----")
    
        if len(self.backups) >= self.MAX_BACKUPS:
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
        filename = os.path.join(BACKUPS_FOLDER, name)
        
        if not os.path.exists(BACKUPS_FOLDER):
            os.mkdir(BACKUPS_FOLDER)

        full_path = self._make_folder_archive(WORLD_FOLDER, filename)

        if not full_path:
            print("Backup failed to create")
        else:
            info = BackupInfo(name, full_path, time)
            print(f"Created backup at: {full_path}")

        self.backups.append(info)

        self._save()

        print("---BACKUP----")
        
    # def _delete_backup(self, filepath:):
    #     pass

    def _make_folder_archive(self, folder_path: str, output_filename: str) -> str | None:
        """Creates an archive, returns True if successful"""

        if not os.path.exists(BACKUPS_FOLDER):
            os.mkdir(BACKUPS_FOLDER)
            print("Created backup folder")

        try:
            return shutil.make_archive(output_filename, "zip", folder_path)
        except shutil.Error as e:
            print(f"Error occurred while creating the archive: {output_filename}: {e}")
            return None

    def _save(self):
        with open("backups.json", "w") as f:
            data = [
                {"name": backup.name, "full_path": backup.full_path, "time": str(backup.time)} for backup in self.backups
            ]

            json.dump(data, f)
            print("Saved backups.json")
