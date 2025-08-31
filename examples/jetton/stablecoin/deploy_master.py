from pytoniq_core import Address

from tonutils.clients import ToncenterClient
from tonutils.contracts import (
    JettonMasterStablecoinV2,
    JettonWalletStablecoinV2,
    WalletV4R2,
)
from tonutils.types import (
    OffchainContent,
    JettonMasterStablecoinData,
    JettonTopUpBody,
)
from tonutils.utils import to_nano

IS_TESTNET = True

MNEMONIC = "word1 word2 word3 ..."

ADMIN_ADDRESS = Address("UQ...")

# https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#jetton-metadata-example-offchain
JETTON_MASTER_URI = "https://example.com/jetton.json"


async def main() -> None:
    client = ToncenterClient(is_testnet=IS_TESTNET, rps=1)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    jetton_wallet_code = JettonWalletStablecoinV2.get_default_code()

    jetton_master_data = JettonMasterStablecoinData(
        admin_address=ADMIN_ADDRESS,
        jetton_wallet_code=jetton_wallet_code,
        content=OffchainContent(uri=JETTON_MASTER_URI),
    )
    jetton_master = JettonMasterStablecoinV2.from_data(
        client=client,
        data=jetton_master_data.serialize(),
    )
    body = JettonTopUpBody()

    tx_hash = await wallet.transfer(
        destination=jetton_master.address,
        amount=to_nano(0.05),
        body=body.serialize(),
        state_init=jetton_master.state_init,
    )

    jetton_master_address = jetton_master.address.to_str(is_test_only=IS_TESTNET)

    print(f"Jetton master address: {jetton_master_address}")
    print(f"Transaction hash: {tx_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
