# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from dexteritysdk.codegen.dex.types import SignPrintTradeParams
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


# LOCK-BEGIN[ix_cls(sign_print_trade)]: DON'T MODIFY
@dataclass
class SignPrintTradeIx:
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
    fee_model_program: AccountMeta
    fee_model_configuration_acct: AccountMeta
    fee_output_register: AccountMeta
    risk_engine_program: AccountMeta
    risk_model_configuration_acct: AccountMeta
    risk_output_register: AccountMeta
    risk_and_fee_signer: AccountMeta
    creator_trader_fee_state_acct: AccountMeta
    creator_trader_risk_state_acct: AccountMeta
    counterparty_trader_fee_state_acct: AccountMeta
    counterparty_trader_risk_state_acct: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    params: SignPrintTradeParams

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
        keys.append(self.fee_model_program)
        keys.append(self.fee_model_configuration_acct)
        keys.append(self.fee_output_register)
        keys.append(self.risk_engine_program)
        keys.append(self.risk_model_configuration_acct)
        keys.append(self.risk_output_register)
        keys.append(self.risk_and_fee_signer)
        keys.append(self.creator_trader_fee_state_acct)
        keys.append(self.creator_trader_risk_state_acct)
        keys.append(self.counterparty_trader_fee_state_acct)
        keys.append(self.counterparty_trader_risk_state_acct)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.SIGN_PRINT_TRADE))
        buffer.write(BYTES_CATALOG.pack(SignPrintTradeParams, self.params))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(sign_print_trade)]: DON'T MODIFY
def sign_print_trade(
    user: Union[str, PublicKey, AccountMeta],
    creator: Union[str, PublicKey, AccountMeta],
    counterparty: Union[str, PublicKey, AccountMeta],
    operator: Union[str, PublicKey, AccountMeta],
    market_product_group: Union[str, PublicKey, AccountMeta],
    product: Union[str, PublicKey, AccountMeta],
    print_trade: Union[str, PublicKey, AccountMeta],
    fee_model_program: Union[str, PublicKey, AccountMeta],
    fee_model_configuration_acct: Union[str, PublicKey, AccountMeta],
    fee_output_register: Union[str, PublicKey, AccountMeta],
    risk_engine_program: Union[str, PublicKey, AccountMeta],
    risk_model_configuration_acct: Union[str, PublicKey, AccountMeta],
    risk_output_register: Union[str, PublicKey, AccountMeta],
    risk_and_fee_signer: Union[str, PublicKey, AccountMeta],
    creator_trader_fee_state_acct: Union[str, PublicKey, AccountMeta],
    creator_trader_risk_state_acct: Union[str, PublicKey, AccountMeta],
    counterparty_trader_fee_state_acct: Union[str, PublicKey, AccountMeta],
    counterparty_trader_risk_state_acct: Union[str, PublicKey, AccountMeta],
    params: SignPrintTradeParams,
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
            is_writable=True,
        )
    if isinstance(counterparty, (str, PublicKey)):
        counterparty = to_account_meta(
            counterparty,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(operator, (str, PublicKey)):
        operator = to_account_meta(
            operator,
            is_signer=False,
            is_writable=True,
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
    if isinstance(fee_model_program, (str, PublicKey)):
        fee_model_program = to_account_meta(
            fee_model_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(fee_model_configuration_acct, (str, PublicKey)):
        fee_model_configuration_acct = to_account_meta(
            fee_model_configuration_acct,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(fee_output_register, (str, PublicKey)):
        fee_output_register = to_account_meta(
            fee_output_register,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(risk_engine_program, (str, PublicKey)):
        risk_engine_program = to_account_meta(
            risk_engine_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(risk_model_configuration_acct, (str, PublicKey)):
        risk_model_configuration_acct = to_account_meta(
            risk_model_configuration_acct,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(risk_output_register, (str, PublicKey)):
        risk_output_register = to_account_meta(
            risk_output_register,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(risk_and_fee_signer, (str, PublicKey)):
        risk_and_fee_signer = to_account_meta(
            risk_and_fee_signer,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(creator_trader_fee_state_acct, (str, PublicKey)):
        creator_trader_fee_state_acct = to_account_meta(
            creator_trader_fee_state_acct,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(creator_trader_risk_state_acct, (str, PublicKey)):
        creator_trader_risk_state_acct = to_account_meta(
            creator_trader_risk_state_acct,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(counterparty_trader_fee_state_acct, (str, PublicKey)):
        counterparty_trader_fee_state_acct = to_account_meta(
            counterparty_trader_fee_state_acct,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(counterparty_trader_risk_state_acct, (str, PublicKey)):
        counterparty_trader_risk_state_acct = to_account_meta(
            counterparty_trader_risk_state_acct,
            is_signer=False,
            is_writable=True,
        )

    return SignPrintTradeIx(
        program_id=program_id,
        user=user,
        creator=creator,
        counterparty=counterparty,
        operator=operator,
        market_product_group=market_product_group,
        product=product,
        print_trade=print_trade,
        system_program=system_program,
        fee_model_program=fee_model_program,
        fee_model_configuration_acct=fee_model_configuration_acct,
        fee_output_register=fee_output_register,
        risk_engine_program=risk_engine_program,
        risk_model_configuration_acct=risk_model_configuration_acct,
        risk_output_register=risk_output_register,
        risk_and_fee_signer=risk_and_fee_signer,
        creator_trader_fee_state_acct=creator_trader_fee_state_acct,
        creator_trader_risk_state_acct=creator_trader_risk_state_acct,
        counterparty_trader_fee_state_acct=counterparty_trader_fee_state_acct,
        counterparty_trader_risk_state_acct=counterparty_trader_risk_state_acct,
        remaining_accounts=remaining_accounts,
        params=params,
    ).to_instruction()

# LOCK-END
