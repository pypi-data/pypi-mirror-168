import json
import logging

from plotrisk_python_client import Configuration
from plotrisk_python_client.api.keycloak_api import KeycloakApi
from plotrisk_python_client.util import EnvType

from python_sdk_client.clients_enum import EnvType

from python_sdk_client.libs.client_cfg import InsightServiceCfg
from python_sdk_client.libs.cropin_exceptions import UnauthorizedError

"""

Keycloak Client
----------------

A class for authenticating the user

"""


class KeyCloakAPI:
    """
    Generates token given tenant, username and password as input
    """
    logging = logging.getLogger('KeyCloakAPI')

    def __init__(self, env: EnvType):
        self.env = env

    def authenticate(self, tenant: str, username: str, password: str) -> (str, str):
        logging.info("Starting authentication now")
        token = None
        refresh_token = None
        x_api_key = None
        response = self._internal_sdk_auth_check(tenant, username, password)
        result_json = json.loads(response)
        if response is not None:
            token = result_json.get('access_token')
            refresh_token = result_json.get('refresh_token')
        if token is None:
            raise UnauthorizedError("Authentication not successful token is None")
        if refresh_token is None:
            raise UnauthorizedError("Authentication not successful refresh_token is None")
        logging.info("Authentication successful! Ready to make function call.")
        return token, refresh_token, x_api_key

    """
    Get access token using the refresh token for authentication
    """

    def re_authenticate(self, refresh_token: str) -> (str, str):
        token = None
        refresh_token = None
        x_api_key = None
        # TODO: refresh token using SDK
        if token is None or refresh_token is None:
            raise UnauthorizedError("Authentication not successful")
        return token, refresh_token, x_api_key

    """
    Validating the returned token
    """

    def validate_token(self, token: str) -> bool:
        is_valid = True
        # TODO: check if token has expired
        return is_valid

    def _internal_sdk_auth_check(self, tenant: str, username: str, password: str):
        import plotrisk_python_client
        from plotrisk_python_client.rest import ApiException

        configuration = Configuration()

        if self.env.value == EnvType.QA.value:
            configuration.host = InsightServiceCfg.QA_BASE_URL

        elif self.env.value == EnvType.PROD.value:
            configuration.host = InsightServiceCfg.PROD_BASE_URL

        elif self.env.value == EnvType.PROD2.value:
            configuration.host = InsightServiceCfg.PROD2_BASE_URL

        elif self.env.value == EnvType.DEV.value:
            configuration.host = InsightServiceCfg.DEV_BASE_URL

        else:
            configuration.host = InsightServiceCfg.PROD_BASE_URL

        keycloakApi = KeycloakApi()  # AccessTokenRequest |
        # Generate access token

        try:

            api_response = keycloakApi.get_token(tenant=tenant, username=username,
                                                 password=password, env=self.env)
            logging.info("auth api response: {0}".format(api_response))
            return api_response
        except ApiException as e:
            logging.error("Exception when calling AuthenticateApi->get_token: {}\n".format(e))
            raise Exception("failed to auth ", e)
