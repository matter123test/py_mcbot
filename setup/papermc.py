import requests
from dataclasses import dataclass

SERVER_URL = "https://fill.papermc.io/"


@dataclass
class Version:
    id: str
    minimum_java_version: int
    recommended_flags: list[str]


@dataclass
class DownloadInfo:
    name: str
    url: str
    total_size: int


def get_supported_versions() -> list[Version]:
    url = SERVER_URL + "v3/projects/paper/versions"

    res = requests.get(url)
    data = res.json()

    versions: list[Version] = []

    for entry in data["versions"]:
        support = entry["version"]["support"]["status"]

        if support != "SUPPORTED":
            continue

        id = entry["version"]["id"]
        java_version = entry["version"]["java"]["version"]["minimum"]
        flags = entry["version"]["java"]["flags"]["recommended"]

        versions.append(Version(id, java_version, flags))

    return versions


def get_latest_build_download(ver: Version) -> DownloadInfo:
    url = SERVER_URL + "v3/projects/paper/versions/" + ver.id + "/builds/latest"

    res = requests.get(url)
    data = res.json()

    name = data["downloads"]["server:default"]["name"]
    url = data["downloads"]["server:default"]["url"]
    size = data["downloads"]["server:default"]["size"]

    return DownloadInfo(name, url, size)
