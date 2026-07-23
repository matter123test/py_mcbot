import requests

from setup.api import LoaderAPI


class FabricMC(LoaderAPI):
    def __init__(self):
        super().__init__(server_url="https://meta.fabricmc.net/")

    def get_supported_versions(self) -> list[str]:
        return self.get_supported_minecraft_versions()

    def get_supported_minecraft_versions(self) -> list[str]:
        response = requests.get(self.server_url + "/v2/versions/game")
        data = response.json()
        stable_versions = [e["version"] for e in data if e["stable"]]
        return stable_versions

    def get_stable_fabric_loader_versions(self) -> list[str]:
        response = requests.get(self.server_url + "/v2/versions/loader")
        data = response.json()
        stable_versions = [e["version"] for e in data if e["stable"]]
        return stable_versions

    def get_latest_fabric_installer_version(self) -> str:
        response = requests.get(self.server_url + "/v2/versions/installer")
        data = response.json()
        stable_versions = [e["version"] for e in data if e["stable"]]
        return stable_versions[0]

    def get_latest_build_download_url(self, game_version: str):
        loader_version = self.get_stable_fabric_loader_versions()[0]
        installer_version = self.get_latest_fabric_installer_version()

        url = (
            self.server_url
            + f"/v2/versions/loader/{game_version}/{loader_version}/{installer_version}/server/jar"
        )

        return url
