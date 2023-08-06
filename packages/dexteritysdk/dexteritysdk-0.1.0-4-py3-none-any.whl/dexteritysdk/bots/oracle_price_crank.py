import asyncio
import argparse
import base64

from jsonrpcserver import Error
from dexteritysdk.dummy_oracle.state.oracle_price import OraclePrice
from dexteritysdk.dummy_oracle.api import OracleAPI
from dexteritysdk.program_ids import ORACLE_PROGRAM_ID
from podite import pod, U64, I64
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.commitment import *
import solana.rpc.types as types
from solana.sysvar import SYSVAR_CLOCK_PUBKEY
import pandas as pd
import numpy as np
import datetime
import json
import websockets as ws
from dexteritysdk.utils import binance_parser


np.random.seed(100)

ap = argparse.ArgumentParser()
ap.add_argument("binance_ticker")
args = ap.parse_args()

bparser = binance_parser.BinanceParser(args.binance_ticker)


clock_key, _ = PublicKey.find_program_address(
    seeds = [
        b"clock",
    ],
    program_id=ORACLE_PROGRAM_ID,
)
oracle_key, _ = PublicKey.find_program_address(
        seeds=[
            b"oracle",
        ],
        program_id=ORACLE_PROGRAM_ID,
    )

print(oracle_key)
print(clock_key)

class Oracle:
    auth = Keypair(b"GOD " * 8)
    oracle_pubkey = oracle_key
    clock_pubkey = clock_key


@pod
class Clock:
    slot: U64
    epoch_start_time: I64
    epoch: U64
    leader_schedule_epoch: U64
    unix_timestamp: I64


# TODO: All of these should be command line args
URL = "http://127.0.0.1:8899"
WS_URI = "ws://127.0.0.1:8900"
ADJ = 100000


oracle_api = OracleAPI(rpc_url=URL)
oracle_api.create_client().request_airdrop(Oracle.auth.public_key, int(50 * 1e9))
print(f"Airdropped SOL to {str(Oracle.auth.public_key)}")


def get_rpc_payload(key):
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "accountSubscribe",
        "params": [
            key,
            {"encoding": "base64", "commitment": "confirmed"},
        ],
    }


clock_payload = get_rpc_payload(str(SYSVAR_CLOCK_PUBKEY))
oracle_payload = get_rpc_payload(str(Oracle.oracle_pubkey))
auth_payload = get_rpc_payload(str(Oracle.auth.public_key))


async def run():
    while True:
        try:
            clock = oracle_api._get_account_data_as(SYSVAR_CLOCK_PUBKEY, Clock)
            book = bparser.get_book()
            bbbo = book.iloc[0]
            bbest_bid = float(bbbo.bid)
            bbest_ask = float(bbbo.ask)
            current_price = int((bbest_ask + bbest_bid)/2)
            break
        except:
            pass

    clock = oracle_api._get_account_data_as(SYSVAR_CLOCK_PUBKEY, Clock)
    try:
        current_oracle = oracle_api.fetch_oracle_price(Oracle.oracle_pubkey)
        if current_oracle.tag._name_ == "UNINITIALIZED":
            raise Error()
        else:
            print(current_oracle)
            pass
    except:
        print("oracle: None; create a new oracle")
        (
            oracle_api.session(Oracle.auth)
            .initialize_oracle(Oracle.oracle_pubkey, Oracle.auth, current_price)
            .send(
                opts=types.TxOpts(
                    skip_preflight=True,
                    skip_confirmation=False,
                    preflight_commitment=Finalized,
                )
            )
        )
        current_oracle = oracle_api.fetch_oracle_price(Oracle.oracle_pubkey)

    try:
        current_clock = oracle_api.fetch_clock(Oracle.clock)
    except:
        print("clock: None; create a new clock")
        (
            oracle_api.session(Oracle.auth)
            .initialize_clock(Oracle.clock_pubkey, Oracle.auth)
            .send(
                opts=types.TxOpts(
                    skip_preflight=True,
                    skip_confirmation=False,
                    preflight_commitment=Finalized,
                )
            )
        )
        current_clock = oracle_api.fetch_clock(Oracle.clock_pubkey)
    while True:
        async with ws.connect(WS_URI) as w:
            await w.send(json.dumps(clock_payload))
            await w.send(json.dumps(oracle_payload))
            await w.send(json.dumps(auth_payload))
            resp = await (w.recv())
            clock_sub_id = json.loads(resp)["result"]
            resp = await (w.recv())
            oracle_sub_id = json.loads(resp)["result"]
            resp = await (w.recv())
            auth_sub_id = json.loads(resp)["result"]
            while True:
                try:
                    acct = await (w.recv())
                except:
                    break
                payload = json.loads(acct)
                if payload["params"]["subscription"] == clock_sub_id:
                    print(f"clock_sub_id: {clock_sub_id}")
                    data = base64.b64decode(
                        payload["params"]["result"]["value"]["data"][0]
                    )
                    clock = Clock.from_bytes(data)
                    while True:
                        try:
                            book = bparser.get_book()
                            bbbo = book.iloc[0]
                            bbest_bid = float(bbbo.bid)
                            bbest_ask = float(bbbo.ask)
                            price = int((bbest_ask + bbest_bid)/2)
                            break
                        except:
                            pass
                    current_oracle = oracle_api.fetch_oracle_price(Oracle.oracle_pubkey)
                    current_clock = oracle_api.fetch_clock(Oracle.clock_pubkey)
                    print(
                        f"{datetime.datetime.fromtimestamp(clock.unix_timestamp)}"
                        f" Oracle Price: {current_oracle.price}"
                        f" Oracle Clock slot {current_clock.slot}"
                        f" Update to binance price: {price}"
                        f" Oracle Slot: {current_oracle.slot}"
                        f" Clock Slot: {clock.slot}"
                    )
                    print(f"updating the price to: {price} and the clock.")
                    try:
                        (
                            oracle_api.session(Oracle.auth)
                            .update_price(Oracle.oracle_pubkey, Oracle.auth, price)
                            .update_clock(Oracle.clock_pubkey, Oracle.auth, clock.slot, clock.epoch_start_time, clock.epoch, clock.leader_schedule_epoch, clock.unix_timestamp)
                            .send()
                        )
                    except:
                        print("update price error")
                        break
                elif payload["params"]["subscription"] == oracle_sub_id:
                    print(f"oracle_sub_id: {oracle_sub_id}")
                    data = base64.b64decode(
                        payload["params"]["result"]["value"]["data"][0]
                    )
                    current_oracle = OraclePrice.from_bytes(data)
                elif payload["params"]["subscription"] == auth_sub_id:
                    print(f"auth_sub_id: {auth_sub_id}")
                    if payload["params"]["result"]["value"]["lamports"] <= 5000:
                        print('request airdrop')
                        try:
                            oracle_api.create_client().request_airdrop(
                                Oracle.auth.public_key, int(5 * 1e9)
                            )
                        except:
                            print('request failed')
                            break


asyncio.run(run())
