import os
from dexteritysdk.local_env import *
import sys
import json
import time
import argparse
import base64

from pathlib import Path

import solana.system_program as sp

from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.commitment import Confirmed
from solana.rpc import types
from solana.transaction import Transaction
from dexteritysdk.utils.solana import get_global_parser

import dexteritysdk.dex.actions as dex_act
import dexteritysdk.constant_fees.actions as fee_act
import dexteritysdk.instruments.actions as ins_act
from dexteritysdk.utils.solana import explore, AccountParser
from dexteritysdk.dex.state import account_parser as dex_account_parser
from dexteritysdk.dex.state import ProductStatus, MarketProductGroup, TraderRiskGroup
from dexteritysdk.utils.aob import account_parser as aob_account_parser
from dexteritysdk.instruments.state import account_parser as ins_account_parser
from dexteritysdk.utils.random_hash import random_hash
from dexteritysdk.utils.solana import (
    set_global_client,
    set_signers,
    send_transaction,
    get_global_client,
    get_signers,
)
from dexteritysdk.program_ids import DEX_PROGRAM_ID, AOB_PROGRAM_ID, INSTRUMENTS_PROGRAM_ID


RPC_URL = "https://api.devnet.solana.com"

SUCCESS = "\u2705"


# TODO: move this somewhere better
def query_all_trader_risk_groups(market_product_group: PublicKey):
    client = get_global_client()
    raw_dex_accounts = client.get_program_accounts(
        pubkey=DEX_PROGRAM_ID,
        encoding="base64",
        data_size=TraderRiskGroup.calc_size() + 8,  # currently need constant offset
    )[
        "result"
    ]  # note: this shouldn't have a cap on the number returned right?

    trader_risk_keys = []
    trader_risk_groups = []
    for acct in raw_dex_accounts:
        key = PublicKey(acct["pubkey"])
        trg: TraderRiskGroup = dex_account_parser(
            base64.b64decode(acct["account"]["data"][0])
        )
        if str(trg.market_product_group) == str(market_product_group):
            trader_risk_keys.append(key)
            trader_risk_groups.append(trg)

    return trader_risk_keys, trader_risk_groups


def expiration_routine(auth: PublicKey, mpg_key: PublicKey, product_key: PublicKey):
    mpg_obj: MarketProductGroup = explore(mpg_key).data_obj
    assert isinstance(mpg_obj, MarketProductGroup)
    product_idx = mpg_obj.find_market_index(product_key)
    product_obj = mpg_obj.get_product_by_key(product_key)
    assert product_obj is not None
    combo_objs = mpg_obj.get_combos_for_outright(product_key)
    combo_keys = [c.product_key for c in combo_objs]

    # optional: actually call settle on the instrument
    assert product_obj.product_status == ProductStatus.EXPIRED

    # crank all event queue events (outright and combo) -> all relevant event queues should be empty
    # if we assume that there is an event queue crank running for the market, can just confirm here!
    for key_i in combo_keys + [product_key]:
        product_i = mpg_obj.mpg_obj.get_product_by_key(
            key_i
        ) or mpg_obj.get_combo_by_key(key_i)
        orderbook = explore(product_i.orderbook).data_obj
        event_queue_key = orderbook.event_queue
        event_queue = explore(event_queue_key).data_obj
        while event_queue.header.count > 0:
            _, resp = dex_act.consume_orderbook_events(
                market_product_group=mpg_key,
                product_key=key_i,
                reward_target=auth,
                max_iterations=10,
            )
            # reload event queue to check when empty
            time.sleep(3)
            event_queue = explore(event_queue_key).data_obj

    # query all trader_risk_groups, call settle on each that has open position -> open interest should be zero
    # should be able to confirm that long and short open interest are both zero at the end of this step
    while product_obj.open_long_interest > 0 or product_obj.open_short_interest > 0:
        all_trader_keys, all_trader_risk_groups = query_all_trader_risk_groups(mpg_key)
        for trg_key, trg in zip(all_trader_keys, all_trader_risk_groups):
            if trg.is_active_product(product_idx):
                _, resp = dex_act.update_trader_funding(
                    market_product_group=mpg_key,
                    trader=trg_key,
                    fee_payer=auth,
                )
        # reload objects to confirm that everyone settled
        time.sleep(5)
        mpg_obj = explore(mpg_key).data_obj
        product_obj = mpg_obj.get_product_by_key(product_key)
        print(
            f"product open interest: ({product_obj.open_long_interest}, {product_obj.open_short_interest})"
        )

    # for each combo and product, crank until all open orders canceled and then remove the product from market product group
    for key_i in combo_keys + [product_key]:
        while True:
            _, resp = dex_act.clear_expired_orders(
                market_product_group=mpg_key,
                product_key=key_i,
                authority=auth,
                num_orders_to_cancel=10,
            )

        _, resp = dex_actions.remove_market_product(
            market_product_group=mpg,
            product_key=key_i,
        )


def main():
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

    auth = Keypair(b"nima" * 8)
    market_product_group_pubkey = PublicKey(mpg_pubkey)
    product_key = PublicKey()

    parser = AccountParser()
    parser.register_parser(DEX_PROGRAM_ID, dex_account_parser)
    parser.register_parser(AOB_PROGRAM_ID, aob_account_parser)
    parser.register_parser(INSTRUMENTS_PROGRAM_ID.ins_account_parser)

    client = Client(RPC_URL)
    set_global_client(client)

    set_signers(auth)

    expiration_routine(auth.public_key, market_product_group_pubkey, product_key)


if __name__ == "__main__":
    main()
