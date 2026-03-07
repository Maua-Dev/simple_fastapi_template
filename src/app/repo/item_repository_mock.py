from typing import Dict, Optional, List

from ..enums.item_type_enum import ItemTypeEnum
from ..entities.item import Item, PydanticItem
from .item_repository_interface import IItemRepository


class ItemRepositoryMock(IItemRepository):
    items: List[Item]
    
    def __init__(self):
        self.items = [
            Item(
                item_id="b11af449-22c7-43db-b0e4-dbfbbe7fdbd7", 
                name="Barbie", price=48.90, 
                item_type=ItemTypeEnum.TOY, 
                admin_permission=False
            ),
            Item(
                item_id="b21af449-22c7-43db-b0e4-dbfbbe7fdbd7", 
                name="Hamburguer", price=38.00, 
                item_type=ItemTypeEnum.FOOD, 
                admin_permission=False
            ),
            Item(
                item_id="b31af449-22c7-43db-b0e4-dbfbbe7fdbd7", 
                name="T-shirt", price=22.95, 
                item_type=ItemTypeEnum.CLOTHES, 
                admin_permission=False
            ),
            Item(
                item_id="b41af449-22c7-43db-b0e4-dbfbbe7fdbd7", 
                name="Super Mario Bros", price=55.00, 
                item_type=ItemTypeEnum.GAMES, 
                admin_permission=True
            )
        ]
        
    def get_all_items(self) -> List[Item]:
        return self.items
    
    def get_item(self, item_id: str) -> Optional[Item]:
        for item in self.items:
            
            if item.item_id == item_id:
                return item
            
        return None
    
    def create_item(self, item: Item) -> Item:
        
        self.items.append(item)
        
        return item
    
    def delete_item(self, item_id: str) -> Item:
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)
                return item
        return None
        
        
    def update_item(
        self, 
        item_id:int, 
        name:str=None, 
        price:float=None, 
        item_type:ItemTypeEnum=None, 
        admin_permission:bool=None
    ) -> Item:
        
        for item in self.items:
            
            if item.item_id == item_id:
                if name is not None:
                    item.name = name
                if price is not None:
                    item.price = price
                if item_type is not None:
                    item.item_type = item_type
                if admin_permission is not None:
                    item.admin_permission = admin_permission
                return item
            
        return None
    