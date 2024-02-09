from substrateinterface import SubstrateInterface
from retry import retry

substrate_instance = SubstrateInterface(
    url="wss://testnet.nimble.technology"
)


@retry(delay=2, tries=3, backoff=2, max_delay=4)
def make_substrate_call_with_retry(
    substrate,
    block_id
):
    return substrate.get_block_hash(block_id)


async def get_block_hash(block_id: int) -> str:
    return make_substrate_call_with_retry(substrate_instance, block_id)
