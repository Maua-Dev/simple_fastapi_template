from fastapi import FastAPI
from mangum import Mangum

from .entities.test_entitie import Entidade

app = FastAPI()

# TODO: Implement my logic here to handle the requests from SimpleFastAPI

@app.get("/")
def read_root():
    Entidade.print()
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/create_item")
def create_item(request: dict):
    item_id = request.get("item_id")
    name = request.get("name")

    return {"item_id": item_id,
            "name": name}   


handler = Mangum(app, lifespan="off")
