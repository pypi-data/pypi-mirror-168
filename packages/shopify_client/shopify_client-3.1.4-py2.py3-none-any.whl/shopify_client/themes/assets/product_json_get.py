import json

import shopify


class AssetProductJSONGet:
    def get(self):
        theme_id = self.get_active_theme_id()
        product_json_asset = self.get_product_json_asset(theme_id)

        return json.loads(product_json_asset.value)

    def get_active_theme_id(self):
        return shopify.Theme.find_first(role='main').id

    def get_product_json_asset(self, theme_id):
        return shopify.Asset.find(theme_id=theme_id, key='templates/product.json')
