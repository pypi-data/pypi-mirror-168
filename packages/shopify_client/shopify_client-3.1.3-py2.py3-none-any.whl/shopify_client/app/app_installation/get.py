from shopify_client.common.graphql_client import GraphqlClient


class AppInstallationGet(GraphqlClient):
    def get(self):
        return self.execute()

    def get_query(self):
        return '''
        query AppInstallation {
            appInstallation{
                id
                launchUrl
            }
        }
        '''

    def get_variables(self, operation_input):
        pass

    def get_parsed_response(self, response):
        app_installation = response['data']['appInstallation']
        return {
            'id': app_installation['id'],
            'launch_url': app_installation['launchUrl']
        }
