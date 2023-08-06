
import logging
from typing import Dict
from .abstract_cached_connexions import AbstractCachedConnexions
from .token_service import TokenServiceConnexion

class CachedConnexions(AbstractCachedConnexions):
    
    def __init__(self, default_host: str = None, default_api_token: str = None) -> None:
        self.connexions: Dict[str, TokenServiceConnexion] = dict()
        self.default_host = default_host
        self.default_api_token = default_api_token

    def get(self, host: str, api_token: str = None) -> TokenServiceConnexion:
        if host in self.connexions:
            return self.connexions[host]
        
        if api_token is None:
            api_token = self.default_api_token

        self.connexions[host] = TokenServiceConnexion(host, api_token, authorization_key="Bearer")
        return self.connexions[host]

    def get_default(self) -> TokenServiceConnexion:
        if self.default_host is None:
            raise Exception("No default connexion")
        
        return self.get(self.default_host)

    def reset(self, host: str) -> None:
        if host not in self.connexions:
            return

        try:
            self.connexions[host].session.close()
        except Exception: #pragma: no cover
            logging.error(f"Could not close session for TokenServiceConnexion with host {host}")
        finally:
            del self.connexions[host]
