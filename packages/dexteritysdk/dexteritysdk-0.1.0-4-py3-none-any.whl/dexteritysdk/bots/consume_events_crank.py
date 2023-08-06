import os
from dexteritysdk.local_env import *
import time
import sys
import asyncio
import base64
import json
import base64
import argparse
import websockets as ws

from solana.keypair import Keypair
from solana.publickey import PublicKey

# dex
from dexteritysdk.dex.state import *
from dexteritysdk.dex.state import account_parser as dex_parser
import dexteritysdk.dex.actions as dex_act

# derivatives
from dexteritysdk.instruments.state import *
from dexteritysdk.instruments.state import account_parser as instr_parser
from dexteritysdk.dummy_oracle.state import *
from dexteritysdk.utils.aob.state import *
from dexteritysdk.utils.aob.state import account_parser as aob_parser
from dexteritysdk.utils.solana import (
    explore,
    AccountParser,
    Context
)
import dexteritysdk.program_ids as pids

# RPC
from solana.rpc.commitment import *
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client

curr_directory = os.path.dirname(os.path.abspath(__file__))
cfg_path = os.path.join(curr_directory, "config.json")
if os.path.exists(cfg_path):
    with open(cfg_path) as f:
        cfg = json.load(f)
        mpg_pubkey = cfg["mpg_key"]
else:
    ap = argparse.ArgumentParser()
    ap.add_argument("mpg_pubkey")
    args = ap.parse_args()
    mpg_pubkey = args.mpg_pubkey

payer = Keypair(b"nima" * 8)
market_product_group_pubkey = PublicKey(mpg_pubkey)
reward_target = payer.public_key
set_signers(payer)


def get_account_info(event):
    try:
        return [event.event_data.callback_info.user_account]
    except:
        return [
            event.event_data.maker_callback_info.user_account,
            event.event_data.taker_callback_info.user_account,
        ]


seq = 0


def get_rpc_payload(key):
    global seq
    payload = {
        "jsonrpc": "2.0",
        "id": seq,
        "method": "accountSubscribe",
        "params": [
            key,
            {"encoding": "base64", "commitment": "confirmed"},
        ],
    }
    seq += 1
    return payload


URL = "https://api.devnet.solana.com"
WS_URI = "wss://api.devnet.solana.com/"


type_dict = {}
event_queue_dict = {}
id_to_dict = {}

subscribed_products = []

parser = AccountParser()
parser.register_parser(pids.DEX_PROGRAM_ID, dex_parser)
parser.register_parser(pids.INSTRUMENTS_PROGRAM_ID, instr_parser)
parser.register_parser(pids.AOB_PROGRAM_ID, aob_parser)
set_global_parser(parser)
set_global_client(Client(URL))

market_product_group = explore(
    market_product_group_pubkey
).data_obj  # type: MarketProductGroup

print(mpg_pubkey)
print(market_product_group)

id_to_dict[seq] = {
    "type": "mpg",
}
mpg_payload = get_rpc_payload(str(market_product_group_pubkey))


async def register_events(market_product_group: MarketProductGroup, w):
    for product in (
        market_product_group.market_products + market_product_group.combo_products
    ):
        if product:
            print(product)
            product_pubkey = product.product_key
            if not product_pubkey in subscribed_products:
                orderbook_pubkey = product.orderbook
                id_to_dict[seq] = {
                    "type": "orderbook",
                    "product_pubkey": product_pubkey,
                    "orderbook_pubkey": orderbook_pubkey,
                }
                orderbook_payload = get_rpc_payload(str(orderbook_pubkey))
                orderbook = explore(orderbook_pubkey).data_obj  # type: MarketState
                event_pubkey = orderbook.event_queue
                await w.send(json.dumps(orderbook_payload))
                id_to_dict[seq] = {
                    "type": "event",
                    "event_pubkey": event_pubkey,
                    "product_pubkey": product_pubkey,
                    "orderbook_pubkey": orderbook_pubkey,
                    "orderbook_fee_budget": orderbook.fee_budget,
                }
                event_payload = get_rpc_payload(str(event_pubkey))
                await w.send(json.dumps(event_payload))
                subscribed_products.append(product_pubkey)

    print("all products loaded")


async def consume_events(payload, type_dict, client, n=20):
    event_data = base64.b64decode(payload["params"]["result"]["value"]["data"][0])
    events = EventQueue.from_bytes(event_data)
    product_pubkey = type_dict[payload["params"]["subscription"]]["product_pubkey"]
    orderbook_fee_budget = type_dict[payload["params"]["subscription"]][
        "orderbook_fee_budget"
    ]
    user_accounts = []
    for i in range(min(events.header.count, n)):
        user_accounts.extend(get_account_info(events[i]))

    unique_user_accounts = [
        PublicKey(item) for item in list(set([str(a) for a in user_accounts]))
    ]

    if events.header.count == 0:
        print("zero events")
        return

    capped_entries_consumed = min(n, events.header.count)
    reward = capped_entries_consumed * orderbook_fee_budget / events.header.count
    profit = reward - 5000
    print(f"profit after consuming this event: {profit}")
    if profit <= 0:
        print("It is not profitable to crank.")
        return

    pre_balance = client.get_balance(payer.public_key)["result"]["value"]
    print("sending consume event ...")
    _, resp = dex_act.consume_orderbook_events(
        market_product_group=market_product_group_pubkey,
        product_key=product_pubkey,
        reward_target=reward_target,
        user_accounts=sorted(unique_user_accounts, key=lambda x: bytes(x)),
        max_iterations=n,
    )
    print("sent consume event!")
    print(resp.tx_string)

    post_balance = client.get_balance(payer.public_key)["result"]["value"]
    print(f"Pre: {pre_balance}, Psot: {post_balance}")

    if post_balance < pre_balance:
        print("Lost money in cranking!")
        return


async def run(n=10):
    global market_product_group
    client = get_global_client()
    while True:
        async with ws.connect(WS_URI) as w:
            time.sleep(1)
            await w.send(json.dumps(mpg_payload))
            await register_events(market_product_group, w)
            while True:
                try:
                    acct = await (w.recv())
                except:
                    continue
                try:
                    payload = json.loads(acct)
                    if "params" in payload.keys():
                        if (
                            type_dict[payload["params"]["subscription"]]["type"]
                            == "mpg"
                        ):
                            print("market product group update")
                            market_product_group = parser.parse(
                                payload["params"]
                            )  # type: MarketProductGroup
                            await register_events(market_product_group, w)

                        elif (
                            type_dict[payload["params"]["subscription"]]["type"]
                            == "orderbook"
                        ):
                            print("orderbook update")
                            order_book: MarketState = parser.parse(payload["params"])
                            orderbook_pubkey = type_dict[
                                payload["params"]["subscription"]
                            ]["orderbook_pubkey"]
                            for item in type_dict:
                                try:
                                    if (
                                        type_dict[item]["orderbook_pubkey"]
                                        == orderbook_pubkey
                                    ):
                                        type_dict[item][
                                            "orderbook_fee_budget"
                                        ] = order_book.fee_budget
                                except:
                                    pass

                        elif (
                            type_dict[payload["params"]["subscription"]]["type"]
                            == "event"
                        ):
                            print("event update")
                            await consume_events(payload, type_dict, client, n)

                        else:
                            raise Exception("Can not find relevant payload!")

                    elif "result" in payload.keys():
                        try:
                            type_dict[payload["result"]] = id_to_dict[payload["id"]]
                        except:
                            raise Exception("Can not find relevant payload!")
                    else:
                        Exception("Can not find relevant payload!")
                except Exception as e:
                    print(e)
                    break


asyncio.run(run())
