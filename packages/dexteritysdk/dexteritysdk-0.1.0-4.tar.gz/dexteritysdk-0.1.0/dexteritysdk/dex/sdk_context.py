import base64
from dataclasses import dataclass
from typing import List, Union, Optional

import base58
from solana.rpc import types
from solana.rpc.commitment import Confirmed
from spl.token import instructions as spl_token_instructions

from ..pyserum.orderbook import OrderBook

from solana.rpc.types import TxOpts
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.system_program import SYS_PROGRAM_ID
from solana.transaction import AccountMeta, TransactionInstruction
from solana import system_program

import dexteritysdk.codegen.dex.instructions as dixs
import dexteritysdk.codegen.dex.types as dtys
from dexteritysdk import program_ids as pids, mints
from dexteritysdk.codegen.dex.accounts import Accounts as DexAccounts
from dexteritysdk.codegen.dex.constants import SENTINEL
from dexteritysdk.codegen.dex.types import MarketProductGroup, Product, CancelOrderParams
from dexteritysdk.constant_fees import instructions as fee_ixs
from dexteritysdk.dex import addrs as daddrs
from dexteritysdk.dex.actions import DexOrderSummary
from dexteritysdk.utils import solana as solana_utils
from dexteritysdk.utils.aob import state as aaob_state
from dexteritysdk.codegen.instruments.accounts import Accounts as InstrumentAccounts
from dexteritysdk.utils.solana import Client, Context, AccountParser, explore, fetch_account_details
from dexteritysdk.solmate.utils import to_account_meta


@dataclass
class SDKOrder:
    order_id: int
    product: "SDKProduct"
    side: aaob_state.Side
    price: float
    qty: float

    @staticmethod
    def from_pyserum_orderbook(order_book: OrderBook, product: "SDKProduct", bids: bool) -> List["SDKOrder"]:
        return [
            SDKOrder(
                o.order_id,
                product,
                aaob_state.Side.BID if bids else aaob_state.Side.ASK,
                o.info.price,
                o.info.size
            ) for o in order_book.orders()
        ]


@dataclass
class SDKOrderSummary:
    order_id: int
    product: "SDKProduct"
    side: aaob_state.Side
    price: float
    qty: float
    filled_qty: float
    remaining_qty: float

    @staticmethod
    def from_dex_order_summary(sdk: "SDKContext", order_summary: DexOrderSummary, product: "SDKProduct",
                               side: aaob_state.Side, quantity: Union[dtys.Fractional, float],
                               price: Union[dtys.Fractional, float]) -> "SDKOrderSummary":
        if isinstance(quantity, dtys.Fractional):
            quantity = quantity.value
        if isinstance(price, dtys.Fractional):
            price = price.value
        order_id = None if order_summary.posted_order_id == order_summary.posted_order_id.NONE \
            else order_summary.posted_order_id.field
        remaining_qty = order_summary.total_base_qty_posted / (10 ** sdk.decimals)
        filled_qty = quantity - remaining_qty
        return SDKOrderSummary(
            order_id=order_id,
            product=product,
            side=side,
            price=price,
            qty=quantity,
            filled_qty=filled_qty,
            remaining_qty=remaining_qty
        )

@dataclass
class SDKProduct:
    key: PublicKey
    name: str  # max 16 bytes
    orderbook: PublicKey
    bids: PublicKey
    asks: PublicKey
    market_signer: PublicKey
    event_queue: PublicKey
    stale_product: Product  # last time prod was fetched

    def get_orderbook(self, sdk: "SDKContext") -> "SDKOrderBook":
        return SDKOrderBook.from_product(sdk, self)

    def crank_raw(self, sdk: "SDKContext", trader_and_risk_accounts: List[PublicKey], reward_target: PublicKey):
        trader_and_risk_accounts.sort()
        trader_and_risk_accounts = _dedup(trader_and_risk_accounts)
        ix = dixs.consume_orderbook_events(
            aaob_program=sdk.aaob_program,
            market_product_group=sdk.market_product_group,
            product=self.key,
            market_signer=self.market_signer,
            orderbook=self.orderbook,
            event_queue=self.event_queue,
            reward_target=reward_target,
            fee_model_program=sdk.fee_model_program,
            fee_model_configuration_acct=sdk.fee_model_configuration_acct,
            fee_output_register=sdk.fee_output_register,
            risk_and_fee_signer=daddrs.get_risk_signer(sdk.market_product_group),
            params=dtys.ConsumeOrderbookEventsParams(
                20
            ),
            remaining_accounts=[AccountMeta(pk, False, False) for pk in trader_and_risk_accounts]
        )
        solana_utils.send_instructions(ix)


def _dedup(xs):
    if len(xs) < 2:
        return xs
    i = 0
    for acct in xs[1:]:
        if xs[i] != acct:
            i += 1
            xs[i] = acct
    return xs[:i + 1]


@dataclass
class SDKOrderBook:
    product: SDKProduct
    bids: List[SDKOrder]
    asks: List[SDKOrder]

    @staticmethod
    def from_product(sdk: "SDKContext", product: "SDKProduct") -> "SDKOrderBook":
        bids_data = base64.b64decode(explore(product.bids).data[0])
        asks_data = base64.b64decode(explore(product.asks).data[0])

        return SDKOrderBook(
            product=product,
            bids=SDKOrder.from_pyserum_orderbook(
                order_book=OrderBook.from_bytes(bids_data, sdk.decimals),
                product=product,
                bids=True,
            ),
            asks=SDKOrder.from_pyserum_orderbook(
                order_book=OrderBook.from_bytes(asks_data, sdk.decimals),
                product=product,
                bids=False,
            )
        )


@dataclass
class SDKTrader:
    keypair: Keypair
    account: PublicKey
    wallet: PublicKey
    trader_fee_state_acct: PublicKey
    trader_risk_state_acct: PublicKey  # separate pk vs kp to allow **vars(trader) in ixs
    whitelist_token_wallet: PublicKey
    dex_program: PublicKey = None

    @staticmethod
    def connect(
            sdk: "SDKContext",
            account: PublicKey,
            keypair: Keypair,
            wallet: PublicKey,
            trader_risk_state_acct: PublicKey,
            dex_program: PublicKey = None,
    ) -> "SDKTrader":
        trader_fee_state_acct = daddrs.get_trader_fee_state_acct(account, sdk.market_product_group,
                                                                 sdk.fee_model_program)
        trg: dtys.TraderRiskGroup = explore(account).data_obj
        assert trg.market_product_group == sdk.market_product_group
        assert trg.risk_state_account == trader_risk_state_acct
        assert trg.fee_state_account == trader_fee_state_acct
        assert trg.owner == keypair.public_key

        whitelist_token_wallet = spl_token_instructions.get_associated_token_address(keypair.public_key, mints.WHITELIST_TOKEN_MINT)

        return SDKTrader(
            keypair, account, wallet, trader_fee_state_acct, trader_risk_state_acct, whitelist_token_wallet, dex_program)

    def get_trader_risk_group(self) -> dtys.TraderRiskGroup:
        return fetch_account_details(self.account).data_obj

    def deposit(self, sdk: "SDKContext", qty: Union[float, dtys.Fractional]):
        if not isinstance(qty, dtys.Fractional):
            qty = dtys.Fractional(int(qty * (10 ** sdk.decimals)), sdk.decimals)
        ix = dixs.deposit_funds(
            user=self.keypair.public_key,
            user_token_account=self.wallet,
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            market_product_group_vault=sdk.market_product_group_vault,
            capital_limits=sdk.capital_limits,
            whitelist_ata_acct=self.whitelist_token_wallet,
            params=dtys.DepositFundsParams(
                quantity=qty,
            ),
            program_id=self.dex_program,
        )
        return sdk.send_instructions(ix)

    def withdraw(self, sdk: "SDKContext", qty: Union[float, dtys.Fractional]):
        if not isinstance(qty, dtys.Fractional):
            qty = dtys.Fractional(int(qty * sdk.decimals), sdk.decimals)
        ix = dixs.withdraw_funds(
            user=self.keypair.public_key,
            user_token_account=self.wallet,
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            market_product_group_vault=sdk.market_product_group_vault,
            risk_output_register=sdk.risk_output_register,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_signer=sdk.risk_signer,
            capital_limits=sdk.capital_limits,
            risk_state_account=self.trader_risk_state_acct,
            params=dtys.WithdrawFundsParams(
                quantity=qty,
            ),
            program_id=self.dex_program,
        )
        return sdk.send_instructions(ix)

    def place_order(
            self,
            sdk: "SDKContext",
            product: Union[SDKProduct, PublicKey],
            side: aaob_state.Side,
            size: Union[dtys.Fractional, float],
            price: Union[dtys.Fractional, float],
            self_trade_behavior: aaob_state.SelfTradeBehavior = aaob_state.SelfTradeBehavior.DECREMENT_TAKE,
            order_type: dtys.OrderType = dtys.OrderType.LIMIT
    ) -> SDKOrderSummary:
        ix = self._place_order_ix(sdk, product, side, size, price, self_trade_behavior, order_type,
                                  sdk.additional_risk_accts)
        trans_details = sdk.send_instructions(ix, raise_on_error=False)
        if trans_details.error:
            raise ValueError(trans_details.error_from_log)
        else:
            raw_summary = trans_details.emitted_logs["new-order:order-summary"]
            return SDKOrderSummary.from_dex_order_summary(sdk, DexOrderSummary.from_bytes(raw_summary),
                                                          product, side, size, price)

    def _place_order_ix(
            self,
            sdk: "SDKContext",
            product: Union[SDKProduct, PublicKey],
            side: aaob_state.Side,
            size: Union[dtys.Fractional, float],
            price: Union[dtys.Fractional, float],
            self_trade_behavior: aaob_state.SelfTradeBehavior = aaob_state.SelfTradeBehavior.DECREMENT_TAKE,
            order_type: dtys.OrderType = dtys.OrderType.LIMIT,
            risk_accounts: Optional[List[PublicKey]] = None,
    ):
        remaining_accounts = [to_account_meta(ra, is_signer=False, is_writable=True) for ra in risk_accounts]

        ix = dixs.new_order(
            program_id=self.dex_program,
            user=self.keypair.public_key,
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            product=product.key,
            aaob_program=sdk.aaob_program,
            orderbook=product.orderbook,
            market_signer=product.market_signer,
            event_queue=product.event_queue,
            bids=product.bids,
            asks=product.asks,
            fee_model_program=sdk.fee_model_program,
            fee_model_configuration_acct=sdk.fee_model_configuration_acct,
            trader_fee_state_acct=self.trader_fee_state_acct,
            fee_output_register=sdk.fee_output_register,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_output_register=sdk.risk_output_register,
            trader_risk_state_acct=self.trader_risk_state_acct,
            risk_and_fee_signer=sdk.risk_signer,
            params=dtys.NewOrderParams(
                side=side,
                max_base_qty=dtys.Fractional.into(size, product.stale_product.metadata().base_decimals),
                order_type=order_type,
                self_trade_behavior=self_trade_behavior,
                match_limit=10,
                limit_price=dtys.Fractional.into(price, product.stale_product.metadata().base_decimals),
            ),
            remaining_accounts=remaining_accounts,
        )

        return ix

    def cancel(
            self,
            sdk: "SDKContext",
            product: SDKProduct,
            order_id: int,
    ):
        self.cancel_underwater(sdk, product, order_id, self.account)

    def cancel_underwater(
            self,
            sdk: "SDKContext",
            product: SDKProduct,
            order_id: int,
            under_water_trg: PublicKey,
    ):
        ix = self._cancel_ix(sdk, product, order_id, under_water_trg)
        trans_details = sdk.send_instructions(ix, raise_on_error=False)
        if trans_details.error:
            raise ValueError(trans_details.error_from_log)

    def _cancel_ix(
            self,
            sdk: "SDKContext",
            product: SDKProduct,
            order_id: int,
            under_water_trg: PublicKey,
    ):
        ix = dixs.cancel_order(
            user=self.keypair.public_key,
            trader_risk_group=under_water_trg,
            market_product_group=sdk.market_product_group,
            product=product.key,
            aaob_program=sdk.aaob_program,
            orderbook=product.orderbook,
            market_signer=product.market_signer,
            event_queue=product.event_queue,
            bids=product.bids,
            asks=product.asks,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_output_register=sdk.risk_output_register,
            trader_risk_state_acct=self.trader_risk_state_acct,
            risk_signer=sdk.risk_signer,
            params=CancelOrderParams(order_id=order_id),
            system_program=SYS_PROGRAM_ID,
            remaining_accounts=None,
            program_id=self.dex_program,
        )

        return ix

    def replace(
            self,
            sdk: "SDKContext",
            product: Union[SDKProduct, PublicKey],
            order_id: int,
            side: aaob_state.Side,
            size: Union[dtys.Fractional, float],
            price: Union[dtys.Fractional, float],
            self_trade_behavior: aaob_state.SelfTradeBehavior = aaob_state.SelfTradeBehavior.DECREMENT_TAKE,
            order_type: dtys.OrderType = dtys.OrderType.LIMIT
    ) -> DexOrderSummary:
        cancel_ix = self._cancel_ix(sdk, product, order_id, self.account)
        place_ix = self._place_order_ix(sdk, product, side, size, price, self_trade_behavior, order_type,
                                        sdk.additional_risk_accts)

        trans_details = sdk.send_instructions(cancel_ix, place_ix, raise_on_error=False)
        if trans_details.error:
            raise Exception(trans_details.error_from_log)
        else:
            raw_summary = trans_details.emitted_logs["new-order:order-summary"]
            return SDKOrderSummary.from_dex_order_summary(sdk, DexOrderSummary.from_bytes(raw_summary),
                                                          product, side, size, price)

    def cancel_all_orders(
            self,
            sdk: "SDKContext",
            product_indices: List[int]
    ):
        trader_risk_group = self.get_trader_risk_group()
        print("Cancelling all orders")
        for n in product_indices:
            order_ids = []
            ptr = trader_risk_group.open_orders.products[n].head_index
            order = trader_risk_group.open_orders.orders[ptr]
            assert order.prev == SENTINEL
            while ptr != SENTINEL:
                order = trader_risk_group.open_orders.orders[ptr]
                assert order.id != 0
                order_ids.append(order.id)
                ptr = order.next

            if order_ids:
                print(f"Cancelling orders with ids {', '.join([str(o_id) for o_id in order_ids])}")
                # TODO parallelize?
                for order_id in order_ids:
                    self.cancel(sdk, sdk.products[n], order_id)
                    print(f"Cancelled order with id {order_id}")


@dataclass
class SDKContext:
    product_group_name: str  # max 16 chars
    trader_risk_state_account_len: int
    decimals: int
    # cached products, reload if necessary
    products: List[SDKProduct]
    # program_ids
    dex_program: PublicKey
    aaob_program: PublicKey
    risk_engine_program: PublicKey
    instruments_program: PublicKey
    # dummy_oracle_program_id: PublicKey
    fee_model_program: PublicKey
    # accts
    market_product_group: PublicKey
    capital_limits: PublicKey
    payer: Keypair
    market_product_group_vault: PublicKey
    vault_mint: PublicKey
    fee_model_configuration_acct: PublicKey
    risk_model_configuration_acct: PublicKey
    risk_signer: PublicKey
    fee_signer: PublicKey
    risk_output_register: PublicKey
    fee_output_register: PublicKey
    fee_collector: PublicKey
    additional_risk_accts: List[PublicKey]
    tx_opts: TxOpts = None

    @staticmethod
    def connect(client: Client,
                payer: Keypair,
                market_product_group_key: PublicKey,
                trader_risk_state_account_len: int = 0,
                dex_program_id: PublicKey = pids.DEX_PROGRAM_ID,
                aaob_program_id: PublicKey = pids.AOB_PROGRAM_ID,
                risk_engine_program_id: PublicKey = pids.RISK_ENGINE_PROGRAM_ID,
                instruments_program_id: PublicKey = pids.INSTRUMENTS_PROGRAM_ID,
                fee_model_program_id: PublicKey = pids.CONSTANT_FEES_MODEL_PROGRAM_ID,
                raise_on_error: bool = False,
                tx_opts: TxOpts = None,
                **kwargs):
        parser = AccountParser()
        parser.register_parser_from_account_enum(pids.DEX_PROGRAM_ID, DexAccounts)
        parser.register_parser(pids.AOB_PROGRAM_ID, aaob_state.account_parser)
        parser.register_parser_from_account_enum(pids.INSTRUMENTS_PROGRAM_ID, InstrumentAccounts)
        Context.init_globals(
            fee_payer=payer,
            client=client,
            signers=[(payer, "payer")],
            parser=parser,
            raise_on_error=raise_on_error,
        )

        mpg: MarketProductGroup = solana_utils.explore(market_product_group_key).data_obj
        print(f"Connecting to mpg {bytes(mpg.name).strip()}")

        capital_limits_key, _ = PublicKey.find_program_address(
            [b"capital_limits_state", bytes(market_product_group_key)],
            dex_program_id
        )

        s_account, _ = PublicKey.find_program_address(
            [b"s", bytes(market_product_group_key)],
            risk_engine_program_id
        )

        r_account, _ = PublicKey.find_program_address(
            [b"r", bytes(market_product_group_key)],
            risk_engine_program_id
        )

        sdk_context = SDKContext(
            product_group_name=bytes(mpg.name).decode("utf-8").strip(),
            trader_risk_state_account_len=trader_risk_state_account_len,
            decimals=mpg.decimals,
            # cached products reload if necessary
            products=[],
            # program_ids
            dex_program=dex_program_id,
            aaob_program=aaob_program_id,
            risk_engine_program=risk_engine_program_id,
            instruments_program=instruments_program_id,
            # dummy_oracle_program_id=None,
            fee_model_program=fee_model_program_id,
            # accts
            market_product_group=market_product_group_key,
            capital_limits=capital_limits_key,
            payer=payer,
            market_product_group_vault=daddrs.get_market_product_group_vault(market_product_group_key),
            vault_mint=mpg.vault_mint,
            fee_model_configuration_acct=mpg.fee_model_configuration_acct,
            risk_model_configuration_acct=mpg.risk_model_configuration_acct,
            risk_signer=daddrs.get_risk_signer(market_product_group_key),
            fee_signer=daddrs.get_risk_signer(market_product_group_key),
            risk_output_register=mpg.risk_output_register,
            fee_output_register=mpg.fee_output_register,
            fee_collector=mpg.fee_collector,
            additional_risk_accts=[s_account, r_account],
            tx_opts=tx_opts,
        )
        sdk_context.load_products()
        return sdk_context

    def list_trader_risk_groups(self) -> List[PublicKey]:
        account_discriminator_filter = types.MemcmpOpts(
            offset=0,
            bytes=str(base58.b58encode(
                int(DexAccounts.TRADER_RISK_GROUP).to_bytes(8, "little")
            ), 'utf-8')
        )
        mpg_filter = types.MemcmpOpts(
            offset=16,
            bytes=str(self.market_product_group.to_base58(), 'utf-8')
        )
        trader_filter = types.MemcmpOpts(
            offset=48,
            bytes=str(self.payer.public_key.to_base58(), 'utf-8')
        )
        response = Context.get_global_client().get_program_accounts(
            pubkey=self.dex_program,
            commitment=Confirmed,
            encoding="base64",
            data_slice=types.DataSliceOpts(offset=0, length=0),  # we don't need any data
            memcmp_opts=[account_discriminator_filter, mpg_filter, trader_filter]
        )
        trgs = []
        if "result" in response:
            for account in response["result"]:
                trgs.append(PublicKey(account["pubkey"]))
        return trgs

    def load_mpg(self) -> MarketProductGroup:
        return solana_utils.fetch_account_details(self.market_product_group).data_obj

    def load_products(self):
        mpg = self.load_mpg()
        products = []
        for prod in mpg.active_products():
            metadata = prod.metadata()
            orderbook: aaob_state.MarketState = fetch_account_details(metadata.orderbook).data_obj
            sdk_product = SDKProduct(
                metadata.product_key,
                bytes(metadata.name).decode('utf-8').strip(),
                orderbook=metadata.orderbook,
                asks=orderbook.asks,
                bids=orderbook.bids,
                event_queue=orderbook.event_queue,
                market_signer=daddrs.get_market_signer(metadata.product_key),
                stale_product=prod,
            )
            products.append(sdk_product)
        self.products = products

    def send_instructions(self, *ixs: TransactionInstruction, **kwargs):
        if self.tx_opts is not None:
            return solana_utils.send_instructions(*ixs, opts=self.tx_opts, **kwargs)
        else:
            return solana_utils.send_instructions(*ixs, **kwargs)

    def register_trader(self, keypair: Keypair, wallet: PublicKey):
        from solana.system_program import SYS_PROGRAM_ID
        trader_risk_group = Keypair.generate()
        trader_risk_state_acct = Keypair.generate()
        _ident = keypair.public_key.to_base58()[:8]
        Context.add_signers(
            (trader_risk_state_acct, f"{_ident}'s trader_risk_state_acct"),
            (trader_risk_group, f"{_ident}'s trader_risk_group)"),
        )
        trader_fee_state_acct = daddrs.get_trader_fee_state_acct(
            trader_risk_group.public_key,
            self.market_product_group,
            self.fee_model_program)

        fee_ix = fee_ixs.initialize_trader_acct_ix(
            program_id=self.fee_model_program,
            payer=self.payer.public_key,
            fee_model_config_acct=self.fee_model_configuration_acct,
            trader_fee_acct=trader_fee_state_acct,
            market_product_group=self.market_product_group,
            trader_risk_group=trader_risk_group.public_key,
            system_program=SYS_PROGRAM_ID)
        size = dtys.TraderRiskGroup.calc_max_size() + 8
        allocate_trg = system_program.create_account(
            system_program.CreateAccountParams(
                from_pubkey=self.payer.public_key,
                new_account_pubkey=trader_risk_group.public_key,
                lamports=solana_utils.calc_rent(size),
                space=size,
                program_id=self.dex_program,
            )
        )
        trg_init_ix = dixs.initialize_trader_risk_group(
            owner=keypair.public_key,
            trader_risk_group=trader_risk_group.public_key,
            trader_risk_state_acct=trader_risk_state_acct.public_key,
            trader_fee_state_acct=trader_fee_state_acct,
            market_product_group=self.market_product_group,
            risk_signer=self.risk_signer,
            risk_engine_program=self.risk_engine_program,
            program_id=self.dex_program,
            # **vars(self),
        )
        self.send_instructions(fee_ix, allocate_trg, trg_init_ix)
        return SDKTrader.connect(
            self,
            trader_risk_group.public_key,
            keypair,
            wallet,
            trader_risk_state_acct.public_key,
            dex_program=self.dex_program,
        )
