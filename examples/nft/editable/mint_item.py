from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import (
    NFTCollectionEditable,
    NFTItemEditable,
    WalletV4R2,
)
from tonutils.types import (
    NFTCollectionMintItemBody,
    NFTItemEditableMintRef,
    OffchainItemContent,
)
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

OWNER_ADDRESS = Address("UQ...")
EDITOR_ADDRESS = Address("UQ...")
NFT_COLLECTION_ADDRESS = Address("EQ...")

NFT_ITEM_INDEX = 0
NFT_ITEM_PREFIX_URI = f"{NFT_ITEM_INDEX}.json"


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    nft_item_code = NFTItemEditable.get_default_code()
    nft_item_content = OffchainItemContent(prefix_uri=NFT_ITEM_PREFIX_URI)

    nft_item_ref = NFTItemEditableMintRef(
        owner_address=OWNER_ADDRESS,
        editor_address=EDITOR_ADDRESS,
        content=nft_item_content,
    )
    body = NFTCollectionMintItemBody(
        item_index=NFT_ITEM_INDEX,
        item_ref=nft_item_ref.serialize(),
        forward_amount=1,
    )

    tx_hash = await wallet.transfer(
        destination=NFT_COLLECTION_ADDRESS,
        amount=to_nano(0.05),
        body=body.serialize(),
    )

    calculated_nft_item_address = NFTCollectionEditable.calculate_nft_item_address(
        index=NFT_ITEM_INDEX,
        nft_item_code=nft_item_code,
        collection_address=NFT_COLLECTION_ADDRESS,
    )
    nft_item_address = calculated_nft_item_address.to_str(is_test_only=IS_TESTNET)

    print(f"NFT item address: {nft_item_address}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
