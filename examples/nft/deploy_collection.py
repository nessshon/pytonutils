from tonutils.clients import ToncenterClient
from tonutils.contracts import (
    NFTCollectionEditable,
    NFTItemEditable,
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

OWNER_ADDRESS = "UQ..."
ROYALTY_ADDRESS = "UQ..."

# URI of the collection metadata
# https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-collection-metadata-example-offchain
URI = "ipfs://bafkreiadoenfdgu46gu4l2l472ud5slzvoyzb3bzcpu657onm75is7sxai?filename=collection.json"
SUFFIX_URI = "ipfs://bafybeibhklflai76uc2obpcp2wkqoilzntx4hpb6vxl3eqdb4w5jk4yog4/"

ROYALTY = 50  # 5% royalty
ROYALTY_DENOMINATOR = 1000


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    nft_item_code = NFTItemEditable.get_default_code()

    collection_content = NFTCollectionContent(
        content=OffchainContent(uri=URI),
        common_content=OffchainCommonContent(suffix_uri=SUFFIX_URI),
    )
    royalty_params = RoyaltyParams(
        royalty=ROYALTY,
        denominator=ROYALTY_DENOMINATOR,
        address=ROYALTY_ADDRESS,
    )
    collection_data = NFTCollectionData(
        owner_address=OWNER_ADDRESS,
        content=collection_content,
        royalty_params=royalty_params,
        nft_item_code=nft_item_code,
    )
    collection = NFTCollectionEditable.from_data(
        client=client,
        data=collection_data.serialize(),
    )

    collection_address = collection.address.to_str(is_test_only=IS_TESTNET)

    tx_hash = await wallet.transfer(
        destination=collection.address,
        amount=to_nano(0.05),
        state_init=collection.state_init,
    )

    print(f"NFT Collection address: {collection_address}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
