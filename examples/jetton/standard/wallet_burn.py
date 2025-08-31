from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import (
    JettonMasterGetMethods,
    WalletV4R2,
)
from tonutils.types import JettonBurnBody
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

JETTON_MASTER_ADDRESS = Address("EQ...")

JETTON_AMOUNT_TO_BURN = to_nano(1000)


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    wallet_address = await JettonMasterGetMethods.get_wallet_address(
        client=client,
        address=JETTON_MASTER_ADDRESS,
        owner_address=wallet.address,
    )

    body = JettonBurnBody(
        jetton_amount=JETTON_AMOUNT_TO_BURN,
        response_address=wallet.address,
    )

    tx_hash = await wallet.transfer(
        destination=wallet_address,
        body=body.serialize(),
        amount=to_nano(0.05),
    )

    jetton_wallet_address = wallet_address.to_str(is_test_only=IS_TESTNET)

    print(f"Jetton wallet address: {jetton_wallet_address}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
