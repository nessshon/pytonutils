from __future__ import annotations

from pytoniq_core import Cell, Slice, begin_cell

from ...types.common import AddressLike
from ...types.tlb.content import (
    ContentLike,
    MetadataPrefix,
    OnchainContent,
    OffchainContent,
)
from ...types.tlb.contract import BaseContractData


class JettonMasterStandardData(BaseContractData):

    def __init__(
        self,
        admin_address: AddressLike,
        content: ContentLike,
        jetton_wallet_code: Cell,
        total_supply: int = 0,
    ) -> None:
        super().__init__()
        self.total_supply = total_supply
        self.admin_address = admin_address
        self.content = content
        self.jetton_wallet_code = jetton_wallet_code

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_coins(self.total_supply)
        cell.store_address(self.admin_address)
        cell.store_ref(self.content.serialize(True))
        cell.store_ref(self.jetton_wallet_code)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonMasterStandardData:
        total_supply = cs.load_coins()
        admin_address = cs.load_address()

        content = cs.load_ref().begin_parse()
        prefix = MetadataPrefix(content.load_uint(8))
        if prefix == MetadataPrefix.ONCHAIN:
            content = OnchainContent.deserialize(content, False)
        else:
            content = OffchainContent.deserialize(content, False)

        return cls(
            total_supply=total_supply,
            admin_address=admin_address,
            content=content,
            jetton_wallet_code=cs.load_ref(),
        )


class JettonMasterStablecoinData(BaseContractData):

    def __init__(
        self,
        admin_address: AddressLike,
        next_admin_address: AddressLike,
        jetton_wallet_code: Cell,
        content: OffchainContent,
        total_supply: int = 0,
    ) -> None:
        super().__init__()
        self.total_supply = total_supply
        self.admin_address = admin_address
        self.next_admin_address = next_admin_address
        self.jetton_wallet_code = jetton_wallet_code
        self.content = content

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_coins(self.total_supply)
        cell.store_address(self.admin_address)
        cell.store_address(self.next_admin_address)
        cell.store_ref(self.jetton_wallet_code)
        cell.store_ref(self.content.serialize(False))
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonMasterStablecoinData:
        return cls(
            total_supply=cs.load_coins(),
            admin_address=cs.load_address(),
            next_admin_address=cs.load_address(),
            jetton_wallet_code=cs.load_ref(),
            content=OffchainContent.deserialize(cs.load_ref().begin_parse(), False),
        )


class JettonWalletStandardData(BaseContractData):

    def __init__(
        self,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        jetton_wallet_code: Cell,
        balance: int = 0,
    ) -> None:
        super().__init__()
        self.balance = balance
        self.owner_address = owner_address
        self.jetton_master_address = jetton_master_address
        self.jetton_wallet_code = jetton_wallet_code

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_coins(self.balance)
        cell.store_address(self.owner_address)
        cell.store_address(self.jetton_master_address)
        cell.store_ref(self.jetton_wallet_code)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonWalletStandardData:
        return cls(
            balance=cs.load_coins(),
            owner_address=cs.load_address(),
            jetton_master_address=cs.load_address(),
            jetton_wallet_code=cs.load_ref(),
        )


class JettonWalletStablecoinData(BaseContractData):

    def __init__(
        self,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        status: int,
        balance: int = 0,
    ) -> None:
        super().__init__()
        self.status = status
        self.balance = balance
        self.owner_address = owner_address
        self.jetton_master_address = jetton_master_address

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.status, 4)
        cell.store_coins(self.balance)
        cell.store_address(self.owner_address)
        cell.store_address(self.jetton_master_address)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonWalletStablecoinData:
        return cls(
            status=cs.load_uint(4),
            balance=cs.load_coins(),
            owner_address=cs.load_address(),
            jetton_master_address=cs.load_address(),
        )


class JettonWalletStablecoinV2Data(BaseContractData):

    def __init__(
        self,
        owner_address: AddressLike,
        jetton_master_address: AddressLike,
        balance: int = 0,
    ) -> None:
        super().__init__()
        self.balance = balance
        self.owner_address = owner_address
        self.jetton_master_address = jetton_master_address

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_coins(self.balance)
        cell.store_address(self.owner_address)
        cell.store_address(self.jetton_master_address)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonWalletStablecoinV2Data:
        return cls(
            balance=cs.load_coins(),
            owner_address=cs.load_address(),
            jetton_master_address=cs.load_address(),
        )
