from unittest import TestCase

from pytoniq_core import Address, Cell

from tests.helpers import ClientTestCase
from tonutils.contracts import (
    JettonMasterStandard,
    JettonMasterStablecoin,
    JettonMasterStablecoinV2,
    JettonWalletStandard,
    JettonWalletStablecoin,
    JettonWalletStablecoinV2,
)
from tonutils.types import (
    ClientType,
    OnchainContent,
    OffchainContent,
    JettonMasterStandardData,
    JettonMasterStablecoinData,
    JettonWalletStandardData,
    JettonWalletStablecoinData,
    JettonWalletStablecoinV2Data,
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
    "EQAitUm4OeSc069m3hpzjoLLHox8mCKjck9rjlwPKc4akfXL"
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


class TestsJettonContracts(TestCase):

    def test_calculate_user_jetton_wallet_address(self) -> None:
        calculated_address_standard = (
            JettonMasterStandard.calculate_user_jetton_wallet_address(
                owner_address=JETTON_WALLET_STANDARD_OWNER_ADDRESS,
                jetton_master_address=JETTON_MASTER_STANDARD_ADDRESS,
                jetton_wallet_code=JettonWalletStandard.get_default_code(),
            )
        )
        self.assertEqual(
            calculated_address_standard,
            JETTON_WALLET_STANDARD_ADDRESS,
        )

        calculated_address_stablecoin = (
            JettonMasterStablecoin.calculate_user_jetton_wallet_address(
                owner_address=JETTON_WALLET_STABLECOIN_OWNER_ADDRESS,
                jetton_master_address=JETTON_MASTER_STABLECOIN_ADDRESS,
                jetton_wallet_code=JettonWalletStablecoin.get_default_code(),
            )
        )
        self.assertEqual(
            calculated_address_stablecoin,
            JETTON_WALLET_STABLECOIN_ADDRESS,
        )

        calculated_address_stablecoin_v2 = (
            JettonMasterStablecoinV2.calculate_user_jetton_wallet_address(
                owner_address=JETTON_WALLET_STABLECOIN_V2_OWNER_ADDRESS,
                jetton_master_address=JETTON_MASTER_STABLECOIN_V2_ADDRESS,
                jetton_wallet_code=JettonWalletStablecoinV2.get_default_code(),
            )
        )
        self.assertEqual(
            calculated_address_stablecoin_v2,
            JETTON_WALLET_STABLECOIN_V2_ADDRESS,
        )


class TestsJettonContractsTonapi(ClientTestCase):
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
            self.jetton_master_standard.content,
            (OnchainContent, OffchainContent),
        )
        self.assertIsInstance(
            self.jetton_master_standard.state_data,
            JettonMasterStandardData,
        )
        self.jetton_master_stablecoin: JettonMasterStablecoin = (
            await JettonMasterStablecoin.from_address(
                client=self.client,
                address=JETTON_MASTER_STABLECOIN_ADDRESS,
            )
        )
        self.assertIsInstance(
            self.jetton_master_stablecoin.content,
            OffchainContent,
        )
        self.assertIsInstance(
            self.jetton_master_stablecoin.state_data,
            JettonMasterStablecoinData,
        )
        self.jetton_master_stablecoin_v2: JettonMasterStablecoinV2 = (
            await JettonMasterStablecoinV2.from_address(
                client=self.client,
                address=JETTON_MASTER_STABLECOIN_V2_ADDRESS,
            )
        )
        self.assertIsInstance(
            self.jetton_master_stablecoin_v2.content,
            OffchainContent,
        )
        self.assertIsInstance(
            self.jetton_master_stablecoin_v2.state_data,
            JettonMasterStablecoinData,
        )

        self.jetton_wallet_standard: JettonWalletStandard = (
            await JettonWalletStandard.from_address(
                client=self.client,
                address=JETTON_WALLET_STANDARD_ADDRESS,
            )
        )
        self.assertIsInstance(
            self.jetton_wallet_standard.state_data,
            JettonWalletStandardData,
        )
        self.jetton_wallet_stablecoin: JettonWalletStablecoin = (
            await JettonWalletStablecoin.from_address(
                client=self.client,
                address=JETTON_WALLET_STABLECOIN_ADDRESS,
            )
        )
        self.assertIsInstance(
            self.jetton_wallet_stablecoin.state_data,
            JettonWalletStablecoinData,
        )
        self.jetton_wallet_stablecoin_v2: JettonWalletStablecoinV2 = (
            await JettonWalletStablecoinV2.from_address(
                client=self.client,
                address=JETTON_WALLET_STABLECOIN_V2_ADDRESS,
            )
        )
        self.assertIsInstance(
            self.jetton_wallet_stablecoin_v2.state_data,
            JettonWalletStablecoinV2Data,
        )

    async def test_jetton_master_get_jetton_data(self) -> None:
        total_supply, mintabe, admin_address, content, jetton_wallet_code = (
            await self.jetton_master_standard.get_jetton_data()
        )
        self.assertIsInstance(total_supply, int)
        self.assertIsInstance(mintabe, bool)
        self.assertIsInstance(admin_address, Address)
        self.assertIsInstance(content, (OnchainContent, OffchainContent))
        self.assertIsInstance(jetton_wallet_code, Cell)

    async def test_jetton_master_get_wallet_address(self) -> None:
        wallet_address = await self.jetton_master_standard.get_wallet_address(
            owner_address=JETTON_WALLET_STANDARD_OWNER_ADDRESS,
        )
        self.assertEqual(wallet_address, JETTON_WALLET_STANDARD_ADDRESS)

    async def test_jetton_master_get_next_admin_address(self) -> None:
        next_admin_address = (
            await self.jetton_master_stablecoin.get_next_admin_address()
        )
        self.assertIsInstance(next_admin_address, type(None))

    async def test_jetton_wallet_get_wallet_data(self) -> None:
        balance, owner_address, jetton_master_address, jetton_wallet_code = (
            await self.jetton_wallet_standard.get_wallet_data()
        )
        self.assertIsInstance(balance, int)
        self.assertEqual(owner_address, JETTON_WALLET_STANDARD_OWNER_ADDRESS)
        self.assertEqual(jetton_master_address, JETTON_MASTER_STANDARD_ADDRESS)
        self.assertIsInstance(jetton_wallet_code, Cell)

    async def test_jetton_wallet_get_status(self) -> None:
        status = await self.jetton_wallet_stablecoin.get_status()
        self.assertIsInstance(status, int)


class TestsJettonContractsToncenter(TestsJettonContractsTonapi):
    CLIENT_TYPE = ClientType.TONCENTER


class TestsJettonContractsLiteserver(TestsJettonContractsTonapi):
    CLIENT_TYPE = ClientType.LITESERVER
