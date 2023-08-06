# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.dex.types.capital_limits import CapitalLimits
from dexteritysdk.codegen.dex.types.capital_limits_params import CapitalLimitsParams
from dexteritysdk.codegen.dex.types.market_product_group import MarketProductGroup
from dexteritysdk.codegen.dex.types.print_trade import PrintTrade
from dexteritysdk.codegen.dex.types.product_array import ProductArray
from dexteritysdk.codegen.dex.types.risk_output_register import RiskOutputRegister
from dexteritysdk.codegen.dex.types.trader_risk_group import TraderRiskGroup
from dexteritysdk.solmate.anchor import AccountDiscriminant
from podite import (
    Enum,
    U64,
    pod,
)

# LOCK-END

from podite import AutoTagTypeValueManager

# LOCK-BEGIN[accounts]: DON'T MODIFY
@pod
class Accounts(Enum[U64]):
    CAPITAL_LIMITS = AccountDiscriminant(field=CapitalLimits)
    MARKET_PRODUCT_GROUP = AccountDiscriminant(field=MarketProductGroup)
    PRODUCT_ARRAY = AccountDiscriminant(field=ProductArray)
    PRINT_TRADE = AccountDiscriminant(field=PrintTrade)
    RISK_OUTPUT_REGISTER = AccountDiscriminant(field=RiskOutputRegister)
    TRADER_RISK_GROUP = AccountDiscriminant(field=TraderRiskGroup)
    CAPITAL_LIMITS_PARAMS = AccountDiscriminant(field=CapitalLimitsParams)
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", format="FORMAT_ZERO_COPY", **kwargs)

    @classmethod
    def _from_bytes_partial(cls, buffer, format="FORMAT_ZERO_COPY", **kwargs):
        # accounts don't have the same size variants, so must manually use zero-copy and
        # set auto tag type.
        # TODO make this api cleaner
        with AutoTagTypeValueManager(U64):
            return super()._inner_from_bytes_partial(buffer, format="FORMAT_ZERO_COPY", **kwargs)
