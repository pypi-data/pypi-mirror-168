# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
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


# LOCK-BEGIN[ix_cls(setup_capital_limits)]: DON'T MODIFY
@dataclass
class SetupCapitalLimitsIx:
    program_id: PublicKey

    # account metas
    authority: AccountMeta
    market_product_group: AccountMeta
    capital_limits_state: AccountMeta
    system_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.authority)
        keys.append(self.market_product_group)
        keys.append(self.capital_limits_state)
        keys.append(self.system_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.SETUP_CAPITAL_LIMITS))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(setup_capital_limits)]: DON'T MODIFY
def setup_capital_limits(
    authority: Union[str, PublicKey, AccountMeta],
    market_product_group: Union[str, PublicKey, AccountMeta],
    capital_limits_state: Union[str, PublicKey, AccountMeta],
    system_program: Union[str, PublicKey, AccountMeta] = PublicKey("11111111111111111111111111111111"),
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PublicKey("FUfpR31LmcP1VSbz5zDaM7nxnH55iBHkpwusgrnhaFjL")

    if isinstance(authority, (str, PublicKey)):
        authority = to_account_meta(
            authority,
            is_signer=True,
            is_writable=True,
        )
    if isinstance(market_product_group, (str, PublicKey)):
        market_product_group = to_account_meta(
            market_product_group,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(capital_limits_state, (str, PublicKey)):
        capital_limits_state = to_account_meta(
            capital_limits_state,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(system_program, (str, PublicKey)):
        system_program = to_account_meta(
            system_program,
            is_signer=False,
            is_writable=False,
        )

    return SetupCapitalLimitsIx(
        program_id=program_id,
        authority=authority,
        market_product_group=market_product_group,
        capital_limits_state=capital_limits_state,
        system_program=system_program,
        remaining_accounts=remaining_accounts,
    ).to_instruction()

# LOCK-END
