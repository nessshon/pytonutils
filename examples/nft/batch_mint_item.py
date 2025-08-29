from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2
from tonutils.types import (
    NFTCollectionBatchMintItemBody,
    NFTItemEditableMintRef,
    OffchainItemContent,
)
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

NFT_COLLECTION_ADDRESS = "EQ..."

# Starting index for minting items
FROM_INDEX = 0

#
OWNERS_AND_EDITORS = [
    ("UQ...", "UQ..."),
    ("UQ...", "UQ..."),
]

#
FORWARD_AMOUNT_PER_ITEM = to_nano(0.25)


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    nft_items_refs = []
    for index, (owner_address, editor_address) in enumerate(
        OWNERS_AND_EDITORS, start=FROM_INDEX
    ):
        nft_item_ref = NFTItemEditableMintRef(
            owner_address=owner_address,
            editor_address=editor_address,
            content=OffchainItemContent(prefix_uri=f"{index}.json"),
        )
        nft_items_refs.append(nft_item_ref.serialize())

    body = NFTCollectionBatchMintItemBody(
        items_refs=nft_items_refs,
        from_index=FROM_INDEX,
        forward_amount=FORWARD_AMOUNT_PER_ITEM,
    )

    nft_items_count = len(OWNERS_AND_EDITORS)
    value = FORWARD_AMOUNT_PER_ITEM * nft_items_count

    tx_hash = await wallet.transfer(
        destination=NFT_COLLECTION_ADDRESS,
        amount=value,
        body=body.serialize(),
    )

    print(f"Minted {nft_items_count} items in collection {NFT_COLLECTION_ADDRESS}")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
