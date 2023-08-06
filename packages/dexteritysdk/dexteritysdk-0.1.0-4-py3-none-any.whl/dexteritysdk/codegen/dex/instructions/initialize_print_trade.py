# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from dexteritysdk.codegen.dex.types import InitializePrintTradeParams
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


# LOCK-BEGIN[ix_cls(initialize_print_trade)]: DON'T MODIFY
@dataclass
class InitializePrintTradeIx:
    program_id: PublicKey

    # account metas
    user: AccountMeta
    creator: AccountMeta
    counterparty: AccountMeta
    operator: AccountMeta
    market_product_group: AccountMeta
    product: AccountMeta
    print_trade: AccountMeta
    system_program: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    params: InitializePrintTradeParams

    def to_instruction(self):
        keys = []
        keys.append(self.user)
        keys.append(self.creator)
        keys.append(self.counterparty)
        keys.append(self.operator)
        keys.append(self.market_product_group)
        keys.append(self.product)
        keys.append(self.print_trade)
        keys.append(self.system_program)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.INITIALIZE_PRINT_TRADE))
        buffer.write(BYTES_CATALOG.pack(InitializePrintTradeParams, self.params))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(initialize_print_trade)]: DON'T MODIFY
def initialize_print_trade(
    user: Union[str, PublicKey, AccountMeta],
    creator: Union[str, PublicKey, AccountMeta],
    counterparty: Union[str, PublicKey, AccountMeta],
    operator: Union[str, PublicKey, AccountMeta],
    market_product_group: Union[str, PublicKey, AccountMeta],
    product: Union[str, PublicKey, AccountMeta],
    print_trade: Union[str, PublicKey, AccountMeta],
    params: InitializePrintTradeParams,
    system_program: Union[str, PublicKey, AccountMeta] = PublicKey("11111111111111111111111111111111"),
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PublicKey("FUfpR31LmcP1VSbz5zDaM7nxnH55iBHkpwusgrnhaFjL")

    if isinstance(user, (str, PublicKey)):
        user = to_account_meta(
            user,
            is_signer=True,
            is_writable=True,
        )
    if isinstance(creator, (str, PublicKey)):
        creator = to_account_meta(
            creator,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(counterparty, (str, PublicKey)):
        counterparty = to_account_meta(
            counterparty,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(operator, (str, PublicKey)):
        operator = to_account_meta(
            operator,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(market_product_group, (str, PublicKey)):
        market_product_group = to_account_meta(
            market_product_group,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(product, (str, PublicKey)):
        product = to_account_meta(
            product,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(print_trade, (str, PublicKey)):
        print_trade = to_account_meta(
            print_trade,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(system_program, (str, PublicKey)):
        system_program = to_account_meta(
            system_program,
            is_signer=False,
            is_writable=False,
        )

    return InitializePrintTradeIx(
        program_id=program_id,
        user=user,
        creator=creator,
        counterparty=counterparty,
        operator=operator,
        market_product_group=market_product_group,
        product=product,
        print_trade=print_trade,
        system_program=system_program,
        remaining_accounts=remaining_accounts,
        params=params,
    ).to_instruction()

# LOCK-END
