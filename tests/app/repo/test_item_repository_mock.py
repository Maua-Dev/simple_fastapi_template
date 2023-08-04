import pytest
from src.app.entities.item import Item
from src.app.enums.item_type_enum import ItemTypeEnum
from src.app.repo.item_repository_mock import ItemRepositoryMock

class Test_ItemRepositoryMock:
    def test_get_all_items(self):
        repo = ItemRepositoryMock()
        assert all([item_expect == item for item_expect, item in zip(repo.items.values(), repo.get_all_items())]) 
        
    def test_get_item(self):
        repo = ItemRepositoryMock()
        item = repo.get_item(item_id=1)
        assert item == repo.items.get(1)
    
    def test_get_item_not_found(self):
        repo = ItemRepositoryMock()
        item = repo.get_item(item_id=10)
        assert item is None    