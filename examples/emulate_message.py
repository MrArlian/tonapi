from pytonapi.rest import TonapiRestClient
from pytonapi.types import Network

# TONAPI key — get one at https://tonconsole.com/
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Serialized signed message in base64 (BOC — Bag of Cells)
# Any library that can build and sign TON messages will produce a BOC
# Recommended: tonutils (pip install tonutils) — wallets, jetton transfers, NFT ops, etc.
BOC = "te6cckEBAQEAAgAAAEysuc0="


async def main() -> None:
    async with TonapiRestClient(API_KEY, NETWORK) as tonapi:
        # Emulate the message to preview resulting events
        # Returns: Event with actions, value flow, and involved accounts
        # Use this to verify the transaction before broadcasting
        event = await tonapi.emulation.emulate_message_to_event(
            body={"boc": BOC},
        )

        # actions describe what the transaction will do (transfer, deploy, swap, etc.)
        # each action has a type, status, and human-readable simple_preview
        for action in event.actions:
            print(f"Action: {action.type} — {action.simple_preview.description}")

        # is_scam flag warns if TONAPI detects suspicious patterns
        print(f"Scam: {event.is_scam}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
