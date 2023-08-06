from shopify_client.common.graphql_client import GraphqlClient
from shopify_client.common.mixins import UserErrorParserMixin


class AppMetafieldSet(GraphqlClient, UserErrorParserMixin):
    def get_query(self):
        return '''
        mutation CreateAppOwnedMetafield($metafieldsSetInput: [MetafieldsSetInput!]!) {
          metafieldsSet(metafields: $metafieldsSetInput) {
            metafields {
              id
              namespace
              key
              value
            }
            userErrors {
              field
              message
            }
          }
        }
        '''

    def get_variables(self, operation_inputs):
        return {
            "metafieldsSetInput": [
                {
                    "namespace": operation_input['namespace'],
                    "key": operation_input['key'],
                    "type": operation_input['type'],
                    "value": operation_input['value'],
                    "ownerId": operation_input['owner_id']
                } for operation_input in operation_inputs
            ]
        }

    def get_parsed_response(self, response):
        metafields_response = response['data']['metafieldsSet']

        return {
            'metafields': metafields_response['metafields'],
            'errors': self.parse_user_error(metafields_response['userErrors'])
        }

    def set(self, metafield_input):
        return self.execute(metafield_input)
