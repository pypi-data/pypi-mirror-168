
from typing import Dict
from .abstract_cached_connexions import AbstractCachedConnexions
from .mock_service_connexion import MockServiceConnexion
from requests.models import Response

class MockCachedConnexions(AbstractCachedConnexions):
    
    def __init__(self) -> None:
        self.connexions: Dict[str, MockServiceConnexion] = dict()
        self.default_host = "localhost"
        self.default_api_token = "random_token"

    def get(self, host: str, api_token: str = None) -> MockServiceConnexion:
        if host in self.connexions:
            return self.connexions[host]
        
        if api_token is None:
            api_token = self.default_api_token

        self.connexions[host] = self._new_connexion()
        return self.connexions[host]

    def get_default(self) -> MockServiceConnexion:
        return self.get(self.default_host)

    def _new_connexion(self) -> MockServiceConnexion:
        mock_client = MockServiceConnexion()
        fake_resp = Response()
        fake_resp._content = {"success": "ok"}
        fake_resp.status_code = 200
        mock_client.set_default_response("get", fake_resp)
        mock_client.set_default_response("post", fake_resp)
        mock_client.set_default_response("put", fake_resp)
        mock_client.set_default_response("delete", fake_resp)
        return mock_client

    def reset(self, host: str) -> None:
        if host not in self.connexions:
            return

        del self.connexions[host]

