from fastapi import FastAPI
from pydantic import BaseModel
from src.routers.get_constant import GetConstantRequest, get_constant_interface
from src.routers.query import QueryRequest, get_balance, query_inerface
from src.routers.query_map import (
    QueryMapRequest,
    get_balances,
    query_map_interface
)
from src.routers.rpc_request import (
    RpcRequestRequest,
    rpc_request_interface,
    state_call
)
from src.routers.get_metadata_call_function import (
    GetMetadataCallRequest,
    get_metadata_call_function
)
from src.routers.get_block_number import get_block_number
from routers.compose_call import (
    ComposeCallRequest,
    compose_call_interface
)
from src.routers.get_block_hash import get_block_hash


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


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


@app.post("/compose_call")
async def call_compose_call_api(request: ComposeCallRequest):
    return await compose_call_interface(request)


@app.get("/get_balance")
async def call_get_balance(request: QueryRequest):
    return await get_balance(request)


@app.get("/query")
async def call_query_api(request: QueryRequest):
    return await query_inerface(request)


@app.get("/get_balances")
async def call_get_balances(request: QueryMapRequest):
    return await get_balances(request)


@app.get("/query_map")
async def call_query_map_api(request: QueryMapRequest):
    return await query_map_interface(request)


@app.get("/get_constant")
async def call_get_constant_api(request: GetConstantRequest):
    return await get_constant_interface(request)


@app.get("/rpc_request")
async def call_rpc_request_api(request: RpcRequestRequest):
    return await rpc_request_interface(request)


@app.get("/state_call")
async def call_state_call_api(request: RpcRequestRequest):
    return await state_call(request)


@app.get("/get_metadata")
async def call_get_metadata_api(request: GetMetadataCallRequest):
    return await get_metadata_call_function(request)


@app.get("/get_block_number")
async def call_get_block_number_api():
    return await get_block_number()


@app.get("/get_block_hash/{block_id}")
async def call_get_block_hash_api(block_id: int):
    return await get_block_hash(block_id)
