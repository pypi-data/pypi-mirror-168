from .set import AppMetafieldSet


class AppMetafieldClient:
    @staticmethod
    def set(metafield_input):
        return AppMetafieldSet().set(metafield_input)
