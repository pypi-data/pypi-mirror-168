from .app_installation import AppInstallationClient
from .metafields import AppMetafieldClient


class AppClient:
    @property
    def installation(self):
        return AppInstallationClient

    @property
    def metafields(self):
        return AppMetafieldClient
