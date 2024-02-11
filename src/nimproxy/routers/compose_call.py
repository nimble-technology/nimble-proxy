from typing import Optional, Tuple
from pydantic import BaseModel
from substrateinterface import SubstrateInterface
from retry import retry
from ..config import SUBSTRATE_URL

substrate_instance = SubstrateInterface(url=SUBSTRATE_URL)


@retry(delay=2, tries=3, backoff=2, max_delay=4)
def make_substrate_call_with_retry(
    substrate,
    module,
    function_name,
    call_params,
    keypair,
    wait_for_inclusion,
    wait_for_finalization,
):
    call = substrate.compose_call(
        call_module=module,
        call_function=function_name,
        call_params=call_params,
    )
    extrinsic = substrate.create_signed_extrinsic(
        call=call,
        keypair=keypair,
    )
    response = substrate.submit_extrinsic(
        extrinsic,
        wait_for_inclusion=wait_for_inclusion,
        wait_for_finalization=wait_for_finalization,
    )
    # We only wait here if we expect finalization.
    if not wait_for_finalization and not wait_for_inclusion:
        return True, None

    response.process_events()
    if response.is_success:
        return True, None
    else:
        return False, response.error_message


class ComposeCallRequest(BaseModel):
    substrate_instance: str
    module: str
    function_name: str
    call_params: dict
    wait_for_inclusion: bool = False
    wait_for_finalization: bool = True
    keypair: str
    version_key: int = 0


async def compose_call_interface(
    request_data: ComposeCallRequest,
) -> Tuple[bool, Optional[str]]:
    return make_substrate_call_with_retry(
        substrate_instance,
        request_data.module,
        request_data.function_name,
        request_data.call_params,
        request_data.keypair,
        request_data.wait_for_inclusion,
        request_data.wait_for_finalization,
    )
