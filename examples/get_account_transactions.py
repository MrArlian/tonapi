from pytonapi.rest import TonapiRestClient
from pytonapi.types import Network
from pytonapi.utils import to_amount

# TONAPI key — get one at https://tonconsole.com/
API_KEY = "YOUR_API_KEY"

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Account address to fetch transactions for
ACCOUNT_ID = "0:408da3b28b6c065a593e10391269baaa9c5f8caebc0c69d9f0aabbab2a99256b"


async def main() -> None:
    async with TonapiRestClient(API_KEY, NETWORK) as tonapi:
        # Fetch recent transactions for the account
        # limit: maximum number of transactions to return
        # Returns: list of blockchain transactions with full message data
        result = await tonapi.blockchain.get_account_transactions(
            account_id=ACCOUNT_ID,
            limit=100,
        )

        for transaction in result.transactions:
            # in_msg.value — incoming message value in nanotons
            # to_amount() converts nanotons to human-readable TON
            print(f"Value: {to_amount(transaction.in_msg.value, precision=5)} TON")

            # decoded_op_name indicates the message type (e.g., "text_comment")
            # decoded_body contains the parsed payload as a dict
            if transaction.in_msg.decoded_op_name == "text_comment":
                print(f"Comment: {transaction.in_msg.decoded_body['text']}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
