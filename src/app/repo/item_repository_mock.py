from typing import Dict, Optional, List

from ..enums.item_type_enum import ItemTypeEnum
from ..entities.item import Item
from .item_repository_interface import IItemRepository


class ItemRepositoryMock(IItemRepository):
    items: Dict[int, Item]
    
    def __init__(self):
        self.items = {
            1: Item(name="Barbie", price=48.90, item_type=ItemTypeEnum.TOY, admin_permission=False),
            2: Item(name="Hamburguer", price=38.00, item_type=ItemTypeEnum.FOOD, admin_permission=False),
            3: Item(name="T-shirt", price=22.95, item_type=ItemTypeEnum.CLOTHES, admin_permission=False),
            4: Item(name="Super Mario Bros", price=55.00, item_type=ItemTypeEnum.GAMES, admin_permission=True)
        }
        
    def get_all_items(self) -> List[Item]:
        return self.items.values()
    
    def get_item(self, item_id: int) -> Optional[Item]:
        '''
        Returns the item with the given id.
        If the item does not exist, returns None
        '''
        pass
    
    def create_item(self, item: Item, item_id: int) -> Item:
        '''
        Creates a new item in the database
        '''
        pass
    
    def delete_item(self, item_id: int) -> Item:
        '''
        Deletes the item with the given id.
        If the item does not exist, returns None
        '''
        
    def update_item(self, item_id: int, item: Item) -> Item:
        '''
        Updates the item with the given id.
        If the item does not exist, returns None
        '''
        pass
    
    