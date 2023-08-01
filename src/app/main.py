from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# TODO: Implement my logic here to handle the requests from SimpleFastAPI


@app.get("/")
def read_root():
    return {
        "name": "Luigi Trevisan",
        "agency": "0000",
        "account": "00000-0",
        "current_balance": 1000.0
    }


@app.get("/history")
def get_history():
    return {
        'all_transactions' : [
            {
                "type" : "deposit",
                "value" : 100.0,
                "timestamp" : 1690482853890
            },
            {
                "type" : "withdraw",
                "value" : 200.0,
                "timestamp" : 1690482853890
            }
        ]
    }

@app.post("/withdraw")
def withdraw(request: dict):
    notas200 = request.get("200")
    notas100 = request.get("100")
    notas50 = request.get("50")
    notas20 = request.get("20")
    notas10 = request.get("10")
    notas5 = request.get("5")
    notas2 = request.get("2")
    return {
        "current_balance": 1000.0,
        "timestamp": 1690482853890, #milliseconds
    }
    
@app.post("/deposit")
def deposit(request: dict):
    notas200 = request.get("200")
    notas100 = request.get("100")
    notas50 = request.get("50")
    notas20 = request.get("20")
    notas10 = request.get("10")
    notas5 = request.get("5")
    notas2 = request.get("2")
    return {
        "current_balance": 1000.0,
        "timestamp": 1690482853890, #milliseconds
    }

handler = Mangum(app, lifespan="off")
