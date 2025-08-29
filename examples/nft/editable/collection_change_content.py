from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2
from tonutils.types import (
    NFTCollectionContent,
    NFTCollectionEditableChangeContentBody,
    OffchainCommonContent,
    OffchainContent,
    RoyaltyParams,
)
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

OWNER_ADDRESS = "UQ..."
ROYALTY_ADDRESS = "UQ..."
NFT_COLLECTION_ADDRESS = "EQ..."

# https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-collection-metadata-example-offchain
COLLECTION_URI = "https://example.com/collection.json"
ITEMS_SUFFIX_URI = "https://example.com/items/"

ROYALTY = 50  # 5% royalty
ROYALTY_DENOMINATOR = 1000


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    nft_collection_content = NFTCollectionContent(
        content=OffchainContent(uri=COLLECTION_URI),
        common_content=OffchainCommonContent(suffix_uri=ITEMS_SUFFIX_URI),
    )
    royalty_params = RoyaltyParams(
        royalty=ROYALTY,
        denominator=ROYALTY_DENOMINATOR,
        address=ROYALTY_ADDRESS,
    )
    body = NFTCollectionEditableChangeContentBody(
        content=nft_collection_content,
        royalty_params=royalty_params,
    )

    tx_hash = await wallet.transfer(
        destination=NFT_COLLECTION_ADDRESS,
        body=body.serialize(),
        amount=to_nano(0.05),
    )

    nft_collection_address = Address(NFT_COLLECTION_ADDRESS).to_str(
        is_test_only=IS_TESTNET
    )

    print(f"NFT collection address: {nft_collection_address}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
