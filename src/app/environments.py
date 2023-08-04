
from enum import Enum

from .errors.environment_errors import EnvironmentNotFound

from .repo.item_repository_interface import IItemRepository


class REPO(Enum):
    MOCK = "MOCK"

class Environments:
    """
    This is an abstraction of "Environments" to simplify the concept. The environments are hardcoded in this class.
    """
    repo: REPO = REPO.MOCK    
    @staticmethod
    def get_item_repo() -> IItemRepository:    
        if Environments.repo == REPO.MOCK:
            from .repo.item_repository_mock import ItemRepositoryMock
            return ItemRepositoryMock
        else:
            raise EnvironmentNotFound("REPO")
    
    