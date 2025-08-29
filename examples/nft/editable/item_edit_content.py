from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2
from tonutils.types import (
    NFTItemEditableEditContentBody,
    OffchainItemContent,
)
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

NFT_ITEM_ADDRESS = "EQ..."

PREFIX_URI = "0.json"


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    nft_item_content = OffchainItemContent(prefix_uri=PREFIX_URI)
    body = NFTItemEditableEditContentBody(content=nft_item_content)

    tx_hash = await wallet.transfer(
        destination=NFT_ITEM_ADDRESS,
        body=body.serialize(),
        amount=to_nano(0.05),
    )

    nft_item_address = Address(NFT_ITEM_ADDRESS).to_str(is_test_only=IS_TESTNET)

    print(f"NFT item address: {nft_item_address}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
