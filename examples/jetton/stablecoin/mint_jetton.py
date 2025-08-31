from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2
from tonutils.types import (
    JettonInternalTransferBody,
    JettonMintBody,
)
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

DESTINATION_ADDRESS = Address("UQ...")
JETTON_MASTER_ADDRESS = Address("EQ...")

JETTON_AMOUNT_TO_MINT = to_nano(1000)


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    body = JettonMintBody(
        internal_transfer=JettonInternalTransferBody(
            jetton_amount=JETTON_AMOUNT_TO_MINT,
            forward_amount=to_nano(0.05),
        ),
        destination_address=DESTINATION_ADDRESS,
        forward_amount=to_nano(0.1),
    )
    tx_hash = await wallet.transfer(
        destination=JETTON_MASTER_ADDRESS,
        amount=to_nano(0.15),
        body=body.serialize(),
    )

    jetton_master_address = JETTON_MASTER_ADDRESS.to_str(is_test_only=IS_TESTNET)

    print(f"Jetton master address: {jetton_master_address}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
