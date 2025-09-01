from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import (
    NFTCollectionStandard,
    NFTItemStandard,
    WalletV4R2,
)
from tonutils.types import (
    NFTCollectionContent,
    NFTCollectionData,
    OffchainCommonContent,
    OffchainContent,
    RoyaltyParams,
)
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

OWNER_ADDRESS = Address("UQ...")

# https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-collection-metadata-example-offchain
COLLECTION_URI = "https://example.com/collection.json"
ITEMS_SUFFIX_URI = "https://example.com/items/"

ROYALTY = 50  # 5% royalty
ROYALTY_DENOMINATOR = 1000
ROYALTY_ADDRESS = Address("UQ...")


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    nft_item_code = NFTItemStandard.get_default_code()

    nft_collection_content = NFTCollectionContent(
        content=OffchainContent(uri=COLLECTION_URI),
        common_content=OffchainCommonContent(suffix_uri=ITEMS_SUFFIX_URI),
    )
    royalty_params = RoyaltyParams(
        royalty=ROYALTY,
        denominator=ROYALTY_DENOMINATOR,
        address=ROYALTY_ADDRESS,
    )
    nft_collection_data = NFTCollectionData(
        owner_address=OWNER_ADDRESS,
        content=nft_collection_content,
        royalty_params=royalty_params,
        nft_item_code=nft_item_code,
    )
    nft_collection = NFTCollectionStandard.from_data(
        client=client,
        data=nft_collection_data.serialize(),
    )

    nft_collection_address = nft_collection.address.to_str(is_test_only=IS_TESTNET)

    tx_hash = await wallet.transfer(
        destination=nft_collection.address,
        amount=to_nano(0.05),
        state_init=nft_collection.state_init,
    )

    print(f"NFT collection address: {nft_collection_address}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
