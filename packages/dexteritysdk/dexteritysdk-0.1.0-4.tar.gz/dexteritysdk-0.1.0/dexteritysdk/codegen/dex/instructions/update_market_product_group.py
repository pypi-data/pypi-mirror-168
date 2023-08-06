# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from dexteritysdk.codegen.dex.types import UpdateMarketProductGroupParams
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


# LOCK-BEGIN[ix_cls(update_market_product_group)]: DON'T MODIFY
@dataclass
class UpdateMarketProductGroupIx:
    program_id: PublicKey

    # account metas
    authority: AccountMeta
    market_product_group: AccountMeta
    fee_collector: AccountMeta
    staking_fee_collector: AccountMeta
    system_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    params: UpdateMarketProductGroupParams

    def to_instruction(self):
        keys = []
        keys.append(self.authority)
        keys.append(self.market_product_group)
        keys.append(self.fee_collector)
        keys.append(self.staking_fee_collector)
        keys.append(self.system_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.UPDATE_MARKET_PRODUCT_GROUP))
        buffer.write(BYTES_CATALOG.pack(UpdateMarketProductGroupParams, self.params))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(update_market_product_group)]: DON'T MODIFY
def update_market_product_group(
    authority: Union[str, PublicKey, AccountMeta],
    market_product_group: Union[str, PublicKey, AccountMeta],
    fee_collector: Union[str, PublicKey, AccountMeta],
    staking_fee_collector: Union[str, PublicKey, AccountMeta],
    params: UpdateMarketProductGroupParams,
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
            is_writable=True,
        )
    if isinstance(fee_collector, (str, PublicKey)):
        fee_collector = to_account_meta(
            fee_collector,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(staking_fee_collector, (str, PublicKey)):
        staking_fee_collector = to_account_meta(
            staking_fee_collector,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(system_program, (str, PublicKey)):
        system_program = to_account_meta(
            system_program,
            is_signer=False,
            is_writable=False,
        )

    return UpdateMarketProductGroupIx(
        program_id=program_id,
        authority=authority,
        market_product_group=market_product_group,
        fee_collector=fee_collector,
        staking_fee_collector=staking_fee_collector,
        system_program=system_program,
        remaining_accounts=remaining_accounts,
        params=params,
    ).to_instruction()

# LOCK-END
