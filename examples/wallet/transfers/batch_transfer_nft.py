from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2
from tonutils.types import TransferNFTMessage

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    tx_hash = await wallet.batch_transfer_message(
        [
            TransferNFTMessage(
                destination="UQ...",
                nft_address="EQ...",
                forward_payload="Hello from tonutils!",
            ),
            TransferNFTMessage(
                destination="UQ...",
                nft_address="EQ...",
                forward_payload="Hello from tonutils!",
            ),
            TransferNFTMessage(
                destination="UQ...",
                nft_address="EQ...",
                forward_payload="Hello from tonutils!",
            ),
        ]
    )

    print(f"Wallet address: {wallet.address.to_str(is_bounceable=False)}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
