from pydantic import BaseModel
from substrateinterface import SubstrateInterface
from retry import retry

substrate_instance = SubstrateInterface(
    url="wss://testnet.nimble.technology"
)


@retry(delay=2, tries=3, backoff=2, max_delay=4)
def make_substrate_call_with_retry(
    substrate,
    module,
    storage_function,
    address,
    block
):
    if block is None:
        block_hash = substrate.get_block_hash(block)
    else:
        block_hash = None
    return substrate.query(
        module=module,
        storage_function=storage_function,
        params=[address],
        block_hash=block_hash,
    )


class QueryRequest(BaseModel):
    substrate_instance: SubstrateInterface
    module: str
    storage_function: str
    address: str
    block: str


async def query_interface(request: QueryRequest) -> dict:
    return make_substrate_call_with_retry(
        substrate_instance,
        request.module,
        request.storage_function,
        request.address,
        request.block
    )
