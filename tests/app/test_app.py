from fastapi.exceptions import HTTPException
import pytest
from src.app.entities.item import Item
from src.app.enums.item_type_enum import ItemTypeEnum
from src.app.main import get_all_items, get_item, create_item, delete_item, update_item, items

class Test_App:
    def test_get_all_items(self):
        response = get_all_items()
        assert response == items
        
    def test_get_item(self):
        item_id = 1
        response = get_item(item_id=item_id)
        assert response == {
            'item_id' : item_id,
            'item': items.get(item_id).to_dict()
        }
        
    def test_get_item_id_is_none(self):
        item_id = None
        with pytest.raises(HTTPException) as err:
            get_item(item_id=item_id)
    
    def test_get_item_id_is_not_int(self):
        item_id = '1'
        with pytest.raises(HTTPException) as err:
            get_item(item_id=item_id)
            
    def test_create_item(self):
        len_before = len(items)
        body = {
            'item_id': 0,
            'name': 'test',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False
        }
        response = create_item(request=body)
        assert response == {'item_id': 0,'item': {'admin_permission': False, 'item_type': 'TOY', 'name': 'test', 'price': 1.0}}
        assert len(items)-1 == len_before
    
    def test_create_item_missing_id(self):
        body = {
            'name': 'test',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
        
    def test_create_item_id_is_not_int(self):
        body = {
            'item_id': '0',
            'name': 'test',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
    
    def test_create_item_id_is_not_positive(self):
        body = {
            'item_id': -1,
            'name': 'test',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_create_item_missing_type(self):
        body = {
            'item_id': 1,
            'name': 'test',
            'price': 1.0,
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_create_item_item_type_is_not_string(self):
        body = {
            'item_id': 1,
            'name': 'test',
            'price': 1.0,
            'item_type': 1,
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_create_item_item_type_is_not_valid(self):
        body = {
            'item_id': 1,
            'name': 'test',
            'price': 1.0,
            'item_type': 'test',
            'admin_permission': False
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_create_item_param_not_validated(self):
        body = {
            'item_id': 1,
            'name': '',
            'price': 1.0,
            'item_type': 'TOY',
            'admin_permission': False,
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
            
    def test_delete_item(self):
        body = {
            "item_id": 1
        }
        len_before = len(items)
        response = delete_item(request=body)
        assert response == {'item_id': 1, 'item': {'name': 'Barbie', 'price': 48.9, 'item_type': 'TOY', 'admin_permission': False}}
        assert len(items)+1 == len_before
        
    def test_delete_item_missing_id(self):
        with pytest.raises(HTTPException) as err:
            delete_item(request={})
            
    def test_delete_item_id_is_not_int(self):
        body = {
            "item_id": '1'
        }
        with pytest.raises(HTTPException) as err:
            delete_item(request=body)
            
    def test_delete_item_id_not_found(self):
        body = {
            "item_id": 100
        }
        with pytest.raises(HTTPException) as err:
            delete_item(request=body)
            
    def test_delete_item_without_admin_permission(self):
        body = {
            "item_id": 4
        }
        with pytest.raises(HTTPException) as err:
            delete_item(request=body)
            
    def test_update_item(self):
        print(len(items))
        body = {
            "item_id": 2,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False
        }
        response = update_item(request=body)
        assert response == {'item_id': 2, 'item': {'name': 'test', 'price': 1.0, 'item_type': 'TOY', 'admin_permission': False}}
        assert items[2] == Item(name='test', price=1.0, item_type=ItemTypeEnum.TOY, admin_permission=False)
        
    def test_update_item_missing_id(self):
        body = {
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
    
    def test_update_item_id_is_not_int(self):
        body = {
            "item_id": "1",
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            
    def test_update_item_not_found(self):
        body = {
            "item_id": 1,
            "name": "test",
            "price": 1.0,
            "item_type": "test",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            
    def test_update_item_without_admin_permission(self):
        body = {
            "item_id": 4,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
    
    def test_update_item_without_changes(self):
        body = {
            "item_id": 2,
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            
    def test_update_item_type_not_string(self):
        body = {
            "item_id": 1,
            "name": "test",
            "price": 1.0,
            "item_type": 1,
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            
    def test_update_item_type_not_valid(self):
        
        body = {
            "item_id": 1,
            "name": "test",
            "price": 1.0,
            "item_type": "test",
            "admin_permission": False
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
            