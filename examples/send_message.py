from pytonapi.rest import TonapiRestClient
from pytonapi.types import Network

# TONAPI key — get one at https://tonconsole.com/
API_KEY = "YOUR_API_KEY"

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Serialized signed message in base64 (BOC — Bag of Cells)
# Any library that can build and sign TON messages will produce a BOC
# Recommended: tonutils (pip install tonutils) — wallets, jetton transfers, NFT ops, etc.
BOC = "te6cckEBAQEAAgAAAEysuc0="


async def main() -> None:
    async with TonapiRestClient(API_KEY, NETWORK) as tonapi:
        # Send the signed message to the blockchain
        # The BOC must be fully signed — TONAPI broadcasts it as-is
        # Raises TONAPIClientError if the message is rejected
        await tonapi.blockchain.send_message(body={"boc": BOC})
        print("Message accepted by the network")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
