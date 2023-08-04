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
        
    def test_create_item(self):
        repo = ItemRepositoryMock()
        len_before = len(repo.items)
        item = Item(name="test", price=1.0, item_type=ItemTypeEnum.TOY, admin_permission=False)
        repo.create_item(item=item, item_id=0)
        len_after = len(repo.items)
        assert len_after == len_before + 1
        assert repo.items.get(0) == item    