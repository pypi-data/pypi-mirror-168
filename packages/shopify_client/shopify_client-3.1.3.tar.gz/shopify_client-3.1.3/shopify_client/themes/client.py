from .assets import AssetClient


class ThemeClient:
    @property
    def assets(self):
        return AssetClient
