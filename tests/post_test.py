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
    block_hash
):
    if block_hash is None:
        block_hash = substrate.get_block_hash(None)
    return substrate.query(
        module=module,
        storage_function=storage_function,
        params=[address],
        block_hash=block_hash,
    )


async def get_balance_api(request: dict) -> dict:
    module = request["module"]
    storage_function = request["storage_function"]
    address = request["address"]
    block_hash = request.get("block_hash")

    try:
        result = make_substrate_call_with_retry(
            substrate_instance,
            module,
            storage_function,
            address,
            block_hash
        )
    except Exception as e:
        print(f'Error occurred: {e}')
        return {"balance": "-1", "error": str(e)}

    if result:
        balance = result.value["data"]["free"]
        return {"balance": balance}

    return {"balance": "-1"}
