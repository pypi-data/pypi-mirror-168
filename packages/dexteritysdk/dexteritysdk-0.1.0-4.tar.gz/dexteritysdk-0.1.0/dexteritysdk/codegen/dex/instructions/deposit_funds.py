# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from dexteritysdk.codegen.dex.types import DepositFundsParams
from dexteritysdk.solmate.utils import to_account_meta
from io import BytesIO
from podite import BYTES_CATALOG
from solana.publickey import PublicKey
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(deposit_funds)]: DON'T MODIFY
@dataclass
class DepositFundsIx:
    program_id: PublicKey

    # account metas
    token_program: AccountMeta
    user: AccountMeta
    user_token_account: AccountMeta
    trader_risk_group: AccountMeta
    market_product_group: AccountMeta
    market_product_group_vault: AccountMeta
    capital_limits: AccountMeta
    whitelist_ata_acct: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    params: DepositFundsParams

    def to_instruction(self):
        keys = []
        keys.append(self.token_program)
        keys.append(self.user)
        keys.append(self.user_token_account)
        keys.append(self.trader_risk_group)
        keys.append(self.market_product_group)
        keys.append(self.market_product_group_vault)
        keys.append(self.capital_limits)
        keys.append(self.whitelist_ata_acct)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.DEPOSIT_FUNDS))
        buffer.write(BYTES_CATALOG.pack(DepositFundsParams, self.params))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(deposit_funds)]: DON'T MODIFY
def deposit_funds(
    user: Union[str, PublicKey, AccountMeta],
    user_token_account: Union[str, PublicKey, AccountMeta],
    trader_risk_group: Union[str, PublicKey, AccountMeta],
    market_product_group: Union[str, PublicKey, AccountMeta],
    market_product_group_vault: Union[str, PublicKey, AccountMeta],
    capital_limits: Union[str, PublicKey, AccountMeta],
    whitelist_ata_acct: Union[str, PublicKey, AccountMeta],
    params: DepositFundsParams,
    token_program: Union[str, PublicKey, AccountMeta] = PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PublicKey("FUfpR31LmcP1VSbz5zDaM7nxnH55iBHkpwusgrnhaFjL")

    if isinstance(token_program, (str, PublicKey)):
        token_program = to_account_meta(
            token_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(user, (str, PublicKey)):
        user = to_account_meta(
            user,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(user_token_account, (str, PublicKey)):
        user_token_account = to_account_meta(
            user_token_account,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(trader_risk_group, (str, PublicKey)):
        trader_risk_group = to_account_meta(
            trader_risk_group,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(market_product_group, (str, PublicKey)):
        market_product_group = to_account_meta(
            market_product_group,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(market_product_group_vault, (str, PublicKey)):
        market_product_group_vault = to_account_meta(
            market_product_group_vault,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(capital_limits, (str, PublicKey)):
        capital_limits = to_account_meta(
            capital_limits,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(whitelist_ata_acct, (str, PublicKey)):
        whitelist_ata_acct = to_account_meta(
            whitelist_ata_acct,
            is_signer=False,
            is_writable=False,
        )

    return DepositFundsIx(
        program_id=program_id,
        token_program=token_program,
        user=user,
        user_token_account=user_token_account,
        trader_risk_group=trader_risk_group,
        market_product_group=market_product_group,
        market_product_group_vault=market_product_group_vault,
        capital_limits=capital_limits,
        whitelist_ata_acct=whitelist_ata_acct,
        remaining_accounts=remaining_accounts,
        params=params,
    ).to_instruction()

# LOCK-END
