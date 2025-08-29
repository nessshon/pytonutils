from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2
from tonutils.utils import to_amount

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

WALLET_ADDRESS = "UQ..."


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet = await WalletV4R2.from_address(client, WALLET_ADDRESS)

    # Or initialize from a mnemonic phrase:
    # wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    # Load the latest on-chain state:
    await wallet.refresh()

    balance = wallet.balance
    ton_balance = to_amount(balance, decimals=9, precision=4)

    print(f"Wallet balance: {balance}")
    print(f"Wallet balance: {ton_balance} TON")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
