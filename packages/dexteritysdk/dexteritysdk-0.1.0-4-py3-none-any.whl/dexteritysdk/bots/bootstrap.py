import argparse
import json
from pathlib import Path
from re import M

import solana.system_program as sp
import time
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc import types
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
from solana.transaction import Transaction

import dexteritysdk.codegen.dex as cd
import dexteritysdk.codegen.dex.types as dex
import dexteritysdk.constant_fees.actions as fee_act
import dexteritysdk.dex.actions as dex_act
import dexteritysdk.dex.addrs as dex_addrs

import dexteritysdk.dummy_oracle.actions as oracle_act
import dexteritysdk.instruments.actions as ins_act

# from dexteritysdk.dex.state import account_parser as dex_account_parser
from dexteritysdk.program_ids import (
    CLOCK_PROGRAM_ID,
    DEX_PROGRAM_ID,
    AOB_PROGRAM_ID,
    ALPHA_RISK_ENGINE_PROGRAM_ID,
)
from dexteritysdk.risk.actions import initialize_risk_config_acct
from dexteritysdk.utils.aob import Side
from dexteritysdk.utils.aob import account_parser as aob_account_parser
from dexteritysdk.utils.random_hash import random_hash
from dexteritysdk.utils.solana import (
    AccountParser,
    Context,
    send_transaction,
)

SUCCESS = "\u2705"


PYTH_PRODUCT_KEYS = {
    "Crypto.ETH/USD": PublicKey("EdVCmQ9FSPcVe5YySXDPCRmc8aDQLKJ9xvYBMZPie1Vw"),
    "Crypto.BTC/USD": PublicKey("HovQMDrbAgAYPCmHVSrezcSmkMtXSSUsLDFANExrZh2J"),
}

MINT_DECIMALS = 6


def ensure_mint_exists(auth: PublicKey, mint: PublicKey):
    print("Ensuring mint exists...", end="", flush=True)

    mint_key, resp = dex_act.init_mint(
        authority=auth,
        mint=mint,
        mint_decimals=MINT_DECIMALS,
    )

    if mint_key is None:
        raise RuntimeError(
            f"On-chain error happened while creating mint: {resp.tx_string}"
        )
    else:
        print(SUCCESS)
    return mint_key


def ensure_fee_model_exists(auth: Keypair, mpg_seed: str):
    print("Ensuring fee acounts exists...", end="", flush=True)

    mpg_key = dex_addrs.get_market_product_group_addr(auth.public_key, mpg_seed)

    fee_model_key = fee_act.get_fee_model_configuration_addr(mpg_key)
    _, resp = fee_act.update_fees(
        auth.public_key,
        fee_model_config_acct=fee_model_key,
        market_product_group=mpg_key,
        maker_fee_bps=0,
        taker_fee_bps=0,
    )

    if resp.error:
        raise RuntimeError(
            f"On-chain error happened while creating fee accounts: {resp.tx_string}"
        )
    else:
        print(SUCCESS)
        return fee_model_key


def ensure_oracle(auth, oracle, price, decimals=6):
    print(f"Ensuring oracle {oracle.public_key} exists...", end="", flush=True)
    oracle_key, resp = oracle_act.initialize_oracle(
        authority=auth.public_key,
        oracle=oracle.public_key,
        price=price * 10**decimals,
        decimals=decimals,
    )
    if resp.error:
        print("\n".join(resp.log_messages))
        raise RuntimeError(
            f"On-chain error happened while creating market product group: {resp.tx_string}"
        )
    else:
        print(SUCCESS)


def ensure_clock(auth, clock):
    print(f"Ensuring clock {clock.public_key} exists...", end="", flush=True)
    clock_key, resp = oracle_act.initialize_clock(
        authority=auth.public_key,
        clock=clock.public_key,
    )
    if resp.error:
        print("\n".join(resp.log_messages))
        raise RuntimeError(
            f"On-chain error happened while creating market product group: {resp.tx_string}"
        )
    else:
        print(SUCCESS)


def ensure_mpg_exists(
    auth: Keypair,
    mpg_seed: str,
    mint_key: PublicKey,
    fee_model_key: PublicKey,
    risk_model_key: PublicKey,
):
    print("Ensuring market product group exists...", end="", flush=True)

    mpg_key, mpg_resp = dex_act.create_market_product_group(
        authority=auth.public_key,
        seed=str(mpg_seed),
        vault_mint=mint_key,
        risk_engine_program=ALPHA_RISK_ENGINE_PROGRAM_ID,
        fee_collector=auth.public_key,
        fee_model_configuration_acct=fee_model_key,
    )

    if mpg_key is None:
        raise RuntimeError(
            f"On-chain error happened while creating market product group: {mpg_resp.tx_string}"
        )

    # Create risk model
    risk_model_key, risk_model_resp = dex_act.create_risk_config_acct(
        authority=auth.public_key,
        group=mpg_key,
    )

    if risk_model_key is None:
        raise RuntimeError(
            f"On-chain error happened while creating risk model: {risk_model_resp.tx_string}"
        )

    vault = PublicKey.find_program_address(
        [b"market_vault", bytes(mpg_key)], cd.PROGRAM_ID
    )[0]
    _, mpg_resp = dex_act.init_market_product_group(
        authority=auth.public_key,
        seed=str(mpg_seed),
        vault_mint=mint_key,
        vault=vault,
        fee_collector=auth.public_key,
        fee_model_configuration_acct=fee_model_key,
        risk_engine_program=ALPHA_RISK_ENGINE_PROGRAM_ID,
        risk_model_configuration_acct=risk_model_key,
    )

    # initialize risk model
    _, config_resp = initialize_risk_config_acct(
        admin=auth.public_key, market_product_group=mpg_key
    )

    # RiskOutputRegister
    out_register_risk_key, risk_resp = dex_act.create_risk_register(
        authority=auth.public_key,
        group=mpg_key,
        register_size=dex_act.OUT_REGISTER_RISK_SIZE,
        program_id=ALPHA_RISK_ENGINE_PROGRAM_ID,
        layout_str=dex_act.OUT_REGISTER_RISK_LAYOUT,
    )

    _, _ = dex_act.create_fee_register(
        authority=auth.public_key,
        group=mpg_key,
        register_size=16,
    )

    if mpg_key is None:
        raise RuntimeError(
            f"On-chain error happened while initializing market product group: {mpg_resp.tx_string}"
        )
    elif out_register_risk_key is None:
        raise RuntimeError(
            f"On-chain error happened while creating risk register: {risk_resp.tx_string}"
        )
    else:
        print(SUCCESS)
        return mpg_key


def ensure_product_exists(auth, name, defn, mpg_key):
    print(f"Ensuring market product [{name}] exists...", end="", flush=True)

    product_key, resp = ins_act.initialize_derivative(
        payer=auth.public_key,
        close_authority=auth.public_key,
        **defn,
    )
    if product_key is None:
        raise RuntimeError(
            f"On-chain error happened while initializing derivative: {resp.tx_string}"
        )
    _, resp = dex_act.create_market_product(
        auth.public_key,
        market_product_group=mpg_key,
        product_key=product_key,
        name=name,
        tick_size=0.1,
        base_decimals=10,
    )
    if False:
        raise RuntimeError(
            f"On-chain error happened while creating market product group: {resp.tx_string}"
        )
    else:
        print(SUCCESS)

        for pyth_key, pk in PYTH_PRODUCT_KEYS.items():
            if str(pk) == str(defn["price_oracle"]):
                return product_key, pyth_key

        return product_key, None


def ensure_combo_exists(auth, name, mpg_key, product_keys, ratios):
    print(f"Ensuring combo [{name}] exists...", end="", flush=True)

    product_key = dex_act.get_combo_product_key(product_keys, ratios)

    _, resp = dex_act.create_combo(
        auth.public_key,
        market_product_group=mpg_key,
        products=product_keys,
        ratios=ratios,
        name=name,
        tick_size=0.1,
    )
    if mpg_key is None:
        raise RuntimeError(
            f"On-chain error happened while creating market product group: {resp.tx_string}"
        )
    else:
        print(SUCCESS)

    return product_key


def ensure_trader_has_tokens(auth, mint_key):
    print(auth, mint_key)
    _, _ = dex_act.init_trader_mint_account(auth.public_key, mint_key)
    _, _ = dex_act.mint_to_trader(
        auth.public_key,
        mint_key,
        auth.public_key,
        int(100000 * (10**MINT_DECIMALS)),
        MINT_DECIMALS,
    )

    # TODO add some checks here


def update_clock(
    clock: PublicKey,
    slot: int = 0,
    epoch_start_timestamp: int = 0,
    epoch: int = 0,
    leader_schedule_epoch: int = 0,
    unix_timestamp: int = 0,
):
    oracle_act.update_clock(
        clock,
        slot,
        epoch_start_timestamp,
        epoch,
        leader_schedule_epoch,
        unix_timestamp,
    )


def transfer_sol_to(auth, trader_key, amount):
    ix = sp.transfer(
        sp.TransferParams(
            from_pubkey=auth.public_key,
            to_pubkey=trader_key.public_key,
            lamports=int(amount * 1e9),
        )
    )
    signers = [auth]
    tx = Transaction().add(ix)
    resp = send_transaction(
        tx,
        *signers,
        opts=types.TxOpts(
            skip_preflight=False,
            skip_confirmation=False,
            preflight_commitment=Confirmed,
        ),
    )

    if resp.error:
        raise RuntimeError(f"Transfering sol to quoter failed: {resp.tx_string}")


def setup_trader(
    i, auth, mpg_key, mint_key, trader_key: Keypair, sol_amount, deposit_amount
):
    print(f"Setting up quoter [{i}]...", end="", flush=True)

    transfer_sol_to(auth, trader_key, sol_amount)

    Context.add_signers((trader_key, "trader" + str(i)))
    risk_group, resp = dex_act.create_trader_risk_group(
        trader_key.public_key, mpg_key, program_id=ALPHA_RISK_ENGINE_PROGRAM_ID
    )
    if risk_group is None:
        raise RuntimeError(f"Creating trader risk group failed: {resp.tx_string}")

    token_account, resp = dex_act.init_trader_mint_account(
        trader_key.public_key, mint_key
    )
    if token_account is None:
        raise RuntimeError(f"Creating trader mint account failed: {resp.tx_string}")

    _, resp = dex_act.mint_to_trader(
        trader_key.public_key,
        mint_key,
        auth.public_key,
        int(deposit_amount * (10**MINT_DECIMALS)),
        MINT_DECIMALS,
    )
    if resp.error:
        raise RuntimeError(f"Minting to quoter failed: {resp.tx_string}")

    _, resp = dex_act.deposit_funds(
        trader_key.public_key, token_account, mpg_key, int(deposit_amount)
    )
    if resp.error:
        raise RuntimeError(f"Depositing fund failed: {resp.tx_string}")

    print(SUCCESS)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mint-seed", dest="mint_seed", required=False, default=random_hash()
    )
    parser.add_argument(
        "--mpg-seed", dest="mpg_seed", required=False, default=random_hash()
    )
    parser.add_argument(
        "--no-output", dest="no_output", action="store_true", default=False
    )
    parser.add_argument("--local", dest="local", action="store_true", default=False)
    parser.add_argument("--test", dest="test", action="store_true", default=False)

    return parser.parse_args()


def main():
    args = get_arguments()

    mint_seed = args.mint_seed
    mpg_seed = args.mpg_seed

    parser = AccountParser()
    # parser.register_parser(DEX_PROGRAM_ID, dex_account_parser)
    parser.register_parser(AOB_PROGRAM_ID, aob_account_parser)

    auth = Keypair(b"nima" * 8)
    mint = Keypair()

    if args.local:
        print("Using local validator.")
        RPC_URL = "http://127.0.0.1:8899"
    else:
        print("Using devnet.")
        RPC_URL = "https://api.devnet.solana.com"

    client = Client(RPC_URL)

    if args.local:
        resp = client.request_airdrop(auth.public_key, int(1000 * 1e9))
        time.sleep(3)

    Context.init_globals(
        fee_payer=auth,
        client=client,
        signers=[(auth, "auth"), (mint, "mint")],
        parser=parser,
    )
    mint_key = ensure_mint_exists(auth.public_key, mint.public_key)
    fee_model_key = ensure_fee_model_exists(auth, mpg_seed)
    risk_model_key = dex_act.create_risk_model_configuration_acct(
        auth, program_id=ALPHA_RISK_ENGINE_PROGRAM_ID
    )
    mpg_key = ensure_mpg_exists(
        auth=auth,
        mpg_seed=mpg_seed,
        mint_key=mint.public_key,
        fee_model_key=fee_model_key,
        risk_model_key=risk_model_key,
    )

    # creating products
    start_time = int(time.time()) + 60

    if args.test:
        btc = Keypair()
        eth = Keypair()
        clock_keypair = Keypair()
        clock = clock_keypair.public_key
        ensure_oracle(auth, btc, 50000)
        ensure_oracle(auth, eth, 4000)
        ensure_clock(auth, clock_keypair)
        update_clock(clock, unix_timestamp=int(start_time - 1))
        oracles = {}
        oracles["Crypto.BTC/USD"] = btc.public_key
        oracles["Crypto.ETH/USD"] = eth.public_key
        oracle_type = ins_act.OracleType.DUMMY

    else:
        oracles = PYTH_PRODUCT_KEYS
        clock = CLOCK_PROGRAM_ID
        oracle_type = ins_act.OracleType.PYTH

    product_definitions = {
        "BTC-PERP": dict(
            price_oracle=oracles["Crypto.BTC/USD"],
            market_product_group=mpg_key,
            instrument_type=ins_act.InstrumentType.RECURRING_CALL,
            strike=0,
            full_funding_period=3600 * 24,  # in seconds
            minimum_funding_period=60,  # in seconds
            initialization_time=start_time,
            oracle_type=oracle_type,
            clock=clock,
        ),
        "ETH-PERP": dict(
            price_oracle=oracles["Crypto.ETH/USD"],
            market_product_group=mpg_key,
            instrument_type=ins_act.InstrumentType.RECURRING_CALL,
            strike=0,
            full_funding_period=3600 * 24,  # in seconds
            minimum_funding_period=60,  # in seconds
            initialization_time=start_time,
            oracle_type=oracle_type,
            clock=clock,
        ),
        "BTC-FUT-M1": dict(
            price_oracle=oracles["Crypto.BTC/USD"],
            market_product_group=mpg_key,
            instrument_type=ins_act.InstrumentType.EXPIRING_CALL,
            strike=0,
            full_funding_period=15 * 60,  # in seconds
            minimum_funding_period=15 * 60,  # in seconds
            initialization_time=start_time,
            oracle_type=oracle_type,
            clock=clock,
        ),
        "BTC-FUT-M2": dict(
            price_oracle=oracles["Crypto.BTC/USD"],
            market_product_group=mpg_key,
            instrument_type=ins_act.InstrumentType.EXPIRING_CALL,
            strike=0,
            full_funding_period=60 * 60,  # in seconds
            minimum_funding_period=60 * 60,  # in seconds
            initialization_time=start_time,
            oracle_type=oracle_type,
            clock=clock,
        ),
        "ETH-FUT-M1": dict(
            price_oracle=oracles["Crypto.ETH/USD"],
            market_product_group=mpg_key,
            instrument_type=ins_act.InstrumentType.EXPIRING_CALL,
            strike=0,
            full_funding_period=15 * 60,  # in seconds
            minimum_funding_period=15 * 60,  # in seconds
            initialization_time=start_time,
            oracle_type=oracle_type,
            clock=clock,
        ),
    }

    combo_definitions = {
        "BTC-CAL-SPR": dict(
            market_product_group=mpg_key,
            products=["BTC-FUT-M1", "BTC-FUT-M2"],
            ratios=[-1, 1],
        ),
        "BTC-ETH-M1-SPR": dict(
            market_product_group=mpg_key,
            products=["BTC-FUT-M1", "ETH-FUT-M1"],
            ratios=[1, -1],  # note: currently this should be positive in price space!
        ),
    }

    product_keys = {}
    product_oracles = {}
    for name, defn in product_definitions.items():
        prod_key, pyth_key = ensure_product_exists(auth, name, defn, mpg_key)

        product_keys[name] = str(prod_key)
        product_oracles[name] = str(pyth_key)

    combo_keys = {}
    combo_weights = {}
    for name, defn in combo_definitions.items():
        prod_key = ensure_combo_exists(
            auth,
            name,
            mpg_key,
            product_keys=[PublicKey(product_keys[k]) for k in defn["products"]],
            ratios=defn["ratios"],
        )

        combo_keys[name] = str(prod_key)
        combo_weights[name] = [(k, w) for k, w in zip(defn["products"], defn["ratios"])]

    # initialize trader risk group and quoters
    ensure_trader_has_tokens(auth, mint_key)
    quoters = []
    quoter_keys = []
    for i in range(5):
        quoter_seed = f"{mpg_seed}_quoter{i}".ljust(32, " ").encode()
        quoter = Keypair(quoter_seed)
        setup_trader(i, auth, mpg_key, mint_key, quoter, 1, 100000000)
        quoters.append(quoter_seed.decode("ascii"))
        quoter_keys.append(quoter)

    # dumping the config
    config = dict(
        mint_seed=mint_seed.ljust(32),
        mpg_key=str(mpg_key),
        quoters=quoters,
        product_keys=product_keys,
        product_oracles=product_oracles,
        combo_keys=combo_keys,
        combo_weights=combo_weights,
    )

    config_str = json.dumps(config, indent=4)

    print(config_str)

    if not args.no_output:
        with open(Path(__file__).parent / "config.json", "w") as fout:
            print(config_str, file=fout)

    if args.test:
        # Continue running test cases
        Context.set_global_fee_payer(None)
        _, response = dex_act.new_order(
            quoter_keys[0].public_key,
            mpg_key,
            PublicKey(product_keys["BTC-PERP"]),
            Side.BID,
            limit_price=49000,
            max_base_qty=1,
            order_type=dex.OrderType.LIMIT,
        )
        print("\n".join(response.log_messages))
        _, response = dex_act.new_order(
            quoter_keys[0].public_key,
            mpg_key,
            PublicKey(product_keys["BTC-PERP"]),
            Side.ASK,
            limit_price=49950,
            max_base_qty=2,
            order_type=dex.OrderType.LIMIT,
        )
        print("\n".join(response.log_messages))
        _, response = dex_act.new_order(
            quoter_keys[1].public_key,
            mpg_key,
            PublicKey(product_keys["BTC-PERP"]),
            Side.BID,
            limit_price=49951,
            max_base_qty=1,
            order_type=dex.OrderType.LIMIT,
        )
        print("\n".join(response.log_messages))

        _, response = dex_act.consume_orderbook_events(
            mpg_key,
            PublicKey(product_keys["BTC-PERP"]),
            quoter_keys[1].public_key,
            10,
        )
        print("\n".join(response.log_messages))


if __name__ == "__main__":
    main()
