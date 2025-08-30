from unittest import TestCase

from pytoniq_core import Address

from tests.helpers import ClientTestCase
from tonutils.contracts import (
    JettonMasterStandard,
    JettonMasterStablecoin,
    JettonMasterStablecoinV2,
    JettonWalletStandard,
)
from tonutils.types import (
    ClientType,
    OnchainContent,
    OffchainContent,
    JettonMasterStandardData,
    JettonMasterStablecoinData,
)

JETTON_MASTER_STANDARD_ADDRESS = Address(
    "EQAL6e1UNPFksn8198qOD6KICnplw6f9cMIFuQW3xV9ld3Ro"
)
JETTON_MASTER_STABLECOIN_ADDRESS = Address(
    "EQD3r1oCVcarXV7yENw6PQC2Y7Yd29enyseEIlARRC4-HtAp"
)
JETTON_MASTER_STABLECOIN_V2_ADDRESS = Address(
    "EQBNIsRjNUVc0xxexfNMHcXJoqLq5YNWPM-7AGrniObnaW_t"
)


JETTON_WALLET_STANDARD_ADDRESS = Address(
    "UQAobSyS2pmMT8-C0nQlfPo9ClK9QSzoPe5kpASnzqq_Mfcp"
)
JETTON_WALLET_STABLECOIN_ADDRESS = Address(
    "EQDMQLgHL8FeB7-BcpOO--Pw5gARzDd590obCKekFpTQPIyR"
)
JETTON_WALLET_STABLECOIN_V2_ADDRESS = Address(
    "EQACwaP5j9Ok2GSU751e-mBpd4dfyaJRJM3fwuaL5Z6vTLQc"
)


JETTON_WALLET_STANDARD_OWNER_ADDRESS = Address(
    "UQAobSyS2pmMT8-C0nQlfPo9ClK9QSzoPe5kpASnzqq_Mfcp"
)
JETTON_WALLET_STABLECOIN_OWNER_ADDRESS = Address(
    "UQDgE9QT-wINxuil1YxzzsAsUaSSVrC_8Q65Lx5BkGrikNio"
)
JETTON_WALLET_STABLECOIN_V2_OWNER_ADDRESS = Address(
    "UQACijaJQNnZx4PRvbAVo4ReYS81s-AYsZ1G5h5P_uLR2TuM"
)


class TestsNFTContracts(TestCase):

    def test_calcualte_nft_item_address(self) -> None:
        pass


class TestsNFTContractsTonapi(ClientTestCase):
    CLIENT_TYPE = ClientType.TONAPI
    IS_TESTNET = False
    RPS = 1

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()

        self.jetton_master_standard: JettonMasterStandard = (
            await JettonMasterStandard.from_address(
                client=self.client,
                address=JETTON_MASTER_STANDARD_ADDRESS,
            )
        )
        self.assertIsInstance(
            self.jetton_master_standard.content, (OnchainContent, OffchainContent)
        )
        self.assertIsInstance(
            self.jetton_master_standard.state_data, JettonMasterStandardData
        )

        self.jetton_master_stablecoin: JettonMasterStablecoin = (
            await JettonMasterStablecoin.from_address(
                client=self.client,
                address=JETTON_MASTER_STABLECOIN_ADDRESS,
            )
        )
        self.assertIsInstance(self.jetton_master_stablecoin.content, OffchainContent)
        self.assertIsInstance(
            self.jetton_master_stablecoin.state_data, JettonMasterStablecoinData
        )

        self.jetton_master_stablecoin_v2: JettonMasterStablecoinV2 = (
            await JettonMasterStablecoinV2.from_address(
                client=self.client,
                address=JETTON_MASTER_STABLECOIN_V2_ADDRESS,
            )
        )
        self.assertIsInstance(self.jetton_master_stablecoin_v2.content, OffchainContent)
        self.assertIsInstance(
            self.jetton_master_stablecoin_v2.state_data, JettonMasterStablecoinData
        )

        self.jetton_wallet_standard: JettonWalletStandard = (
            await JettonWalletStandard.from_address(
                client=self.client,
                address=JETTON_WALLET_STANDARD_ADDRESS,
            )
        )

    async def test(self): ...
