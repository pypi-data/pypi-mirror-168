import logging

from python_sdk_client.clients_enum import EnvType
from abc import ABC

from python_sdk_client.libs.keycloak_client import KeyCloakAPI


class AbstractClient(ABC):

    def __init__(self, tenant: str, username: str, password: str, env: EnvType) -> None:
        self.tenant = tenant
        self.env = env
        self.org_id = 'sf_plus_' + str(tenant)
        self.token, self.refresh_token, self.x_api_key = KeyCloakAPI(env).authenticate(tenant, username, password)
        logging.info("Super class is initialized")

    def get_auth(self) -> str:
        return self.token

    def refresh_auth(self) -> (str, str):
        self.token, self.refresh_token = KeyCloakAPI.re_authenticate(self.refresh_token())
