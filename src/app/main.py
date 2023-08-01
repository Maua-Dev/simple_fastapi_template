from fastapi import FastAPI, HTTPException
from mangum import Mangum

from .errors.entity_errors import ParamNotValidated

from .enums.item_type_enum import ItemTypeEnum

from .entities.item import Item


app = FastAPI()

items = {
    1: Item(name="Barbie", price=48.90, item_type=ItemTypeEnum.TOY, admin_permission=False),
    2: Item(name="Hamburguer", price=38.00, item_type=ItemTypeEnum.FOOD, admin_permission=False),
    3: Item(name="T-shirt", price=22.95, item_type=ItemTypeEnum.CLOTHES, admin_permission=False),
    4: Item(name="Super Mario Bros", price=55.00, item_type=ItemTypeEnum.GAMES, admin_permission=True)
}

# TODO: Implement my logic here to handle the requests from SimpleFastAPI

@app.get("/items/get_all_items")
def get_all_items():
    global items
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id is None:
        raise HTTPException(status_code=400, detail="Missing 'item_id' parameter")

    if type(item_id) != int:
        raise HTTPException(status_code=400, detail="Parameter 'item_id' must be an integer")
    
    global items
    item = items.get(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")
    
    return {
        "item_id": item_id,
        "item": item.to_dict()    
    }

@app.post("/items/create_item", status_code=201)
def create_item(request: dict):
    item_id = request.get("item_id")
    if item_id is None:
        raise HTTPException(status_code=400, detail="Missing 'item_id' parameter")

    if type(item_id) != int:
        raise HTTPException(status_code=400, detail="Parameter 'item_id' must be an integer")
    
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Parameter 'item_id' must be a positive integer")
    
    name = request.get("name")
    price = request.get("price")
    item_type = request.get("item_type")
    if item_type is None:
        raise HTTPException(status_code=400, detail="Item type is required")
    if type(item_type) != str:
        raise HTTPException(status_code=400, detail="Item type must be a string")
    if item_type not in [possible_type.value for possible_type in ItemTypeEnum]:
        raise HTTPException(status_code=400, detail="Item type is not a valid one")
    
    admin_permission = request.get("admin_permission")
    
    try:
        item = Item(name=name, price=price, item_type=ItemTypeEnum[item_type], admin_permission=admin_permission)
    except ParamNotValidated as err:
        raise HTTPException(status_code=400, detail=err.message)
    
    items[item_id] = item
    return {
        "item_id": item_id,
        "item": item.to_dict()    
    }
    
@app.delete("/items/delete_item")
def delete_item(request: dict):
    item_id = request.get("item_id")
    if item_id is None:
        raise HTTPException(status_code=400, detail="Missing 'item_id' parameter")

    if type(item_id) != int:
        raise HTTPException(status_code=400, detail="Parameter 'item_id' must be an integer")
    
    global items
    item = items.get(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")
    
    if item.admin_permission == True:
        raise HTTPException(status_code=403, detail="Item Not found")
    
    items.pop(item_id)
    
    return {
        "item_id": item_id,
        "item": item.to_dict()    
    }
    
@app.put("/items/update_item")
def update_item(request: dict):
    item_id = request.get("item_id")
    if item_id is None:
        raise HTTPException(status_code=400, detail="Missing 'item_id' parameter")

    if type(item_id) != int:
        raise HTTPException(status_code=400, detail="Parameter 'item_id' must be an integer")
    
    global items
    item = items.get(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")
    
    if item.admin_permission == True:
        raise HTTPException(status_code=403, detail="Item Not found")
    
    name = request.get("name")
    price = request.get("price")
    item_type = request.get("item_type")
    admin_permission = request.get("admin_permission")
    
    if name == None and price == None and item_type == None and admin_permission == None:
        raise HTTPException(status_code=400, detail="Missing parameters")
    if name != None:
        items[item_id].name = name
    if price != None:
        items[item_id].price = price
    if item_type != None:
        if type(item_type) != str:
            raise HTTPException(status_code=400, detail="Item type must be a string")
        if item_type not in [possible_type.value for possible_type in ItemTypeEnum]:
            raise HTTPException(status_code=400, detail="Item type is not a valid one")
        items[item_id].item_type = ItemTypeEnum[item_type]
    if admin_permission != None:
        items[item_id].admin_permission = admin_permission
    
    return {
        "item_id": item_id,
        "item": items[item_id].to_dict()    
    }
    


handler = Mangum(app, lifespan="off")
