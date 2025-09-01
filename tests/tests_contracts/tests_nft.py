from unittest import TestCase

from pytoniq_core import Address

from tests.helpers import ClientTestCase
from tonutils.contracts import (
    NFTCollectionEditable,
    NFTCollectionStandard,
    NFTItemStandard,
    NFTItemEditable,
    NFTItemSoulbound,
)
from tonutils.types import (
    ClientType,
    NFTCollectionContent,
    NFTCollectionData,
    NFTItemEditableData,
    NFTItemStandardData,
    NFTItemSoulboundData,
    OffchainContent,
    OffchainItemContent,
)

NFT_COLLECTION_STANDARD_ADDRESS = Address(
    "EQAG2BH0JlmFkbMrLEnyn2bIITaOSssd4WdisE4BdFMkZbir"
)
NFT_COLLECTION_EDITABLE_ADDRESS = Address(
    "EQBibSZPEVHWHhUALDTW4y5NDNcC7HPS-BRgv9dAAsZQjh2E"
)
NFT_COLLECTION_SOULBOUND_ADDRESS = Address(
    "EQCsiaV6k0-EZvl5AyurAjNYqvT6FhGX83xYlKlU5isWt6ki"
)


NFT_ITEM_STANDARD_ADDRESS = Address("EQCoADmGFboLrgOCDSwAe-jI-lOOVoRYllA5F4WeIMokINW8")
NFT_ITEM_EDITABLE_ADDRESS = Address("EQCSAPwp9B8IioWbjYf5w9YTzNlLdk_ntvNvjVtFkp9TGyno")
NFT_ITEM_SOULBOUND_ADDRESS = Address("EQCC6S6n3qStNZYuhGUiu_iJXcdOh2xa7WsklqS7uXiaE8W3")


class TestsNFTContracts(TestCase):

    def test_calcualte_nft_item_address(self) -> None:
        calculated_address_standard = NFTCollectionStandard.calculate_nft_item_address(
            index=0,
            nft_item_code=NFTItemStandard.get_default_code(),
            collection_address=NFT_COLLECTION_STANDARD_ADDRESS,
        )
        self.assertEqual(calculated_address_standard, NFT_ITEM_STANDARD_ADDRESS)

        calculated_address_editable = NFTCollectionEditable.calculate_nft_item_address(
            index=0,
            nft_item_code="b5ee9c72010212010002e5000114ff00f4a413f4bcf2c80b0102016202030202ce0405020120101102012006070201200e0f04f70c8871c02497c0f83434c0c05c6c2497c0f83e903e900c7e800c5c75c87e800c7e800c3c00816ce38596db088d148cb1c17cb865407e90353e900c040d3c00f801f4c7f4cfe08417f30f45148c2ea3a28c8412040dc409841140b820840bf2c9a8948c2eb8c0a0840701104a948c2ea3a28c8412040dc409841140a008090a0b00113e910c1c2ebcb8536001f65136c705f2e191fa4021f001fa40d20031fa00820afaf0801ca121945315a0a1de22d70b01c300209206a19136e220c2fff2e192218e3e821005138d91c8500acf16500ccf1671244a145446b0708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb00105894102b385be20c0080135f03333334347082108b77173504c8cbff58cf164430128040708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0001f65134c705f2e191fa4021f001fa40d20031fa00820afaf0801ca121945315a0a1de22d70b01c300209206a19136e220c2fff2e192218e3e8210511a4463c85008cf16500ccf1671244814544690708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb00103894102b365be20d0046e03136373782101a0b9d5116ba9e5131c705f2e19a01d4304400f003e05f06840ff2f00082028e3527f0018210d53276db103845006d71708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0093303335e25503f0030082028e3527f0018210d53276db103848006d71708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0093303630e25503f00300413b513434cffe900835d27080271fc07e90353e900c040d440d380c1c165b5b5b600025013232cfd400f3c58073c5b30073c5b27b5520000dbf03a78013628c000bbc7e7f801184",
            collection_address=NFT_COLLECTION_EDITABLE_ADDRESS,
        )
        self.assertEqual(calculated_address_editable, NFT_ITEM_EDITABLE_ADDRESS)

        calculated_address_soulbound = NFTCollectionStandard.calculate_nft_item_address(
            index=2777,
            nft_item_code="b5ee9c720102130100033b000114ff00f4a413f4bcf2c80b0102016202030202ce04050201200f1004bd46c2220c700915be001d0d303fa4030f002f842b38e1c31f84301c705f2e195fa4001f864d401f866fa4030f86570f867f003e002d31f0271b0e30201d33f8210d0c3bfea5230bae302821004ded1485230bae3023082102fcb26a25220ba8060708090201200d0e00943031d31f82100524c7ae12ba8e39d33f308010f844708210c18e86d255036d804003c8cb1f12cb3f216eb39301cf179131e2c97105c8cb055004cf1658fa0213cb6accc901fb009130e200c26c12fa40d4d30030f847f841c8cbff5006cf16f844cf1612cc14cb3f5230cb0003c30096f8465003cc02de801078b17082100dd607e3403514804003c8cb1f12cb3f216eb39301cf179131e2c97105c8cb055004cf1658fa0213cb6accc901fb0000c632f8445003c705f2e191fa40d4d30030f847f841c8cbfff844cf1613cc12cb3f5210cb0001c30094f84601ccde801078b17082100524c7ae405503804003c8cb1f12cb3f216eb39301cf179131e2c97105c8cb055004cf1658fa0213cb6accc901fb0003fa8e4031f841c8cbfff843cf1680107082108b7717354015504403804003c8cb1f12cb3f216eb39301cf179131e2c97105c8cb055004cf1658fa0213cb6accc901fb00e082101f04537a5220bae30282106f89f5e35220ba8e165bf84501c705f2e191f847c000f2e193f823f867f003e08210d136d3b35220bae30230310a0b0c009231f84422c705f2e1918010708210d53276db102455026d830603c8cb1f12cb3f216eb39301cf179131e2c97105c8cb055004cf1658fa0213cb6accc901fb008b02f8648b02f865f003008e31f84422c705f2e191820afaf08070fb028010708210d53276db102455026d830603c8cb1f12cb3f216eb39301cf179131e2c97105c8cb055004cf1658fa0213cb6accc901fb00002082105fcc3d14ba93f2c19dde840ff2f000613b513434cfc07e187e90007e18dc3e188835d2708023859ffe18be90007e1935007e19be90007e1974cfcc3e19e44c38a000373e11fe11be107232cffe10f3c5be1133c5b33e1173c5b2cff27b55200201581112001dbc7e7f8017c217c20fc21fc227c234000db5631e005f08b0000db7b07e005f08f0",
            collection_address=NFT_COLLECTION_SOULBOUND_ADDRESS,
        )
        self.assertEqual(calculated_address_soulbound, NFT_ITEM_SOULBOUND_ADDRESS)


class TestsNFTContractsTonapi(ClientTestCase):
    CLIENT_TYPE = ClientType.TONAPI
    IS_TESTNET = False
    RPS = 1

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()

        self.nft_collection_standard = await NFTCollectionStandard.from_address(
            client=self.client,
            address=NFT_COLLECTION_STANDARD_ADDRESS,
        )
        self.assertIsInstance(
            self.nft_collection_standard.content,
            NFTCollectionContent,
        )
        self.assertIsInstance(
            self.nft_collection_standard.state_data,
            NFTCollectionData,
        )
        self.nft_collection_editable = await NFTCollectionEditable.from_address(
            client=self.client,
            address=NFT_COLLECTION_EDITABLE_ADDRESS,
        )
        self.assertIsInstance(
            self.nft_collection_editable.content,
            NFTCollectionContent,
        )
        self.assertIsInstance(
            self.nft_collection_editable.state_data,
            NFTCollectionData,
        )

        self.nft_item_standard: NFTItemStandard = await NFTItemStandard.from_address(
            client=self.client,
            address=NFT_ITEM_STANDARD_ADDRESS,
        )
        self.assertIsInstance(self.nft_item_standard.content, OffchainItemContent)
        self.assertIsInstance(self.nft_item_standard.state_data, NFTItemStandardData)

        self.nft_item_editable: NFTItemEditable = await NFTItemEditable.from_address(
            client=self.client,
            address=NFT_ITEM_EDITABLE_ADDRESS,
        )
        self.assertIsInstance(self.nft_item_editable.content, OffchainItemContent)
        self.assertIsInstance(self.nft_item_editable.state_data, NFTItemEditableData)

        self.nft_item_soulbound: NFTItemSoulbound = await NFTItemSoulbound.from_address(
            client=self.client,
            address=NFT_ITEM_SOULBOUND_ADDRESS,
        )
        self.assertIsInstance(self.nft_item_soulbound.content, OffchainItemContent)
        self.assertIsInstance(self.nft_item_soulbound.state_data, NFTItemSoulboundData)

    async def test_nft_collection_get_collection_data(self) -> None:
        next_item_index, content, owner_address = (
            await self.nft_collection_standard.get_collection_data()
        )
        self.assertIsInstance(next_item_index, int)
        self.assertIsInstance(content, OffchainContent)
        self.assertIsInstance(owner_address, Address)

    async def test_nft_collection_get_nft_address_by_index(self) -> None:
        item_address = await self.nft_collection_standard.get_nft_address_by_index(
            index=self.nft_item_standard.index,
        )
        self.assertEqual(self.nft_item_standard.address, item_address)

    async def test_nft_collection_get_nft_content(self) -> None:
        item_full_content = await self.nft_collection_standard.get_nft_content(
            index=self.nft_item_standard.index,
            individual_nft_content=self.nft_item_standard.content.serialize(),
        )
        item_suffix_uri = self.nft_collection_standard.content.common_content.suffix_uri
        item_prefix_uri = self.nft_item_standard.content.prefix_uri
        item_full_uri = item_suffix_uri + item_prefix_uri
        self.assertEqual(item_full_uri, item_full_content.uri)

    async def test_nft_item_get_nft_data(self) -> None:
        init, index, collection_address, owner_address, content = (
            await self.nft_item_standard.get_nft_data()
        )
        self.assertIsInstance(init, bool)
        self.assertIsInstance(index, int)
        self.assertIsInstance(collection_address, Address)
        self.assertIsInstance(owner_address, Address)
        self.assertIsInstance(content, OffchainItemContent)

    async def test_nft_item_get_editor(self) -> None:
        editor_address = await self.nft_item_editable.get_editor_address()
        self.assertIsInstance(editor_address, (Address, type(None)))

    async def test_nft_item_get_authority_address(self) -> None:
        authority_address = await self.nft_item_soulbound.get_authority_address()
        self.assertIsInstance(authority_address, (Address, type(None)))

    async def test_nft_item_get_revoked_time(self) -> None:
        revoked_time = await self.nft_item_soulbound.get_revoked_time()
        self.assertIsInstance(revoked_time, int)


class TestsNFTContractsToncenter(TestsNFTContractsTonapi):
    CLIENT_TYPE = ClientType.TONCENTER


class TestsNFTContractsLiteserver(TestsNFTContractsTonapi):
    CLIENT_TYPE = ClientType.LITESERVER
