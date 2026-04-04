from pytonapi.rest import TonapiRestClient
from pytonapi.types import Network
from pytonapi.utils import raw_to_userfriendly, to_amount

# TONAPI key — get one at https://tonconsole.com/
API_KEY = ""

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address to inspect — any format works (raw, bounceable, non-bounceable)
ACCOUNT_ID = "EQAUxYSo-UwoqAGixaD3d7CNLp9PthgmEZfnr6BvsijzJHdA"


async def main() -> None:
    async with TonapiRestClient(API_KEY, NETWORK) as tonapi:
        # Fetch account information
        # Returns: balance, status, interfaces, name, and more
        account = await tonapi.accounts.get_account(account_id=ACCOUNT_ID)

        # address is returned in raw format (workchain:hex_hash)
        # raw_to_userfriendly() converts to human-readable base64 form
        print(f"Address: {raw_to_userfriendly(account.address)}")

        # balance is in nanotons (1 TON = 10^9 nanotons)
        # to_amount() converts to human-readable TON
        print(f"Balance: {to_amount(account.balance)} TON")

        # Account status — active, uninit, frozen, or nonexist
        print(f"Status: {account.status}")

        # name — human-readable label (e.g., TON Foundation, Getgems, etc.)
        # None if the account is not recognized
        print(f"Name: {account.name}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
