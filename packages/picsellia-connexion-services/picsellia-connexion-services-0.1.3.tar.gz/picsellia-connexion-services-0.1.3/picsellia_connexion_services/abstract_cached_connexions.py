
from abc import ABC, abstractmethod
from .abstract_service_connexion import AbstractServiceConnexion

class AbstractCachedConnexions(ABC):

    @abstractmethod
    def get(self, host: str, api_token: str = None) -> AbstractServiceConnexion:
        pass

    @abstractmethod
    def get_default(self) -> AbstractServiceConnexion:
        pass

    @abstractmethod
    def reset(self, host: str) -> None:
        pass