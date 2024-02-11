from substrateinterface import SubstrateInterface
from retry import retry
from ..config import SUBSTRATE_URL

substrate_instance = SubstrateInterface(url=SUBSTRATE_URL)


@retry(delay=2, tries=3, backoff=2, max_delay=4)
def make_substrate_call_with_retry(
    substrate,
):
    return substrate.get_block_number(None)


async def get_block_number() -> int:
    return make_substrate_call_with_retry(substrate_instance)
