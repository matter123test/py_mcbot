class LoaderAPI:
    def __init__(self, server_url):
        self.server_url = server_url

    def get_supported_versions(self) -> list[str]:
        pass

    def get_latest_build_download_url(self, game_version: str):
        pass
