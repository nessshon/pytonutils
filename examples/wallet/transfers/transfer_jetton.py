from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import WalletV4R2
from tonutils.types import TransferJettonMessage
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

DESTINATION_ADDRESS = Address("UQ...")
JETTON_MASTER_ADDRESS = Address("EQ...")

JETTON_AMOUNT_TO_SEND = to_nano(1000)


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    tx_hash = await wallet.transfer_message(
        TransferJettonMessage(
            destination=DESTINATION_ADDRESS,
            jetton_amount=JETTON_AMOUNT_TO_SEND,
            jetton_master_address=JETTON_MASTER_ADDRESS,
            forward_payload="Hello from tonutils!",
        )
    )

    print(f"Wallet address: {wallet.address.to_str(is_bounceable=False)}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
