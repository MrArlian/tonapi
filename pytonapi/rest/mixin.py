# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.resources.accounts import AccountsResource
from pytonapi.rest.resources.blockchain import BlockchainResource
from pytonapi.rest.resources.connect import ConnectResource
from pytonapi.rest.resources.dns import DNSResource
from pytonapi.rest.resources.emulation import EmulationResource
from pytonapi.rest.resources.events import EventsResource
from pytonapi.rest.resources.extra_currency import ExtraCurrencyResource
from pytonapi.rest.resources.gasless import GaslessResource
from pytonapi.rest.resources.jettons import JettonsResource
from pytonapi.rest.resources.lite_server import LiteServerResource
from pytonapi.rest.resources.multisig import MultisigResource
from pytonapi.rest.resources.nft import NFTResource
from pytonapi.rest.resources.purchases import PurchasesResource
from pytonapi.rest.resources.rates import RatesResource
from pytonapi.rest.resources.staking import StakingResource
from pytonapi.rest.resources.storage import StorageResource
from pytonapi.rest.resources.traces import TracesResource
from pytonapi.rest.resources.utilities import UtilitiesResource
from pytonapi.rest.resources.wallet import WalletResource

if t.TYPE_CHECKING:
    from pytonapi.rest.client import TonapiRestClient


class ResourcesMixin:
    """Mixin that exposes all API resources as properties."""

    def __init__(self, client: TonapiRestClient) -> None:
        self._client = client

    @property
    def accounts(self) -> AccountsResource:
        """Access :class:`AccountsResource` resource group."""
        return AccountsResource(self._client)

    @property
    def blockchain(self) -> BlockchainResource:
        """Access :class:`BlockchainResource` resource group."""
        return BlockchainResource(self._client)

    @property
    def connect(self) -> ConnectResource:
        """Access :class:`ConnectResource` resource group."""
        return ConnectResource(self._client)

    @property
    def dns(self) -> DNSResource:
        """Access :class:`DNSResource` resource group."""
        return DNSResource(self._client)

    @property
    def emulation(self) -> EmulationResource:
        """Access :class:`EmulationResource` resource group."""
        return EmulationResource(self._client)

    @property
    def events(self) -> EventsResource:
        """Access :class:`EventsResource` resource group."""
        return EventsResource(self._client)

    @property
    def extra_currency(self) -> ExtraCurrencyResource:
        """Access :class:`ExtraCurrencyResource` resource group."""
        return ExtraCurrencyResource(self._client)

    @property
    def gasless(self) -> GaslessResource:
        """Access :class:`GaslessResource` resource group."""
        return GaslessResource(self._client)

    @property
    def jettons(self) -> JettonsResource:
        """Access :class:`JettonsResource` resource group."""
        return JettonsResource(self._client)

    @property
    def lite_server(self) -> LiteServerResource:
        """Access :class:`LiteServerResource` resource group."""
        return LiteServerResource(self._client)

    @property
    def multisig(self) -> MultisigResource:
        """Access :class:`MultisigResource` resource group."""
        return MultisigResource(self._client)

    @property
    def nft(self) -> NFTResource:
        """Access :class:`NFTResource` resource group."""
        return NFTResource(self._client)

    @property
    def purchases(self) -> PurchasesResource:
        """Access :class:`PurchasesResource` resource group."""
        return PurchasesResource(self._client)

    @property
    def rates(self) -> RatesResource:
        """Access :class:`RatesResource` resource group."""
        return RatesResource(self._client)

    @property
    def staking(self) -> StakingResource:
        """Access :class:`StakingResource` resource group."""
        return StakingResource(self._client)

    @property
    def storage(self) -> StorageResource:
        """Access :class:`StorageResource` resource group."""
        return StorageResource(self._client)

    @property
    def traces(self) -> TracesResource:
        """Access :class:`TracesResource` resource group."""
        return TracesResource(self._client)

    @property
    def utilities(self) -> UtilitiesResource:
        """Access :class:`UtilitiesResource` resource group."""
        return UtilitiesResource(self._client)

    @property
    def wallet(self) -> WalletResource:
        """Access :class:`WalletResource` resource group."""
        return WalletResource(self._client)
