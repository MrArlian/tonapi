# This file is auto-generated. Do not edit manually.

from __future__ import annotations

import typing as t

from pytonapi.rest.resources._base import BaseResource


class LiteServerResource(BaseResource):
    """LiteServerResource resource group."""

    async def get_raw_masterchain_info(
        self,
    ) -> t.Any:
        """Get raw masterchain info.

        :return: dict[str, t.Any]
        """
        path = "/v2/liteserver/get_masterchain_info"
        return await self._request(
            method="GET",
            path=path,
        )

    async def get_raw_masterchain_info_ext(
        self,
        mode: int,
    ) -> t.Any:
        """Get raw masterchain info ext.

        :param mode: Mode.
        :return: dict[str, t.Any]
        """
        path = "/v2/liteserver/get_masterchain_info_ext"
        params = {"mode": mode}
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_raw_time(
        self,
    ) -> t.Any:
        """Get raw time.

        :return: dict[str, t.Any]
        """
        path = "/v2/liteserver/get_time"
        return await self._request(
            method="GET",
            path=path,
        )

    async def get_raw_blockchain_block(
        self,
        block_id: str,
    ) -> t.Any:
        """Get raw blockchain block.

        :param block_id: Block ID: (workchain,shard,seqno,root_hash,file_hash).
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/get_block/{block_id}"
        return await self._request(
            method="GET",
            path=path,
        )

    async def get_raw_blockchain_block_state(
        self,
        block_id: str,
    ) -> t.Any:
        """Get raw blockchain block state.

        :param block_id: Block ID: (workchain,shard,seqno,root_hash,file_hash).
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/get_state/{block_id}"
        return await self._request(
            method="GET",
            path=path,
        )

    async def get_raw_blockchain_block_header(
        self,
        block_id: str,
        mode: int,
    ) -> t.Any:
        """Get raw blockchain block header.

        :param block_id: Block ID: (workchain,shard,seqno,root_hash,file_hash).
        :param mode: Mode.
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/get_block_header/{block_id}"
        params = {"mode": mode}
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def send_raw_message(
        self,
        body: dict[str, t.Any],
    ) -> t.Any:
        """Send raw message to blockchain.

        :param body: Request body.
        :return: dict[str, t.Any]
        """
        path = "/v2/liteserver/send_message"
        return await self._request(
            method="POST",
            path=path,
            body=body,
        )

    async def get_raw_account_state(
        self,
        account_id: str,
        target_block: str | None = None,
    ) -> t.Any:
        """Get raw account state.

        :param account_id: Account ID.
        :param target_block: Target block: (workchain,shard,seqno,root_hash,file_hash).
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/get_account_state/{account_id}"
        params = {"target_block": target_block}
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_raw_shard_info(
        self,
        block_id: str,
        workchain: int,
        shard: int,
        exact: bool,
    ) -> t.Any:
        """Get raw shard info.

        :param block_id: Block ID: (workchain,shard,seqno,root_hash,file_hash).
        :param workchain: Workchain.
        :param shard: Shard.
        :param exact: Exact.
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/get_shard_info/{block_id}"
        params = {
            "workchain": workchain,
            "shard": shard,
            "exact": exact,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_all_raw_shards_info(
        self,
        block_id: str,
    ) -> t.Any:
        """Get all raw shards info.

        :param block_id: Block ID: (workchain,shard,seqno,root_hash,file_hash).
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/get_all_shards_info/{block_id}"
        return await self._request(
            method="GET",
            path=path,
        )

    async def get_raw_transactions(
        self,
        account_id: str,
        count: int,
        lt: int,
        hash: str,
    ) -> t.Any:
        """Get raw transactions.

        :param account_id: Account ID.
        :param count: Count.
        :param lt: Lt.
        :param hash: Hash.
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/get_transactions/{account_id}"
        params = {
            "count": count,
            "lt": lt,
            "hash": hash,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_raw_list_block_transactions(
        self,
        block_id: str,
        mode: int,
        count: int,
        account_id: str | None = None,
        lt: int | None = None,
    ) -> t.Any:
        """Get raw list block transactions.

        :param block_id: Block ID: (workchain,shard,seqno,root_hash,file_hash).
        :param mode: Mode.
        :param count: Count.
        :param account_id: Account ID.
        :param lt: Lt.
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/list_block_transactions/{block_id}"
        params = {
            "mode": mode,
            "count": count,
            "account_id": account_id,
            "lt": lt,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_raw_block_proof(
        self,
        known_block: str,
        mode: int,
        target_block: str | None = None,
    ) -> t.Any:
        """Get raw block proof.

        :param known_block: Known block: (workchain,shard,seqno,root_hash,file_hash).
        :param target_block: Target block: (workchain,shard,seqno,root_hash,file_hash).
        :param mode: Mode.
        :return: dict[str, t.Any]
        """
        path = "/v2/liteserver/get_block_proof"
        params = {
            "known_block": known_block,
            "target_block": target_block,
            "mode": mode,
        }
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_raw_config(
        self,
        block_id: str,
        mode: int,
    ) -> t.Any:
        """Get raw config.

        :param block_id: Block ID: (workchain,shard,seqno,root_hash,file_hash).
        :param mode: Mode.
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/get_config_all/{block_id}"
        params = {"mode": mode}
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def get_raw_shard_block_proof(
        self,
        block_id: str,
    ) -> t.Any:
        """Get raw shard block proof.

        :param block_id: Block ID: (workchain,shard,seqno,root_hash,file_hash).
        :return: dict[str, t.Any]
        """
        path = f"/v2/liteserver/get_shard_block_proof/{block_id}"
        return await self._request(
            method="GET",
            path=path,
        )

    async def get_out_msg_queue_sizes(
        self,
    ) -> t.Any:
        """Get out msg queue sizes.

        :return: dict[str, t.Any]
        """
        path = "/v2/liteserver/get_out_msg_queue_sizes"
        return await self._request(
            method="GET",
            path=path,
        )
