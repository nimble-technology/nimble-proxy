from pydantic import BaseModel
from substrateinterface import SubstrateInterface
from retry import retry
from typing import Optional, List

substrate_instance = SubstrateInterface(
    url="wss://testnet.nimble.technology"
)


@retry(delay=2, tries=3, backoff=2, max_delay=4)
def make_substrate_call_with_retry(
    method: str,
    params: List,
    block: Optional[int] = None
) -> dict:
    if block is not None:
        block_hash = substrate_instance.get_block_hash(block)
    else:
        block_hash = None

    if block_hash:
        params = params + [block_hash]

    json_body = substrate_instance.rpc_request(method=method, params=params)
    return json_body["result"]


class RpcRequestRequest(BaseModel):
    method: str
    encoded_key: Optional[str] = None
    uid: Optional[int] = None
    netuid: Optional[int] = None
    data: Optional[str] = None
    block: Optional[int] = None


async def rpc_request_interface(request: RpcRequestRequest) -> dict:
    params = []
    if request.data is not None:
        params = [request.data]
    elif request.netuid is not None and request.uid is not None:
        params = [request.netuid, request.uid]
    elif request.netuid is not None:
        params = [request.netuid]
    elif request.encoded_key is not None:
        params = [request.encoded_key]

    return await make_substrate_call_with_retry(
        request.method, params, request.block
    )


async def state_call(request: RpcRequestRequest) -> Optional[object]:
    result = await rpc_request_interface(request)
    return result
