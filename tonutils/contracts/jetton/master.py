import abc
import typing as t

from pytoniq_core import (
    Address,
    Cell,
    Slice,
    StateInit,
    begin_cell,
)

from .get_methods import JettonMasterGetMethods
from ..base import BaseContract
from ...types import (
    AddressLike,
    ContentLike,
    MetadataPrefix,
    OnchainContent,
    OffchainContent,
    JettonMasterStandardData,
    JettonMasterStablecoinData,
    JettonMasterVersion,
    WorkchainID,
)
from ...utils import to_cell, cell_hash

D = t.TypeVar(
    "D",
    bound=t.Union[
        JettonMasterStandardData,
        JettonMasterStablecoinData,
    ],
)
C = t.TypeVar(
    "C",
    bound=t.Union[
        OnchainContent,
        OffchainContent,
    ],
)


DStandard = t.TypeVar("DStandard", bound=JettonMasterStandardData)
DStablecoin = t.TypeVar("DStablecoin", bound=JettonMasterStablecoinData)

CStandard = t.TypeVar("CStandard", bound=ContentLike)
CStablecoin = t.TypeVar("CStablecoin", bound=OnchainContent)


class BaseJettonMaster(BaseContract[D], t.Generic[D, C], abc.ABC):
    _data_model: t.Type[D]

    @property
    def jetton_wallet_code(self) -> Cell:
        return self.state_data.jetton_wallet_code

    @property
    def admin_address(self) -> Address:
        return self.state_data.admin_address

    @property
    def total_supply(self) -> int:
        return self.state_data.total_supply

    @property
    def content(self) -> C:
        return self.state_data.content

    @classmethod
    @abc.abstractmethod
    def _pack_jetton_wallet_data(
        cls,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        jetton_wallet_code: t.Union[Cell, str],
    ) -> Cell: ...

    @classmethod
    def calculate_user_jetton_wallet_address(
        cls,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        jetton_wallet_code: t.Union[Cell, str],
        workchain: WorkchainID = WorkchainID.BASECHAIN,
    ) -> Address:
        code = to_cell(jetton_wallet_code)
        data = cls._pack_jetton_wallet_data(
            owner_address=owner_address,
            jetton_master_address=jetton_master_address,
            jetton_wallet_code=code,
        )
        state_init = StateInit(code=code, data=data)
        return Address((workchain.value, state_init.serialize().hash))

    async def get_wallet_address(self, owner_address: AddressLike) -> Address:
        return await JettonMasterGetMethods.get_wallet_address(
            client=self.client,
            address=self.address,
            owner_address=owner_address,
        )


class JettonMasterStandard(BaseJettonMaster[DStandard, CStandard]):
    _data_model = JettonMasterStandardData
    VERSION = JettonMasterVersion.JettonMasterStandard

    @classmethod
    def _pack_jetton_wallet_data(
        cls,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        jetton_wallet_code: Cell,
        workchain: WorkchainID = WorkchainID.BASECHAIN,
    ) -> Cell:
        cell = begin_cell()
        cell.store_coins(0)
        cell.store_address(owner_address)
        cell.store_address(jetton_master_address)
        cell.store_ref(jetton_wallet_code)
        return cell.end_cell()

    async def get_jetton_data(self) -> t.Tuple[
        int,
        bool,
        Address,
        ContentLike,
        Cell,
    ]:
        method_result = await JettonMasterGetMethods.get_jetton_data(
            client=self.client,
            address=self.address,
        )
        content_cs: Slice = method_result[3].begin_parse()
        return (
            method_result[0],
            bool(method_result[1]),
            method_result[2],
            (
                OnchainContent.deserialize(content_cs, False)
                if content_cs.load_uint(8) == MetadataPrefix.ONCHAIN
                else OffchainContent.deserialize(content_cs, False)
            ),
            method_result[4],
        )


class JettonMasterStablecoin(BaseJettonMaster[DStablecoin, CStablecoin]):
    _data_model = JettonMasterStablecoinData
    VERSION = JettonMasterVersion.JettonMasterStablecoin

    @classmethod
    def _pack_jetton_wallet_data(
        cls,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        jetton_wallet_code: Cell,
    ) -> Cell:
        cell = begin_cell()
        cell.store_uint(0, 4)
        cell.store_coins(0)
        cell.store_address(owner_address)
        cell.store_address(jetton_master_address)
        return cell.end_cell()

    async def get_jetton_data(self) -> t.Tuple[
        int,
        bool,
        Address,
        OnchainContent,
        Cell,
    ]:
        method_result = await JettonMasterGetMethods.get_jetton_data(
            client=self.client,
            address=self.address,
        )
        content_cs: Slice = method_result[3]
        return (
            method_result[0],
            bool(method_result[1]),
            method_result[2],
            OnchainContent.deserialize(content_cs, True),
            method_result[4],
        )

    async def get_next_admin_address(self) -> t.Optional[Address]:
        return await JettonMasterGetMethods.get_next_admin_address(
            client=self.client,
            address=self.address,
        )


class JettonMasterStablecoinV2(JettonMasterStablecoin):
    _SHARD_DEPTH: int = 8
    VERSION = JettonMasterVersion.JettonMasterStablecoinV2

    @classmethod
    def _get_address_shard_prefix(cls, address: AddressLike) -> int:
        if isinstance(address, str):
            address = Address(address)
        cs = address.to_cell().begin_parse()
        return cs.skip_bits(3 + 8).preload_uint(8)

    @classmethod
    def _pack_jetton_wallet_data(
        cls,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        jetton_wallet_code: Cell,
    ) -> Cell:
        cell = begin_cell()
        cell.store_coins(0)
        cell.store_address(owner_address)
        cell.store_address(jetton_master_address)
        return cell.end_cell()

    @classmethod
    def _calculate_jetton_wallet_state_init_cell(
        cls,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        jetton_wallet_code: t.Union[Cell, str],
    ) -> Cell:
        code = to_cell(jetton_wallet_code)
        data = cls._pack_jetton_wallet_data(
            owner_address=owner_address,
            jetton_master_address=jetton_master_address,
            jetton_wallet_code=code,
        )
        cell = begin_cell()
        cell.store_uint(1, 1)
        cell.store_uint(cls._SHARD_DEPTH, 5)
        cell.store_uint(0, 1)
        cell.store_maybe_ref(code)
        cell.store_maybe_ref(data)
        cell.store_uint(0, 1)
        return cell.end_cell()

    @classmethod
    def calculate_user_jetton_wallet_address(
        cls,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        jetton_wallet_code: t.Union[Cell, str],
        workchain: WorkchainID = WorkchainID.BASECHAIN,
    ) -> Address:
        state_init_cell = cls._calculate_jetton_wallet_state_init_cell(
            owner_address=owner_address,
            jetton_master_address=jetton_master_address,
            jetton_wallet_code=jetton_wallet_code,
        )
        shard_prefix = cls._get_address_shard_prefix(owner_address)
        mask = (1 << (256 - cls._SHARD_DEPTH)) - 1
        prefix_less = cell_hash(state_init_cell) & mask
        cell = begin_cell()
        cell.store_uint(4, 3)
        cell.store_int(workchain.value, 8)
        cell.store_uint(shard_prefix, cls._SHARD_DEPTH)
        cell.store_uint(prefix_less, 256 - cls._SHARD_DEPTH)
        return cell.end_cell().begin_parse().load_address()
