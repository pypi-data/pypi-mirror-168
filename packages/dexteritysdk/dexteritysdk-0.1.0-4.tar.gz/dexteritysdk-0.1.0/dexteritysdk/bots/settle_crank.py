import os

from dexteritysdk.local_env import *

import asyncio
import json
import base64
import argparse
import websockets as ws
import time

# dex
from dexteritysdk.dex.state import *
from dexteritysdk.dex.state import account_parser as dex_parser
import dexteritysdk.dex.actions as dex_actions

# derivatives
from dexteritysdk.instruments.state import *
from dexteritysdk.instruments.state import account_parser as instr_parser
import dexteritysdk.instruments.actions as instr_actions
from dexteritysdk.dummy_oracle.state import *
from dexteritysdk.utils.aob.state import *
from dexteritysdk.utils.aob.state import account_parser as aob_parser
from dexteritysdk.utils.solana import (
    explore,
    AccountParser,
    set_global_parser,
    get_global_client,
    set_global_client,
    set_signers,
)
import dexteritysdk.program_ids as pids

# RPC
from solana.rpc.commitment import *
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.sysvar import SYSVAR_CLOCK_PUBKEY


def load_account_as(pubkey: PublicKey, cls):
    client = get_global_client()
    info = client.get_account_info(pubkey, commitment=Confirmed)
    if info["result"]["value"] is None:
        return None
    data = base64.b64decode(info["result"]["value"]["data"][0])
    if len(data) == cls.calc_size() + 8:
        return cls.from_bytes(data[8:])
    return cls.from_bytes(data)


def get_account_info(event):
    try:
        return [event.event_data.callback_info.user_account]
    except:
        return [
            event.event_data.maker_callback_info.user_account,
            event.event_data.taker_callback_info.user_account,
        ]


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

WS_URI = "wss://api.devnet.solana.com/"
RPC_URL = "https://api.devnet.solana.com"

parser = AccountParser()
parser.register_parser(pids.DEX_PROGRAM_ID, dex_parser)
parser.register_parser(pids.INSTRUMENTS_PROGRAM_ID, instr_parser)
parser.register_parser(pids.AOB_PROGRAM_ID, aob_parser)
set_global_parser(parser)
set_global_client(Client(RPC_URL))


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


async def settle_funds(market_product_group):
    clock = load_account_as(SYSVAR_CLOCK_PUBKEY, Clock)
    for product in market_product_group.market_products:
        if product:
            product_pubkey = product.product_key
            derivative_metadata = load_account_as(product_pubkey, DerivativeMetadata)
            if not derivative_metadata:
                continue
            print(f"Considering Product {product_pubkey}")
            print(f"    Current Funding per Share: {product.cum_funding_per_share}")
            last_funding_ts = derivative_metadata.last_funding_time
            next_funding_ts = (
                last_funding_ts + derivative_metadata.minimum_funding_period
            )
            curr_ts = clock.unix_timestamp
            print(f"    Current Time: {curr_ts}")
            print(f"    Next Funding: {next_funding_ts} (last={last_funding_ts})")
            print(f"    Time Until Next Funding: {next_funding_ts - curr_ts}")
            if curr_ts < next_funding_ts:
                print("    -> Funding period has not elapsed")
                continue
            print("Oracle:", derivative_metadata.price_oracle)
            _, resp = instr_actions.settle_derivative(
                market_product_group_pubkey,
                product.product_key,
                payer.public_key,
                derivative_metadata.price_oracle,
            )
            print(resp.log_messages)
        else:
            print("all products settled!")
            break


async def run():
    while True:
        try:
            market_product_group = load_account_as(
                market_product_group_pubkey, MarketProductGroup
            )
            await settle_funds(market_product_group)
            time.sleep(1)
        except:
            continue


asyncio.run(run())
