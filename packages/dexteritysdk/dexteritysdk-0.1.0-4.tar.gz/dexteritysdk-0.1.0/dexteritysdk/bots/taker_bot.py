#!/usr/bin/env python3

# python quoter-bot.py 7 Crypto.BTC/USD AVG4tHmvfGssaDLNddVqbkwwjJH3dPi7h3Yhg7ZqjfaM jarry 10
# python quoter_bot.py BTC_0 Crypto.BTC/USD 9UW8hNAzUhJ9mBScLgcQZYoSLZoPpDqgiFAzF3wP3n5q jarry 1
# python quoter_bot.py BTC_0 Crypto.BTC/USD jjcJHDJ6x7kaTVRrz8GKPYH1y2pUpzRqJHNfDYpHHRy jarry 1
from __future__ import annotations
from dexteritysdk.local_env import *
import asyncio
import signal
import sys
from typing import List, Any
import argparse
import random
import time
import json
import numpy as np

from loguru import logger

from pythclient.pythclient import PythClient  # noqa
from pythclient.ratelimit import RateLimit  # noqa
from pythclient.pythaccounts import PythPriceAccount  # noqa
from pythclient.utils import get_key  # noqa
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.rpc.async_api import AsyncClient


from dexteritysdk.program_ids import *
import dexteritysdk.utils.solana as ctx
import dexteritysdk.dex.actions as dex_act
import dexteritysdk.dex.instructions as dex_ixs
from dexteritysdk.utils.solana import explore, AccountParser
from dexteritysdk.dex.state import account_parser as dex_account_parser
from dexteritysdk.dex.state import OpenOrdersNode
from dexteritysdk.utils.aob import account_parser as aob_account_parser
from dexteritysdk.dex.instructions.common import Side

from dexteritysdk.utils import binance_parser

from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed

MAX_MARKET_PRODUCT = 128

logger.enable("pythclient")

RateLimit.configure_default_ratelimit(overall_cps=9, method_cps=3, connection_cps=3)

to_exit = False

parser = AccountParser()
parser.register_parser(DEX_PROGRAM_ID, dex_account_parser)
parser.register_parser(AOB_PROGRAM_ID, aob_account_parser)


ctx.set_global_parser(parser)
url = "https://api.devnet.solana.com"
ctx.set_global_client(Client(url))

curr_directory = os.path.dirname(os.path.abspath(__file__))
cfg_path = os.path.join(curr_directory, "config.json")
if os.path.exists(cfg_path):
    with open(cfg_path) as f:
        cfg = json.load(f)
        mpg_key = cfg["mpg_key"]

        ap = argparse.ArgumentParser()
        ap.add_argument("prod_name")
        ap.add_argument("binance_ticker")
        ap.add_argument("size", nargs="?", const=1, default=1, type=int)
        ap.add_argument("idx", nargs="?", const=1, default=0, type=int)
        ap.add_argument("positions_limit", nargs="?", const=1, default=1, type=int)
        args = ap.parse_args()
        trader = Keypair(cfg["quoters"][args.idx].encode())
        prod_name = args.prod_name
        oracle = cfg["product_oracles"][prod_name]
        size = args.size

else:
    ap = argparse.ArgumentParser()
    ap.add_argument("prod_name")
    ap.add_argument("binance_ticker")
    ap.add_argument("oracle_prod_name")
    ap.add_argument("mpg_pubkey")
    ap.add_argument("seed")
    ap.add_argument("size", nargs="?", const=1, default=1, type=int)
    ap.add_argument("positions_limit", nargs="?", const=1, default=1, type=int)
    args = ap.parse_args()

    mpg_key = args.mpg_pubkey
    prod_name = args.prod_name

    trader = Keypair(
        bytes(args.seed, "utf-8") + b"1" + b"x" * (31 - len(bytes(args.seed, "utf-8")))
    )
    oracle = args.oracle_prod_name
    size = int(args.min_size)


bparser = binance_parser.BinanceParser(args.binance_ticker)


prev_fair = None

ctx.set_signers(trader)


trader_risk_group = dex_act.get_trader_risk_group_addr(trader.public_key, mpg_key)

market_obj = explore(mpg_key).data_obj
risk_engine = market_obj.risk_engine_program


for idx, product in enumerate(market_obj.market_products):
    if product:
        if product.name == prod_name:
            product_obj = product
            product_idx = idx
            break
    else:
        raise
else:
    raise


orderbook_obj = explore(product_obj.orderbook).data_obj

tick_size = product_obj.tick_size.m * 10 ** (-product_obj.tick_size.exp)


def set_to_exit(sig: Any, frame: Any):
    global to_exit
    to_exit = True


signal.signal(signal.SIGINT, set_to_exit)


def new_order(side, price):
    print(f"Send new order: side: {side}, price: {price}")
    return dex_act.new_order(
        trader=trader.public_key,
        market_product_group=mpg_key,
        product_key=product_obj.product_key,
        side=side,
        limit_price=price,
        max_base_qty=size,
        order_type=dex_ixs.OrderType.IMMEDIATE_OR_CANCEL,
    )


async def get_bbo(side, slab_pubkey):
    if side == Side.ASK:
        func = np.min
        bbo = np.inf
    elif side == Side.BID:
        func = np.max
        bbo = -np.inf
    slab = explore(slab_pubkey).data_obj
    counter = 0
    while True:
        if slab[counter].kind.name == "Leaf":
            order_price = slab[counter].node_data.key // 2 ** 64 // 2 ** 32 * tick_size
            bbo = func((bbo, order_price))
        if slab[counter].kind.name == "Uninitialized":
            break
        counter += 1
    print(f"BBO for side: {side}, price: {bbo}")
    return bbo


async def async_send(*args):
    await asyncio.gather(args)


def get_positions_count(trg):
    trg_obj = explore(trg).data_obj
    position_idx = trg_obj.active_positions[product_idx]
    position = trg_obj.trader_positions[position_idx]
    return position.position.value


async def main():
    global to_exit
    while True:
        try:
            best_bid = await get_bbo(Side.BID, orderbook_obj.bids)
            best_ask = await get_bbo(Side.ASK, orderbook_obj.asks)
            # print(f"best bid: {best_bid}")
            # print(f"best ask: {best_ask}")
            book = bparser.get_book()
            bbbo = book.iloc[0]
            bbest_bid = float(bbbo.bid)
            bbest_ask = float(bbbo.ask)
            positions_count = get_positions_count(trader_risk_group)
            if bbest_bid > best_ask and positions_count <= args.positions_limit:
                print("time to buy")
                new_order(Side.BID, best_ask)
            elif bbest_ask < best_bid and positions_count >= -args.positions_limit:
                print("time to sell")
                new_order(Side.ASK, best_bid)
            time.sleep(0.5)
        except Exception as e:
            print(f"Exception occured: {e}")


asyncio.run(main())
