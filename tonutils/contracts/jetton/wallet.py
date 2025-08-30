import typing as t

from pytoniq_core import Address, Cell

from .get_methods import JettonWalletGetMethods
from ..base import BaseContract
from ...types import (
    JettonWalletStandardData,
    JettonWalletStablecoinData,
    JettonWalletStablecoinV2Data,
    JettonWalletVersion,
)

D = t.TypeVar(
    "D",
    bound=t.Union[
        JettonWalletStandardData,
        JettonWalletStablecoinData,
        JettonWalletStablecoinV2Data,
    ],
)


class BaseJettonWallet(BaseContract[D]):
    _data_model: t.Type[D]

    @property
    def jetton_balance(self) -> int:
        return self.state_data.balance

    @property
    def owner_address(self) -> Address:
        return self.state_data.owner_address

    @property
    def jetton_master_address(self) -> Address:
        return self.state_data.jetton_master_address

    async def get_wallet_data(self) -> t.Tuple[
        int,
        Address,
        Address,
        Cell,
    ]:
        method_result = await JettonWalletGetMethods.get_wallet_data(
            client=self.client,
            address=self.address,
        )
        return (
            method_result[0],
            method_result[1],
            method_result[2],
            method_result[3],
        )


class JettonWalletStandard(BaseJettonWallet[JettonWalletStandardData]):
    _data_model = JettonWalletStandardData
    VERSION = JettonWalletVersion.JettonWalletStandard


class JettonWalletStablecoin(BaseJettonWallet[JettonWalletStablecoinData]):
    _data_model = JettonWalletStablecoinData
    VERSION = JettonWalletVersion.JettonWalletStablecoin

    async def get_status(self) -> int:
        return await JettonWalletGetMethods.get_status(
            client=self.client,
            address=self.address,
        )


class JettonWalletStablecoinV2(BaseJettonWallet[JettonWalletStablecoinV2Data]):
    _data_model = JettonWalletStablecoinV2Data
    VERSION = JettonWalletVersion.JettonWalletStablecoinV2
