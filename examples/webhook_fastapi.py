from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, Response

from pytonapi.types import Network, Opcode
from pytonapi.webhook import (
    AccountTxEvent,
    MempoolMsgEvent,
    NewContractsEvent,
    OpcodeMsgEvent,
    TonapiWebhookClient,
    TonapiWebhookDispatcher,
)

# TONAPI key — get one at https://tonconsole.com/
API_KEY = "YOUR_API_KEY"

# Target network — MAINNET or TESTNET
NETWORK = Network.MAINNET

# Public webhook URL prefix — TONAPI will POST events here
# Each event type gets its own suffix: /account-tx, /mempool-msg, etc.
WEBHOOK_URL = "https://example.com/webhook"

# Host and port for the local web server
HOST = "0.0.0.0"
PORT = 8000

# Account address to track — raw format
ACCOUNT_ID = "0:408da3b28b6c065a593e10391269baaa9c5f8caebc0c69d9f0aabbab2a99256b"

# Step 1: Create webhook client and dispatcher
client = TonapiWebhookClient(API_KEY, NETWORK)

# Dispatcher manages the full lifecycle: session, webhooks, subscriptions.
# setup() creates a separate TONAPI webhook for each event type that has handlers,
# subscribes them, and stores per-path secret tokens automatically.
dispatcher = TonapiWebhookDispatcher(
    WEBHOOK_URL,
    client=client,
    accounts=[ACCOUNT_ID],
    opcodes=[Opcode.TEXT_COMMENT],
)


# Step 2: Register event handlers
# Handles all account_tx events for every subscribed account
@dispatcher.account_tx()
async def on_account_tx(event: AccountTxEvent) -> None:
    print(f"Account TX: {event.account_id} | {event.tx_hash}")


# Local filter — only fires for ACCOUNT_ID
# Decorator filters are local dispatch only, they don't affect TONAPI subscriptions
@dispatcher.account_tx(ACCOUNT_ID)
async def on_my_account_tx(event: AccountTxEvent) -> None:
    print(f"My account TX: {event.tx_hash}")


# Mempool messages — raw BOC of pending transactions
@dispatcher.mempool_msg()
async def on_mempool_msg(event: MempoolMsgEvent) -> None:
    print(f"Mempool: {event.boc}")


# Opcode messages — fires when a message with a matching opcode is detected
@dispatcher.opcode_msg()
async def on_opcode_msg(event: OpcodeMsgEvent) -> None:
    print(f"Opcode: {event.account_id} | {event.tx_hash}")


# New contract deployments — fires when a new contract is deployed on-chain
@dispatcher.new_contracts()
async def on_new_contract(event: NewContractsEvent) -> None:
    print(f"New contract: {event.account_id} | {event.tx_hash}")


# Step 3: HTTP handler for incoming webhook POST requests
async def handle_webhook(request: Request) -> Response:
    data = await request.json()
    try:
        # Verify the Authorization header and dispatch the event to handlers
        authorization = request.headers.get("Authorization")
        await dispatcher.process(request.url.path, data, authorization=authorization)
    except Exception as e:
        print(f"Webhook error: {e}")
        return Response(status_code=401)
    return Response(status_code=200)


# Step 4: FastAPI lifespan — manages dispatcher setup/teardown
@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        # Opens session, creates webhooks, subscribes, stores tokens
        await dispatcher.setup()
        print("Webhooks synced")

        # Register a POST route for each event type path
        for path in dispatcher.paths.values():
            application.add_api_route(path, handle_webhook, methods=["POST"])
        print(f"Routes: {list(dispatcher.paths.values())}")

        yield
    finally:
        # Closes session only — subscriptions persist across restarts
        # Use teardown(cleanup=True) to also unsubscribe
        await dispatcher.teardown()


# Step 5: Create and run the app
app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
