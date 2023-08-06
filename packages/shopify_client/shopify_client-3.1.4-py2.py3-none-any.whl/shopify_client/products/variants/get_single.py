import json

import shopify


class VariantsGetSingle:
    def get(self, variant_input):
        response = shopify.GraphQL().execute(self.get_query(), self.get_variables(variant_input))
        return self.get_parse_response(json.loads(response))

    def get_query(self):
        return '''
            query getVariant($id: ID!){
                productVariant(id: $id){
                    id
                    title
                    displayName
                    price
                    sku
                    availableForSale
                    selectedOptions {
                        name
                        value
                    }
                    product {
                        id
                        title
                        handle
                        featuredImage {
                            url
                        }
                    }
                    image {
                        url
                    }
                }
            }
        '''

    def get_variables(self, variants_input):
        return {
            'id': variants_input['variant_id']
        }

    def get_parse_response(self, response):
        variant = response['data']['productVariant']
        return {
            'id': variant['id'],
            'title': variant['title'],
            'display_name': variant['displayName'],
            'price': float(variant['price']),
            'sku': variant['sku'],
            'is_available': variant['availableForSale'],
            'selected_options': variant['selectedOptions'],
            'image': (variant['image'] or {}).get('url') or variant['product']['featuredImage']['url'],
            'product_id': variant['product']['id'],
            'product_name': variant['product']['title'],
            'product_handle': variant['product']['handle']
        }
