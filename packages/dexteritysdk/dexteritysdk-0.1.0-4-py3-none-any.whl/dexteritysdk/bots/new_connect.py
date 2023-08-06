#!/usr/bin/env python3

import argparse
import os.path

from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana import system_program
import base58

from dexteritysdk.dex.sdk_context import SDKContext
from dexteritysdk.program_ids import programs
from dexteritysdk.utils.solana import Client, send_instructions, Context, explore
from dexteritysdk.codegen.dex.types import Fractional

DEVNET_URL = "https://api.devnet.solana.com"
MAINNET_URL = "https://api.mainnet-beta.solana.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--market_product_group", required=True, type=PublicKey)
    parser.add_argument("-n", "--network", default=DEVNET_URL)
    args = parser.parse_args()
    mpg_key = PublicKey(args.market_product_group)
    print(mpg_key.to_base58())

    payer_keypair_b58 = os.environ["PRIVATE_KEY"]
    payer_keypair_bytes = base58.b58decode(payer_keypair_b58)
    payer_keypair = Keypair.from_secret_key(payer_keypair_bytes)

    client = Client(args.network)
    Context.set_raise_on_error(True)

    sdk = SDKContext.connect(client, market_product_group_key=mpg_key, payer=payer_keypair, **programs, raise_on_error=True)
    trader = create_test_trader(sdk, fund_from_mint=False)


def create_test_trader(sdk: SDKContext, fund_from_mint=True):
    from spl.token import instructions
    from spl.token.constants import TOKEN_PROGRAM_ID

    keypair = Keypair.generate()
    Context.add_signers((keypair, "test_trader"))
    # transfer lamports since 'keypair' will be payer
    send_instructions(system_program.transfer(system_program.TransferParams(
        from_pubkey=sdk.payer.public_key,
        to_pubkey=keypair.public_key,
        lamports=1_000_000_000,  # 1 SOL
    )))

    # create and mint to ata to fund trader
    wallet = instructions.get_associated_token_address(keypair.public_key, sdk.vault_mint)
    ata_ix = instructions.create_associated_token_account(sdk.payer.public_key, keypair.public_key, sdk.vault_mint)
    ixs = [ata_ix]
    if fund_from_mint:
        mint_ix = instructions.mint_to(instructions.MintToParams(
            program_id=TOKEN_PROGRAM_ID,
            mint=sdk.vault_mint,
            dest=wallet,
            mint_authority=sdk.payer.public_key,
            amount=200_000_000,
        ))
        ixs.append(mint_ix)
    else:
        print(f"Please get the MPG admin to mint vault tokens to the trader. The vault token mint is {sdk.vault_mint}")

    send_instructions(*ixs)
    trader = sdk.register_trader(keypair=keypair, wallet=wallet)
    print(f"Trader pubkey is {str(keypair.public_key)}")
    print(f"Trader keypair is {str(base58.b58encode(keypair.secret_key))}")
    print(f"Trader risk group is {str(trader.account)}")
    print(f"Trader vault token ATA is {str(wallet)}")

    # deposit minted tokens to dex
    if fund_from_mint:
        print("Depositing vault tokens to dex")
        trader.deposit(sdk, Fractional(100_000_000, sdk.decimals))

    return trader


if __name__ == '__main__':
    main()
