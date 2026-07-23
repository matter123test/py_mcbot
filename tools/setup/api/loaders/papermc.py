import requests

from setup.api import LoaderAPI


class PaperMC(LoaderAPI):
    def __init__(self):
        super().__init__(server_url="https://fill.papermc.io/")

    def get_supported_versions(self):
        url = self.server_url + "v3/projects/paper/versions"

        res = requests.get(url)
        data = res.json()

        versions: list[str] = []

        for entry in data["versions"]:
            support = entry["version"]["support"]["status"]

            if support != "SUPPORTED":
                continue

            id = entry["version"]["id"]

            versions.append(id)

        return versions

    def get_latest_build_download_url(self, game_version: str):
        url = (
            self.server_url
            + "v3/projects/paper/versions/"
            + game_version
            + "/builds/latest"
        )

        res = requests.get(url)
        data = res.json()

        url = data["downloads"]["server:default"]["url"]

        return url
