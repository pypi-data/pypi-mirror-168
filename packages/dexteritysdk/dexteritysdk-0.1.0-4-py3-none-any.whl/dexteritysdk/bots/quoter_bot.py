#!/usr/bin/env python3

from __future__ import annotations
import asyncio
import signal
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Any, Tuple, Dict
import argparse

from loguru import logger

from pythclient.pythclient import PythClient  # noqa
from pythclient.ratelimit import RateLimit  # noqa
from pythclient.pythaccounts import PythPriceAccount, PythPriceType  # noqa
from pythclient.utils import get_key  # noqa
from solana.keypair import Keypair
from solana.rpc.api import Client

import dexteritysdk.utils.solana
from dexteritysdk.codegen.dex.types import TraderRiskGroup
from dexteritysdk.codegen.instruments.types import DerivativeMetadata
from dexteritysdk.dex.sdk_context import SDKContext, SDKTrader
from dexteritysdk.program_ids import *
from dexteritysdk.utils.solana import explore
from dexteritysdk.utils.aob import Side
from spl.token import instructions
import base58
import base64

logger.enable("pythclient")

RateLimit.configure_default_ratelimit(overall_cps=9, method_cps=3, connection_cps=3)

to_exit = False

DEVNET_URL = "https://api.devnet.solana.com"
MAINNET_URL = "https://api.mainnet-beta.solana.com"

async def refresh_prices(
        price_map: Dict[str, Tuple[float, float]],
        symbols: List[str],
        c: PythClient,
):
    await c.refresh_all_prices()
    products = await c.get_products()
    for p in products:
        if p and "symbol" in p.attrs and p.attrs["symbol"] in symbols:
            print(p.key, p.attrs)
            prices = await p.get_prices()
            for _, pr in prices.items():
                price_map[p.attrs["symbol"]] = (
                    p.prices[PythPriceType.PRICE].aggregate_price,
                    p.prices[PythPriceType.PRICE].aggregate_price_confidence_interval,
                )


async def subscribe_to_prices(
        price_map: Dict[str, Tuple[float, float]],
        symbols: List[str],
        loop=True,
):
    # TODO these calls have been timing out a lot
    # v2_first_mapping_account_key = get_key("devnet", "mapping")
    # v2_program_key = get_key("devnet", "program")

    v2_first_mapping_account_key = "BmA9Z6FjioHJPpjT39QazZyhDRUdZy2ezwx4GiDdE2u2"
    v2_program_key = "gSbePebfvPy7tRqimPoVecS2UsBvYv46ynrzWocc92s"

    use_program = True
    async with PythClient(
        first_mapping_account_key=v2_first_mapping_account_key,
        program_key=v2_program_key if use_program else None,
    ) as c:
        await refresh_prices(price_map, symbols, c)

        if loop:
            while True:
                if to_exit:
                    break

                await refresh_prices(price_map, symbols, c)
                await asyncio.sleep(1)


@dataclass
class FairPrice:
    theo: float
    edge: float


def trade_loop(
        sdk: SDKContext,
        trader: SDKTrader,
        price_map: Dict,
        edge_pct: float,
        size: float,
        cancel_thres: float
):
    last_fair = None
    order_map = defaultdict(dict)  # product id -> { side -> order id }
    trader.cancel_all_orders(sdk, list(range(9)))

    while True:
        if to_exit:
            break

        update_quotes = False
        price = price_map["Crypto.BTC/USD"][0]

        edge = price * edge_pct

        if last_fair is None:
            last_fair = FairPrice(price, edge)
        fair = last_fair

        if fair.theo + fair.edge > price > fair.theo - fair.edge:
            diff = min(fair.theo + fair.edge - price, price - fair.theo + fair.edge)
            ratio = diff / (fair.edge * 2)
            update_quotes |= ratio < cancel_thres
        else:
            update_quotes = True

        if update_quotes:

            for product in sdk.products[0:1]:
                meta: DerivativeMetadata = explore(product.key).data_obj
                funding_period = meta.initialization_time + meta.full_funding_period - time.time()

                # This is the assumed RFR of the futures curve over a year. Represented as bips.
                rfr = 420
                dte = funding_period / 86400  # seconds in a day
                premium = (rfr * dte / 365) * price / 10000

                product_key_str = str(product.key)

                if product_key_str not in order_map or Side.ASK not in order_map[product_key_str]:
                    print(f"Placing ask order for product {product.name} {product.key} "
                          f"for {size}@{price + edge + premium}")
                    order_summary = trader.place_order(
                        sdk, product, Side.ASK, size, price + edge + premium)
                    print(order_summary)
                    if order_summary.order_id is None:
                        print(f"Order fully filled {order_summary}")
                    else:
                        print(f"Order in book, id={order_summary.order_id}")
                        order_map[product_key_str][Side.ASK] = order_summary.order_id
                else:
                    order_id = order_map[product_key_str][Side.ASK]
                    print(f"Replacing ask order {order_id} for product {product.name} {product.key} "
                          f"for {size}@{price + edge + premium}")
                    order_summary = trader.replace(
                        sdk, product, order_id, Side.ASK, size, price + edge + premium)
                    print(order_summary)
                    if order_summary.order_id is None:
                        print(f"Order fully filled {order_summary}")
                        del order_map[product_key_str][Side.ASK]
                    else:
                        print(f"Order in book, id={order_summary.order_id}")
                        order_map[product_key_str][Side.ASK] = order_summary.order_id

                if product_key_str not in order_map or Side.BID not in order_map[product_key_str]:
                    print(f"Placing bid order for product {product.name} {product.key} "
                          f"for {size}@{price - edge + premium}")
                    order_summary = trader.place_order(
                        sdk, product, Side.BID, size, price - edge + premium)
                    print(order_summary)
                    if order_summary.order_id is None:
                        print(f"Order fully filled {order_summary}")
                    else:
                        print(f"Order in book, id={order_summary.order_id}")
                        order_map[product_key_str][Side.BID] = order_summary.order_id
                else:
                    order_id = order_map[product_key_str][Side.BID]
                    print(f"Replacing bid order {order_id} for product {product.name} {product.key} "
                          f"for {size}@{price - edge + premium}")
                    order_summary = trader.replace(
                        sdk, product, order_id, Side.BID, size, price - edge + premium)
                    print(order_summary)
                    if order_summary.order_id is None:
                        print(f"Order fully filled {order_summary}")
                        del order_map[product_key_str][Side.BID]
                    else:
                        print(f"Order in book, id={order_summary.order_id}")
                        order_map[product_key_str][Side.BID] = order_summary.order_id


            last_fair = FairPrice(price, edge)


def set_to_exit(sig: Any, frame: Any):
    global to_exit
    to_exit = True


signal.signal(signal.SIGINT, set_to_exit)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--market_product_group", required=True, type=PublicKey)
    ap.add_argument("-t", "--trader_risk_group", type=PublicKey)
    ap.add_argument("-b", "--bps", type=int)
    ap.add_argument("-c", "--cancel_bps", type=int)
    ap.add_argument("-s", "--size", default=1, type=int)
    ap.add_argument("-n", "--network", default=DEVNET_URL)
    ap.add_argument("-d", "--deposit", type=float, default=0.0)
    ap.add_argument("-x", "--mint", type=float, default=0.0)
    args = ap.parse_args()

    mpg_key = args.market_product_group
    print(f"market product group: {mpg_key}")

    client = Client(args.network)

    keypair_bytes = base58.b58decode(os.environ["PRIVATE_KEY"])
    keypair = Keypair.from_secret_key(keypair_bytes)
    print(f"keypair pubkey = {keypair.public_key}")

    sdk = SDKContext.connect(
        client,
        market_product_group_key=mpg_key,
        payer=keypair,
        **programs,
        raise_on_error=True
    )

    wallet = instructions.get_associated_token_address(keypair.public_key, sdk.vault_mint)
    print(f"wallet = {wallet}")

    if args.trader_risk_group is None:
        print(f"Registering trader")
        trader = sdk.register_trader(keypair, wallet)
        trg_key = trader.account
        print(f"Registered successfully")
    else:
        trg_key = args.trader_risk_group

    print(f"trg = {trg_key}")

    trg: TraderRiskGroup = explore(trg_key).data_obj

    trader = SDKTrader.connect(
        sdk, trg_key, keypair, wallet, trg.risk_state_account, dex_program=DEX_PROGRAM_ID)
    print(f"trader cash balance is {trg.cash_balance.value}")

    if args.mint > 0.0:
        print(f"minting {args.mint}")
        mint_ix = instructions.mint_to_checked(
            instructions.MintToCheckedParams(
                program_id=SPL_TOKEN_PROGRAM_ID,
                amount=int(args.mint * (10**6)),
                decimals=6,
                dest=wallet,
                mint=sdk.vault_mint,
                mint_authority=keypair.public_key,
            )
        )
        dexteritysdk.utils.solana.send_instructions(mint_ix)

    if args.deposit > 0.0:
        print(f"depositing {args.deposit}")
        trader.deposit(sdk, args.deposit)

    price_map = {}

    print(sdk.products[0].name)
    book = sdk.products[0].get_orderbook(sdk)

    for o in book.bids:
        print(f"Found bid {o.order_id} - {o.qty}@{o.price}")

    for o in book.asks:
        print(f"Found ask {o.order_id} - {o.qty}@{o.price}")

    await subscribe_to_prices(price_map, ["Crypto.BTC/USD"], loop=False)
    asyncio.create_task(subscribe_to_prices(price_map, ["Crypto.BTC/USD"]))

    trade_loop(sdk, trader, price_map, 0.02, 1, 0.75)


asyncio.run(main())
