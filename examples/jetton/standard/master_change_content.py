from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2
from tonutils.types import (
    JettonStandardChangeContentBody,
    OffchainContent,
)
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

JETTON_MASTER_ADDRESS = Address("EQ...")

# https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#jetton-metadata-example-offchain
JETTON_MASTER_URI = "https://example.com/jetton.json"


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    jetton_master_content = OffchainContent(uri=JETTON_MASTER_URI)
    body = JettonStandardChangeContentBody(content=jetton_master_content)

    tx_hash = await wallet.transfer(
        destination=JETTON_MASTER_ADDRESS,
        body=body.serialize(),
        amount=to_nano(0.05),
    )

    jetton_master_address = JETTON_MASTER_ADDRESS.to_str(is_test_only=IS_TESTNET)

    print(f"Jetton master address: {jetton_master_address}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
