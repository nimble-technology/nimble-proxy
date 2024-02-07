from fastapi import FastAPI
from pydantic import BaseModel
from query import QueryRequest, get_balance, query_inerface
from query_map import QueryMapRequest, get_balances, query_map_interface
from set_weights import SetWeightsRequest, set_weights
app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None


@app.get("/print")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_description": item.description}


@app.post("/dendrite/")
async def post_dendrite(synapse: dict):
    print("dendrite synapse", synapse)
    return {"synapse": synapse}


@app.post("/set_weights")
async def call_set_weights(request: SetWeightsRequest):
    return await set_weights(request)


@app.post("/get_balance")
async def call_get_balance(request: QueryRequest):
    return await get_balance(request)


@app.post("/query")
async def call_query_api(request: QueryRequest):
    return await query_inerface(request)


@app.post("/get_balances")
async def call_get_balances(request: QueryMapRequest):
    return await get_balances(request)


@app.post("/query_map")
async def call_query_map_api(request: QueryMapRequest):
    return await query_map_interface(request)
