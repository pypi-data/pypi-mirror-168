from .index_json_get import AssetIndexJSONGet
from .product_json_get import AssetProductJSONGet


class AssetClient:
    @classmethod
    def get_product_json_for_active_theme(cls):
        return AssetProductJSONGet().get()

    @classmethod
    def get_index_json_for_active_theme(cls):
        return AssetIndexJSONGet().get()
