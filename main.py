from fastapi import FastAPI
from pydantic import BaseModel
from get_constant import GetConstantRequest, get_constant_interface
from query import QueryRequest, get_balance, query_inerface
from query_map import QueryMapRequest, get_balances, query_map_interface
from set_weights import SetWeightsRequest, set_weights
from rpc_request import RpcRequestRequest, rpc_request_interface, state_call
from get_metadata_call_function import (
    GetMetadataCallRequest,
    get_metadata_call_function
)
from get_block_number import get_block_number
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


@app.post("/get_constant")
async def call_get_constant_api(request: GetConstantRequest):
    return await get_constant_interface(request)


@app.post("/rpc_request_interface")
async def call_rpc_request_api(request: RpcRequestRequest):
    return await rpc_request_interface(request)


@app.post("/state_call")
async def call_state_call_api(request: RpcRequestRequest):
    return await state_call(request)


@app.post("/get_metadata")
async def call_get_metadata_api(request: GetMetadataCallRequest):
    return await get_metadata_call_function(request)


@app.post("/get_block_number")
async def call_get_block_number_api():
    return await get_block_number()
