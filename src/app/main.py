from fastapi import FastAPI, Response
from mangum import Mangum

from .errors.entity_errors import ParamNotValidated

from .enums.item_type_enum import ItemTypeEnum

from .entities.item import Item


app = FastAPI()

items = {
    1: Item(name="Barbie", price=48.90, item_type=ItemTypeEnum.TOY),
    2: Item(name="Hamburguer", price=38.00, item_type=ItemTypeEnum.FOOD),
    3: Item(name="T-shirt", price=22.95, item_type=ItemTypeEnum.CLOTHES),
    4: Item(name="Super Mario Bros", price=55.00, item_type=ItemTypeEnum.GAMES)
}

# TODO: Implement my logic here to handle the requests from SimpleFastAPI

@app.get("/items/get_all_items")
def get_all_items():
    global items
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response):
    if item_id is None:
        response.status_code = 400
        return "Missing 'item_id' parameter"

    if type(item_id) != int:
        response.status_code = 400
        return "Parameter 'item_id' must be an integer"
    
    global items
    item = items.get(item_id)
    
    if item == None:
        response.status_code = 404
        return "Item Not found"
    return {
        "item_id": item_id,
        "item": dict(item)    
    }

@app.post("/items/create_item")
def create_item(request: dict, response: Response):
    item_id = request.get("item_id")
    if item_id is None:
        response.status_code = 400
        return "Missing 'item_id' parameter"
    if type(item_id) != int:
        response.status_code = 400
        return "Parameter 'item_id' must be an integer"
    
    name = request.get("name")
    price = request.get("price")
    item_type = request.get("item_type")
    
    try:
        item = Item(name=name, price=price, item_type=item_type)
    except ParamNotValidated as err:
        response.status_code = 400
        return err.message
    
    items[item_id] = item
    return {
        "item_id": item_id,
        "item": dict(item)    
    }
    
@app.delete("/items/delete_item")
def delete_item(request: dict, response: Response):
    pass
    



handler = Mangum(app, lifespan="off")
