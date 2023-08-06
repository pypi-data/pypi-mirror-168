from .get import AppInstallationGet


class AppInstallationClient:
    @staticmethod
    def get():
        return AppInstallationGet().get()
