from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1, max_retries=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    # Any outgoing transaction will deploy the wallet contract if needed.
    tx_hash = await wallet.transfer(destination=wallet.address, amount=0)

    print(f"Wallet address: {wallet.address.to_str(is_bounceable=False)}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
