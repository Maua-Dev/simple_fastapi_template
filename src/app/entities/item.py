from typing import Tuple
from ..errors.entity_errors import ParamNotValidated
from ..enums.item_type_enum import ItemTypeEnum


class Item:
    name: str
    price: float
    item_type: ItemTypeEnum
    admin_permission: bool = False
    
    def __init__(self, name: str=None, price: float=None, item_type: ItemTypeEnum=None, admin_permission: bool=None):
        validation_name = self.validate_name(name)
        if validation_name[0] is False:
            raise ParamNotValidated("name", validation_name[1])
        self.name = name
        
        validation_price = self.validate_price(price)
        if validation_price[0] is False:
            raise ParamNotValidated("price", validation_price[1])
        self.price = price

        validation_item_type = self.validate_item_type(item_type)
        if validation_item_type[0] is False:
            raise ParamNotValidated("item_type", validation_item_type[1])
        self.item_type = item_type
        
        validation_admin_permission = self.validate_admin_permission(admin_permission)
        if validation_admin_permission[0] is False:
            raise ParamNotValidated("admin_permission", validation_admin_permission[1])
        self.admin_permission = admin_permission
        
    @staticmethod
    def validate_name(name: str) -> Tuple[float, str]:
        if name is None:
            return (False, "Name is required")
        if type(name) != str:
            return (False, "Name must be a string")
        if len(name) < 3:
            return (False, "Name must be at least 3 characters long")
        return (True, "")
        
    @staticmethod
    def validate_price(price: float) -> Tuple[float, str]:
        if price is None:
            return (False, "Price is required")
        if type(price) != float:
            return (False, "Price must be a float")
        if price < 0:
            return (False, "Price must be a positive number")
        return (True, "")
    
    @staticmethod
    def validate_item_type(item_type: ItemTypeEnum) -> Tuple[float, str]:
        if item_type is None:
            return (False, "Item type is required")
        if type(item_type) != ItemTypeEnum:
            return (False, "Item type must be a ItemTypeEnum")
        return (True, "")
    
    @staticmethod
    def validate_admin_permission(admin_permission: bool) -> Tuple[float, str]:
        if admin_permission is None:
            return (False, "Admin permission is required")
        if type(admin_permission) != bool:
            return (False, "Admin permission must be a boolean")
        return (True, "")
        
    
    def __dict__(self):
        return {
            "name": self.name,
            "price": self.price,
            "item_type": self.item_type.value
        }