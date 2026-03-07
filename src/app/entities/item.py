from typing import Tuple
import uuid
from pydantic import BaseModel, ConfigDict, Field
from ..errors.entity_errors import ParamNotValidated
from ..enums.item_type_enum import ItemTypeEnum


class Item:
    item_id: str
    name: str
    price: float
    item_type: ItemTypeEnum
    admin_permission: bool
    
    def __init__(
        self, 
        item_id: str = None,
        name: str = None, 
        price: float = None, 
        item_type: ItemTypeEnum = None,
        admin_permission: bool = False # o default colocamos dessa forma
    ):
        validation_item_id = self.validate_item_id(item_id)
        if validation_item_id[0] is False:
            raise ParamNotValidated("item_id", validation_item_id[1])
        self.item_id = item_id
        
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
    def validate_item_id(item_id: str) -> Tuple[bool, str]:
        if item_id is None:
            return (False, "Item id is required")
        if type(item_id) != str:
            return (False, "Item id must be a string")
        if not uuid.UUID(item_id):
            return (False, "Item id must be a valid uuid string")
        return (True, "")
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        if name is None:
            return (False, "Name is required")
        if type(name) != str:
            return (False, "Name must be a string")
        if len(name) < 3:
            return (False, "Name must be at least 3 characters long")
        return (True, "")
        
    @staticmethod
    def validate_price(price: float) -> Tuple[bool, str]:
        if price is None:
            return (False, "Price is required")
        if type(price) != float:
            return (False, "Price must be a float")
        if price < 0:
            return (False, "Price must be a positive number")
        return (True, "")
    
    @staticmethod
    def validate_item_type(item_type: ItemTypeEnum) -> Tuple[bool, str]:
        if item_type is None:
            return (False, "Item type is required")
        if type(item_type) != ItemTypeEnum:
            return (False, "Item type must be a ItemTypeEnum")
        return (True, "")
    
    @staticmethod
    def validate_admin_permission(admin_permission: bool) -> Tuple[bool, str]:
        if admin_permission is None:
            return (False, "Admin permission is required")
        if type(admin_permission) != bool:
            return (False, "Admin permission must be a boolean")
        return (True, "")
    
        
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "item_type": self.item_type.value,
            "admin_permission": self.admin_permission
        }
    
    def __eq__(self,other):
        return (
            self.name == other.name and 
            self.price == other.price and 
            self.item_type == other.item_type and 
            self.admin_permission == other.admin_permission
        )
    
    def __repr__(self):
        return f"""
            Item(name={self.name}, 
            price={self.price}, 
            item_type={self.item_type}, 
            admin_permission={self.admin_permission})
        """
        
# esse é o caminho do desafio, não é necessário para completar o trainee fazer o objeto por meio do pydantic
        
class PydanticItem(BaseModel):
    
    item_id: uuid.UUID = Field(
        description="ID único do item, em formato UUID",
        default_factory=uuid.uuid4
    )
    name: str = Field(
        description="Nome do item, precisa ter no minimo 3 caracteres e no maximo 100",
        pattern=r'^[A-Za-z\s]+$', # apenas espaços e letras
        min_length=3,
        max_length=100,
    )
    price: float = Field(
        description="Preço do Item, precisa ser maior que 0",
        gt=0 # gt significa greater than
    )
    item_type: ItemTypeEnum = Field(
        description="Tipo do Item, determinado por um Enum",
    )
    admin_permission: bool = Field(
        description="Bool indicando permissão de administador",
        default=False
    )
    
    model_config = ConfigDict(
        use_enum_values=False,
        extra="forbid",
        populate_by_name=True
    )