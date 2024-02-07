from pydantic import BaseModel
from substrateinterface import SubstrateInterface
from retry import retry
from typing import Optional

substrate_instance = SubstrateInterface(
    url="wss://testnet.nimble.technology"
)


@retry(delay=2, tries=3, backoff=2, max_delay=4)
def make_substrate_call_with_retry(
    substrate,
    module_name,
    constant_name,
    block
):
    if block is not None:
        block_hash = substrate.get_block_hash(block)
    else:
        block_hash = None
    return substrate.get_constant(
        module_name=module_name,
        constant_name=constant_name,
        block_hash=block_hash,
    )


class GetConstantRequest(BaseModel):
    substrate_instance: str
    module_name: str
    constant_name: str
    block: Optional[int] = None


async def query_map_interface(request: GetConstantRequest) -> Optional[object]:
    return make_substrate_call_with_retry(
        substrate_instance,
        request.module_name,
        request.constant_name,
        request.block
    )