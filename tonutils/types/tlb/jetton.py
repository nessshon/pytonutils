from __future__ import annotations

import typing as t

from pytoniq_core import (
    Cell,
    Slice,
    begin_cell,
    TlbScheme,
)

from ...exceptions import UnexpectedOpCodeError
from ...types.common import AddressLike
from ...types.opcodes import OpCode
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
        jetton_wallet_code: Cell,
        content: OffchainContent,
        next_admin_address: t.Optional[AddressLike] = None,
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


class JettonTopUpBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_TOP_UP

    def __init__(self, query_id: int = 0) -> None:
        self.query_id = query_id

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonTopUpBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(query_id=cs.load_uint(64))
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonInternalTransferBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_INTERNAL_TRANSFER

    def __init__(
        self,
        jetton_amount: int,
        forward_amount: int,
        from_address: t.Optional[AddressLike] = None,
        response_address: t.Optional[AddressLike] = None,
        forward_payload: t.Optional[Cell] = None,
        query_id: int = 0,
    ) -> None:
        self.query_id = query_id
        self.jetton_amount = jetton_amount
        self.from_address = from_address
        self.response_address = response_address
        self.forward_amount = forward_amount
        self.forward_payload = forward_payload

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_coins(self.jetton_amount)
        cell.store_address(self.from_address)
        cell.store_address(self.response_address)
        cell.store_coins(self.forward_amount)
        cell.store_maybe_ref(self.forward_payload)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonInternalTransferBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(
                query_id=cs.load_uint(64),
                jetton_amount=cs.load_coins(),
                from_address=cs.load_address(),
                response_address=cs.load_address(),
                forward_amount=cs.load_coins(),
                forward_payload=cs.load_maybe_ref(),
            )
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonTransferBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_TRANSFER

    def __init__(
        self,
        jetton_amount: int,
        destination_address: AddressLike,
        response_address: t.Optional[AddressLike] = None,
        custom_payload: t.Optional[Cell] = None,
        forward_payload: t.Optional[Cell] = None,
        forward_amount: int = 1,
        query_id: int = 0,
    ) -> None:
        self.query_id = query_id
        self.jetton_amount = jetton_amount
        self.destination_address = destination_address
        self.response_address = response_address
        self.custom_payload = custom_payload
        self.forward_amount = forward_amount
        self.forward_payload = forward_payload

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_coins(self.jetton_amount)
        cell.store_address(self.destination_address)
        cell.store_address(self.response_address)
        cell.store_maybe_ref(self.custom_payload)
        cell.store_coins(self.forward_amount)
        cell.store_maybe_ref(self.forward_payload)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonTransferBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(
                query_id=cs.load_uint(64),
                jetton_amount=cs.load_coins(),
                destination_address=cs.load_address(),
                response_address=cs.load_address(),
                custom_payload=cs.load_maybe_ref(),
                forward_amount=cs.load_coins(),
                forward_payload=cs.load_maybe_ref(),
            )
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonMintBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_MINT

    def __init__(
        self,
        destination_address: AddressLike,
        internal_transfer: JettonInternalTransferBody,
        forward_amount: int,
        query_id: int = 0,
    ) -> None:
        self.query_id = query_id
        self.destination_address = destination_address
        self.forward_amount = forward_amount
        self.internal_transfer = internal_transfer

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_address(self.destination_address)
        cell.store_coins(self.forward_amount)
        cell.store_ref(self.internal_transfer.serialize())
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonMintBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(
                query_id=cs.load_uint(64),
                destination_address=cs.load_address(),
                forward_amount=cs.load_coins(),
                internal_transfer=JettonInternalTransferBody.deserialize(
                    cs.load_ref().begin_parse()
                ),
            )
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonStandardMintBody(JettonMintBody):
    OP_CODE: t.Union[OpCode, int] = 21


class JettonChangeAdminBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_CHANGE_ADMIN

    def __init__(
        self,
        admin_address: AddressLike,
        query_id: int = 0,
    ) -> None:
        self.query_id = query_id
        self.admin_address = admin_address

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_address(self.admin_address)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonChangeAdminBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(
                query_id=cs.load_uint(64),
                admin_address=cs.load_address(),
            )
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonStandardChangeAdminBody(JettonChangeAdminBody):
    OP_CODE: t.Union[OpCode, int] = 3


class JettonDiscoveryBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_PROVIDE_WALLET_ADDRESS

    def __init__(
        self,
        owner_address: AddressLike,
        include_address: bool = True,
        query_id: int = 0,
    ) -> None:
        self.query_id = query_id
        self.owner_address = owner_address
        self.include_address = include_address

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_address(self.owner_address)
        cell.store_bool(self.include_address)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonDiscoveryBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(
                query_id=cs.load_uint(64),
                owner_address=cs.load_address(),
                include_address=cs.load_bool(),
            )
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonClaimAdminBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_CLAIM_ADMIN

    def __init__(self, query_id: int = 0) -> None:
        self.query_id = query_id

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonClaimAdminBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(query_id=cs.load_uint(64))
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonDropAdminBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_DROP_ADMIN

    def __init__(self, query_id: int = 0) -> None:
        self.query_id = query_id

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonDropAdminBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(query_id=cs.load_uint(64))
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonChangeContentBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_CHANGE_METADATA_URI

    def __init__(
        self,
        content: OffchainContent,
        query_id: int = 0,
    ) -> None:
        self.query_id = query_id
        self.content = content

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_snake_string(self.content.uri)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonChangeContentBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(
                query_id=cs.load_uint(64),
                content=OffchainContent.deserialize(cs, False),
            )
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonStandardChangeContentBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = 4

    def __init__(
        self,
        content: ContentLike,
        query_id: int = 0,
    ) -> None:
        self.query_id = query_id
        self.content = content

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_ref(self.content.serialize(True))
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonStandardChangeContentBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            query_id = cs.load_uint(64)
            content_cs = cs.load_ref().begin_parse()
            prefix = MetadataPrefix(content_cs.load_uint(8))
            if prefix == MetadataPrefix.ONCHAIN:
                content = OnchainContent.deserialize(content_cs, False)
            else:
                content = OffchainContent.deserialize(content_cs, False)
            return cls(query_id=query_id, content=content)
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonBurnBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_BURN

    def __init__(
        self,
        jetton_amount: int,
        response_address: AddressLike,
        custom_payload: t.Optional[Cell] = None,
        query_id: int = 0,
    ) -> None:
        self.query_id = query_id
        self.jetton_amount = jetton_amount
        self.response_address = response_address
        self.custom_payload = custom_payload

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_coins(self.jetton_amount)
        cell.store_address(self.response_address)
        cell.store_maybe_ref(self.custom_payload)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonBurnBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(
                query_id=cs.load_uint(64),
                jetton_amount=cs.load_coins(),
                response_address=cs.load_address(),
                custom_payload=cs.load_maybe_ref(),
            )
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)


class JettonUpgradeBody(TlbScheme):
    OP_CODE: t.Union[OpCode, int] = OpCode.JETTON_UPGRADE

    def __init__(
        self,
        code: Cell,
        data: Cell,
        query_id: int = 0,
    ) -> None:
        self.query_id = query_id
        self.data = data
        self.code = code

    def serialize(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.OP_CODE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_ref(self.data)
        cell.store_ref(self.code)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonUpgradeBody:
        op_code = cs.load_uint(32)
        if op_code == cls.OP_CODE:
            return cls(
                query_id=cs.load_uint(64),
                data=cs.load_ref(),
                code=cs.load_ref(),
            )
        raise UnexpectedOpCodeError(cls, cls.OP_CODE, op_code)
