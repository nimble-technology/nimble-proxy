from pydantic import BaseModel
from substrateinterface import SubstrateInterface
from retry import retry
from ..config import SUBSTRATE_URL

substrate_instance = SubstrateInterface(url=SUBSTRATE_URL)


@retry(delay=2, tries=3, backoff=2, max_delay=4)
def make_substrate_call_with_retry(
    substrate,
    module,
    extrinsic
):
    return substrate.get_metadata_call_function(
        module,
        extrinsic
    )


class GetMetadataCallRequest(BaseModel):
    substrate_instance: str
    module: str
    extrinsic: str


async def get_metadata_call_function(request: GetMetadataCallRequest) -> dict:
    return make_substrate_call_with_retry(
        substrate_instance,
        request.module,
        request.extrinsic
    )
