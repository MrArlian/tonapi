# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.models import AccountEvents, NftCollection, NftCollections, NftItem, NftItems, NftOperations
from pytonapi.rest.resources._base import BaseResource


class NFTResource(BaseResource):
    """NFTResource resource group."""

    async def get_account_nft_history(
        self,
        account_id: str,
        limit: int,
        before_lt: int | None = None,
        accept_language: str | None = None,
    ) -> NftOperations:
        """Get the transfer nft history.

        :param account_id: Account ID.
        :param before_lt: Omit this parameter to get last events.
        :param limit: Limit.
        :param accept_language: Accept language.
        :return: NftOperations
        """
        path = f"/v2/accounts/{account_id}/nfts/history"
        params = {
            "before_lt": before_lt,
            "limit": limit,
        }
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            response_model=NftOperations,
        )

    async def get_collections(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> NftCollections:
        """Get NFT collections.

        :param limit: Limit.
        :param offset: Offset.
        :return: NftCollections
        """
        path = "/v2/nfts/collections"
        params = {
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=NftCollections,
        )

    async def get_collection(
        self,
        account_id: str,
    ) -> NftCollection:
        """Get NFT collection by collection address.

        :param account_id: Account ID.
        :return: NftCollection
        """
        path = f"/v2/nfts/collections/{account_id}"
        return await self._request(
            method="GET",
            path=path,
            response_model=NftCollection,
        )

    async def get_collection_items_by_addresses(
        self,
        body: dict[str, t.Any],
    ) -> NftCollections:
        """Get NFT collection items by their addresses.

        :param body: Request body.
        :return: NftCollections
        """
        path = "/v2/nfts/collections/_bulk"
        return await self._request(
            method="POST",
            path=path,
            body=body,
            response_model=NftCollections,
        )

    async def get_items_from_collection(
        self,
        account_id: str,
        limit: int = 1000,
        offset: int = 0,
    ) -> NftItems:
        """Get NFT items from collection by collection address.

        :param account_id: Account ID.
        :param limit: Limit.
        :param offset: Offset.
        :return: NftItems
        """
        path = f"/v2/nfts/collections/{account_id}/items"
        params = {
            "limit": limit,
            "offset": offset,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
            response_model=NftItems,
        )

    async def get_items_by_addresses(
        self,
        body: dict[str, t.Any],
    ) -> NftItems:
        """Get NFT items by their addresses.

        :param body: Request body.
        :return: NftItems
        """
        path = "/v2/nfts/_bulk"
        return await self._request(
            method="POST",
            path=path,
            body=body,
            response_model=NftItems,
        )

    async def get_item_by_address(
        self,
        account_id: str,
    ) -> NftItem:
        """Get NFT item by its address.

        :param account_id: Account ID.
        :return: NftItem
        """
        path = f"/v2/nfts/{account_id}"
        return await self._request(
            method="GET",
            path=path,
            response_model=NftItem,
        )

    async def get_history_by_id(
        self,
        account_id: str,
        limit: int,
        before_lt: int | None = None,
        start_date: int | None = None,
        end_date: int | None = None,
        accept_language: str | None = None,
    ) -> AccountEvents:
        """Please use `getAccountNftHistory`` instead.

        :param account_id: Account ID.
        :param before_lt: Omit this parameter to get last events.
        :param limit: Limit.
        :param start_date: Start date.
        :param end_date: End date.
        :param accept_language: Accept language.
        :return: AccountEvents
        """
        path = f"/v2/nfts/{account_id}/history"
        params = {
            "before_lt": before_lt,
            "limit": limit,
            "start_date": start_date,
            "end_date": end_date,
        }
        headers = {"Accept-Language": accept_language}
        return await self._request(
            method="GET",
            path=path,
            params=params,
            headers=headers,
            response_model=AccountEvents,
        )
