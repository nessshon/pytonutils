from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2
from tonutils.types import NFTCollectionEditableChangeOwnerBody
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

OWNER_ADDRESS = "UQ..."
NFT_COLLECTION_ADDRESS = "EQ..."


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    body = NFTCollectionEditableChangeOwnerBody(owner_address=OWNER_ADDRESS)

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
