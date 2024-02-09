from typing import List, Dict, Union, Optional
from pydantic import BaseModel
from substrateinterface.base import QueryMapResult, SubstrateInterface
from retry import retry
from ..utils.balance import Balance
from ..config import SUBSTRATE_URL

substrate_instance = SubstrateInterface(url=SUBSTRATE_URL)


@retry(delay=2, tries=3, backoff=2, max_delay=4)
def make_substrate_call_with_retry(
    substrate,
    module,
    storage_function,
    params,
    block
):
    if block is not None:
        block_hash = substrate.get_block_hash(block)
    else:
        block_hash = None
    return substrate.query_map(
        module=module,
        storage_function=storage_function,
        params=params,
        block_hash=block_hash,
    )


class QueryMapRequest(BaseModel):
    substrate_instance: str
    module: str
    storage_function: str
    params: Optional[List[object]] = []
    block: Optional[int] = None


async def get_balances(request: QueryMapRequest) -> Dict[str, Balance]:
    result = make_substrate_call_with_retry(
        substrate_instance,
        request.module,
        request.storage_function,
        request.params,
        request.block
    )
    return_dict = {}
    for r in result:
        bal = Balance(int(r[1]["data"]["free"].value))
        return_dict[r[0].value] = bal
    return return_dict


async def query_map_interface(
        request: QueryMapRequest
) -> Union[Optional[object], QueryMapResult]:
    return make_substrate_call_with_retry(
        substrate_instance,
        request.module,
        request.storage_function,
        request.params,
        request.block
    )
