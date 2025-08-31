import abc
import typing as t

from pytoniq_core import (
    Address,
    Cell,
    StateInit,
    WalletMessage,
)

from ..types.common import AddressLike, SendMode
from ..types.tlb.jetton import JettonTransferBody
from ..types.tlb.nft import NFTTransferBody
from ..types.tlb.text import TextComment
from ..utils.value_utils import to_nano

if t.TYPE_CHECKING:
    from ..protocols import WalletProtocol

    Wallet = WalletProtocol
else:
    Wallet = t.Any


class BaseTransferMessage(abc.ABC):

    @abc.abstractmethod
    async def to_wallet_msg(
        self,
        wallet: Wallet,
    ) -> WalletMessage: ...

    def __repr__(self) -> str:
        parts = " ".join(f"{k}: {v!r}" for k, v in vars(self).items())
        return f"< {self.__class__.__name__} {parts} >"


class TransferMessage(BaseTransferMessage):

    def __init__(
        self,
        destination: AddressLike,
        amount: int,
        body: t.Optional[t.Union[Cell, str]] = None,
        state_init: t.Optional[StateInit] = None,
        send_mode: t.Optional[t.Union[SendMode, int]] = None,
        bounce: t.Optional[bool] = None,
    ) -> None:
        if isinstance(body, str):
            body = TextComment(body).serialize()

        self.destination = destination
        self.amount = amount
        self.body = body
        self.state_init = state_init
        self.send_mode = send_mode
        self.bounce = bounce

    async def to_wallet_msg(
        self,
        wallet: Wallet,
    ) -> WalletMessage:
        from ..utils.msg_builders import build_internal_wallet_msg

        return build_internal_wallet_msg(
            dest=self.destination,
            value=self.amount,
            body=self.body,
            state_init=self.state_init,
            send_mode=self.send_mode,
            bounce=self.bounce,
        )


class TransferNFTMessage(BaseTransferMessage):

    def __init__(
        self,
        destination: AddressLike,
        nft_address: AddressLike,
        response_address: t.Optional[AddressLike] = None,
        custom_payload: t.Optional[t.Union[Cell]] = None,
        forward_amount: int = 1,
        forward_payload: t.Optional[t.Union[Cell, str]] = None,
        total_amount: int = to_nano(0.05),
        send_mode: t.Optional[t.Union[SendMode, int]] = None,
        bounce: t.Optional[bool] = None,
    ) -> None:
        if isinstance(forward_payload, str):
            forward_payload = TextComment(forward_payload).serialize()

        self.destination_address = destination
        self.nft_address = nft_address
        self.response_address = response_address
        self.custom_payload = custom_payload
        self.forward_amount = forward_amount
        self.forward_payload = forward_payload
        self.total_amount = total_amount
        self.send_mode = send_mode
        self.bounce = bounce

    async def to_wallet_msg(
        self,
        wallet: Wallet,
    ) -> WalletMessage:
        from ..utils.msg_builders import build_internal_wallet_msg

        body = NFTTransferBody(
            destination_address=self.destination_address,
            response_address=self.response_address or wallet.address,
            custom_payload=self.custom_payload,
            forward_amount=self.forward_amount,
            forward_payload=self.forward_payload,
        )
        return build_internal_wallet_msg(
            dest=self.nft_address,
            send_mode=self.send_mode,
            value=self.total_amount,
            body=body.serialize(),
            bounce=self.bounce,
        )


class TransferJettonMessage(BaseTransferMessage):

    def __init__(
        self,
        destination: AddressLike,
        jetton_amount: int,
        jetton_master_address: AddressLike,
        jetton_wallet_address: t.Optional[AddressLike] = None,
        response_address: t.Optional[AddressLike] = None,
        custom_payload: t.Optional[Cell] = None,
        forward_amount: int = 1,
        forward_payload: t.Optional[t.Union[Cell, str]] = None,
        total_amount: int = to_nano(0.05),
        send_mode: t.Optional[t.Union[SendMode, int]] = None,
        bounce: t.Optional[bool] = None,
    ) -> None:
        if isinstance(forward_payload, str):
            forward_payload = TextComment(forward_payload).serialize()

        self.destination_address = destination
        self.jetton_amount = jetton_amount
        self.jetton_master_address = jetton_master_address
        self.jetton_wallet_address = jetton_wallet_address
        self.response_address = response_address
        self.custom_payload = custom_payload
        self.forward_amount = forward_amount
        self.forward_payload = forward_payload
        self.total_amount = total_amount
        self.send_mode = send_mode
        self.bounce = bounce

    async def _get_jetton_wallet_address(self, wallet: Wallet) -> Address:
        from ..contracts import JettonMasterGetMethods

        return await JettonMasterGetMethods.get_wallet_address(
            client=wallet.client,
            address=self.jetton_master_address,
            owner_address=wallet.address,
        )

    async def to_wallet_msg(
        self,
        wallet: Wallet,
    ) -> WalletMessage:
        from ..utils.msg_builders import build_internal_wallet_msg

        if self.jetton_wallet_address is None:
            self.jetton_wallet_address = await self._get_jetton_wallet_address(wallet)

        body = JettonTransferBody(
            jetton_amount=self.jetton_amount,
            destination_address=self.destination_address,
            response_address=self.response_address or wallet.address,
            custom_payload=self.custom_payload,
            forward_amount=self.forward_amount,
            forward_payload=self.forward_payload,
        )
        return build_internal_wallet_msg(
            dest=self.jetton_wallet_address,
            send_mode=self.send_mode,
            value=self.total_amount,
            body=body.serialize(),
            bounce=self.bounce,
        )
