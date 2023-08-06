# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.dex.types.fractional import Fractional
from dexteritysdk.solmate.dtypes import Usize
from dexteritysdk.utils.aob.state.base import Side
from podite import pod

# LOCK-END


# LOCK-BEGIN[class(InitializePrintTradeParams)]: DON'T MODIFY
@pod
class InitializePrintTradeParams:
    product_index: Usize
    size: Fractional
    price: Fractional
    side: Side
    operator_creator_fee_proportion: Fractional
    operator_counterparty_fee_proportion: Fractional
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
