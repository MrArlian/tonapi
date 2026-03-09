# This example requires the `tonutils` package:
# pip install tonutils

from pytoniq_core import Address

from tonutils.clients import TonapiClient
from tonutils.contracts import WalletV5R1
from tonutils.types import NetworkGlobalID
from tonutils.utils import to_nano

# Tonapi API key (required)
# Get one at https://tonconsole.com/
API_KEY = "YOUR_API_KEY"

# 24-word mnemonic phrase (BIP-39 or TON-specific)
# Used to derive the wallet's private key
MNEMONIC = "word1 word2 word3 ..."

# Destination address (recipient)
DESTINATION_ADDRESS = Address("UQ...")


async def main() -> None:
    # Initialize HTTP client for TON blockchain interaction
    # NetworkGlobalID.MAINNET (-239) for production
    # NetworkGlobalID.TESTNET (-3) for testing
    client = TonapiClient(network=NetworkGlobalID.MAINNET, api_key=API_KEY)
    await client.connect()

    # Create wallet instance from mnemonic (full access mode)
    # Returns: (wallet, public_key, private_key, mnemonic)
    wallet, _, _, _ = WalletV5R1.from_mnemonic(client, MNEMONIC)

    # Send TON with optional text comment
    # destination: recipient address
    # amount: in nanotons (use to_nano() to convert from TON)
    #   1 TON = 1,000,000,000 nanotons (10^9)
    # body: optional text comment (visible in explorers and recipient wallet)
    msg = await wallet.transfer(
        destination=DESTINATION_ADDRESS,
        amount=to_nano(0.01),  # Convert 0.01 TON to nanotons (10,000,000)
        body="Hello from tonutils!",
    )

    # Transaction hash for tracking on blockchain explorers
    # Use tonviewer.com or tonscan.org to view transaction
    print(f"Transaction hash: {msg.normalized_hash}")

    await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
