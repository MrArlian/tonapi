from pytonapi.rest import TonapiRestClient
from pytonapi.types import Network
from pytonapi.utils import raw_to_userfriendly, to_amount

# TONAPI key — get one at https://tonconsole.com/
API_KEY = "YOUR_API_KEY"

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Jetton master contract address — identifies the token type
# This is the USDT jetton on TON mainnet
JETTON_ID = "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs"


async def main() -> None:
    async with TonapiRestClient(API_KEY, NETWORK) as tonapi:
        # Fetch jetton metadata and stats by its master contract address
        # Returns: name, symbol, decimals, total supply, holders count, and more
        jetton = await tonapi.jettons.get_jetton_info(account_id=JETTON_ID)

        # metadata contains token identity: name, symbol, decimals, image, etc.
        print(f"Name: {jetton.metadata.name}")
        print(f"Symbol: {jetton.metadata.symbol}")

        # total_supply is in base units (smallest denomination)
        # decimals defines how to convert: e.g., 1 USDT = 10^6 base units
        supply = to_amount(int(jetton.total_supply), int(jetton.metadata.decimals))
        print(f"Total supply: {supply} {jetton.metadata.symbol}")

        # holders_count — number of unique wallets holding this jetton
        print(f"Holders: {jetton.holders_count}")

        # verification — whitelist/blacklist/none status on TONAPI
        print(f"Verification: {jetton.verification}")

        # mintable — whether new tokens can still be minted
        print(f"Mintable: {jetton.mintable}")

        # admin — contract admin address (can mint/burn), None if renounced
        if jetton.admin:
            print(f"Admin: {raw_to_userfriendly(jetton.admin.address)}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
