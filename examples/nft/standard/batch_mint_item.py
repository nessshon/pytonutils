from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import (
    NFTCollectionStandard,
    NFTItemStandard,
    WalletV4R2,
)
from tonutils.types import (
    NFTCollectionBatchMintItemBody,
    NFTItemStandardMintRef,
    OffchainItemContent,
)
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

NFT_COLLECTION_ADDRESS = Address("EQ...")

MINT_FROM_INDEX = 0
NFT_ITEM_OWNERS = [
    Address("UQ..."),
    Address("UQ..."),
]


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    nft_item_code = NFTItemStandard.get_default_code()
    nft_items_count = len(NFT_ITEM_OWNERS)
    nft_items_refs = []

    for nft_item_index, owner_address in enumerate(
        NFT_ITEM_OWNERS, start=MINT_FROM_INDEX
    ):
        nft_item_ref = NFTItemStandardMintRef(
            owner_address=owner_address,
            content=OffchainItemContent(prefix_uri=f"{nft_item_index}.json"),
        )
        nft_items_refs.append(nft_item_ref.serialize())

    body = NFTCollectionBatchMintItemBody(
        items_refs=nft_items_refs,
        from_index=MINT_FROM_INDEX,
        forward_amount=to_nano(0.01),
    )

    tx_hash = await wallet.transfer(
        destination=NFT_COLLECTION_ADDRESS,
        amount=to_nano(0.025) * nft_items_count,
        body=body.serialize(),
    )

    for nft_item_index in range(MINT_FROM_INDEX, MINT_FROM_INDEX + nft_items_count):
        calculated_nft_item_address = NFTCollectionStandard.calculate_nft_item_address(
            index=nft_item_index,
            nft_item_code=nft_item_code,
            collection_address=NFT_COLLECTION_ADDRESS,
        )
        nft_item_address = calculated_nft_item_address.to_str(is_test_only=IS_TESTNET)
        print(f"NFT item {nft_item_index} address: {nft_item_address}")

    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
