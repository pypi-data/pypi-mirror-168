import os

import solana.system_program
import solana.sysvar
import spl.token.constants
from solana.publickey import PublicKey
# from solmate import set_pid_by_protocol_name

from dexteritysdk.scripts import extract_program_ids

try:
    programs = extract_program_ids.get_program_to_id()
except:
    programs = {}

RENT_PROGRAM_ID = solana.sysvar.SYSVAR_RENT_PUBKEY
CLOCK_PROGRAM_ID = solana.sysvar.SYSVAR_CLOCK_PUBKEY
SYSTEM_PROGRAM_ID = solana.system_program.SYS_PROGRAM_ID
SPL_TOKEN_PROGRAM_ID = spl.token.constants.TOKEN_PROGRAM_ID

DEX_PROGRAM_ID = PublicKey(
    os.environ.get("DEX", programs.get("dex", ""))
)
INSTRUMENTS_PROGRAM_ID = PublicKey(
    os.environ.get("INSTRUMENTS", programs.get("instruments", ""))
)
ORACLE_PROGRAM_ID = PublicKey(
    os.environ.get("DUMMY_ORACLE", programs.get("dummy_oracle", ""))
)
# NOOP_RISK_ENGINE_PROGRAM_ID = PublicKey(
#     os.environ.get("NOOP_RISK_ENGINE", programs.get("noop_risk_engine", ""))
# )
# SIMPLE_RISK_ENGINE_PROGRAM_ID = PublicKey(
#     os.environ.get("SIMPLE_RISK_ENGINE", "4HzqJ5fXcE5W1YTLa8m6M3cdSuGGjuBmDy9zNSTSnkJY")  # todo remove
# )
# ALPHA_RISK_ENGINE_PROGRAM_ID = PublicKey(
#     os.environ.get("ALPHA_RISK_ENGINE", programs.get("alpha_risk_engine", ""))
# )

# this is to get things going as this is imported in a few places but seems unused
ALPHA_RISK_ENGINE_PROGRAM_ID = PublicKey(1)

RISK_ENGINE_PROGRAM_ID = PublicKey(
    os.environ.get("RISK_ENGINE", "")
)
AOB_PROGRAM_ID = PublicKey(
    os.environ.get("AGNOSTIC_ORDERBOOK",
                   programs.get("agnostic_orderbook", "aaobKniTtDGvCZces7GH5UReLYP671bBkB96ahr9x3e"))
)
CONSTANT_FEES_MODEL_PROGRAM_ID = PublicKey(
    os.environ.get("CONSTANT_FEES", programs.get("constant_fees", ""))
)

# todo: make this ~better~ -> work...
# set_pid_by_protocol_name("risk", ALPHA_RISK_ENGINE_PROGRAM_ID)
# set_pid_by_protocol_name("dex", DEX_PROGRAM_ID)
# set_pid_by_protocol_name("instruments", INSTRUMENTS_PROGRAM_ID)
