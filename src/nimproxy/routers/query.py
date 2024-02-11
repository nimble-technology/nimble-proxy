from typing import List, Optional
from pydantic import BaseModel
from substrateinterface import SubstrateInterface
from retry import retry
from ..config import SUBSTRATE_URL

substrate_instance = SubstrateInterface(url=SUBSTRATE_URL)


@retry(delay=2, tries=3, backoff=2, max_delay=4)
def make_substrate_call_with_retry(
    substrate, module, storage_function, params, block
):
    if block is not None:
        block_hash = substrate.get_block_hash(block)
    else:
        block_hash = None
    return substrate.query(
        module=module,
        storage_function=storage_function,
        params=params,
        block_hash=block_hash,
    )


class QueryRequest(BaseModel):
    substrate_instance: str
    module: str
    storage_function: str
    params: Optional[List[object]] = []
    block: Optional[int] = None


async def get_balance(request: QueryRequest) -> dict:
    result = make_substrate_call_with_retry(
        substrate_instance,
        request.module,
        request.storage_function,
        request.params,
        request.block,
    )
    if result:
        balance = result.value["data"]["free"]
        return {"balance": balance}

    return {"balance": "-1"}


async def query_inerface(request: QueryRequest) -> Optional[object]:
    return make_substrate_call_with_retry(
        substrate_instance,
        request.module,
        request.storage_function,
        request.params,
        request.block,
    )
