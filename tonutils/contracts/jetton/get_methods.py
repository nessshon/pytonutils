import typing as t

from pytoniq_core import Address

from ...protocols import ClientProtocol
from ...types import AddressLike


class JettonMasterGetMethods:

    @classmethod
    async def get_jetton_data(
        cls,
        client: ClientProtocol,
        address: AddressLike,
    ) -> t.List[t.Any]:
        method_result = await client.run_get_method(
            address=address,
            method_name="get_jetton_data",
        )
        return method_result

    @classmethod
    async def get_wallet_address(
        cls,
        client: ClientProtocol,
        address: AddressLike,
        owner_address: AddressLike,
    ) -> Address:
        method_result = await client.run_get_method(
            address=address,
            method_name="get_wallet_address",
            stack=[owner_address],
        )
        return method_result[0]

    @classmethod
    async def get_next_admin_address(
        cls,
        client: ClientProtocol,
        address: AddressLike,
    ) -> t.Optional[Address]:
        method_result = await client.run_get_method(
            address=address,
            method_name="get_next_admin_address",
        )
        return method_result[0]


class JettonWalletGetMethods:

    @classmethod
    async def get_wallet_data(
        cls,
        client: ClientProtocol,
        address: AddressLike,
    ) -> t.List[t.Any]:
        method_result = await client.run_get_method(
            address=address,
            method_name="get_wallet_data",
        )
        return method_result

    @classmethod
    async def get_status(
        cls,
        client: ClientProtocol,
        address: AddressLike,
    ) -> int:
        method_result = await client.run_get_method(
            address=address,
            method_name="get_status",
        )
        return method_result[0]
