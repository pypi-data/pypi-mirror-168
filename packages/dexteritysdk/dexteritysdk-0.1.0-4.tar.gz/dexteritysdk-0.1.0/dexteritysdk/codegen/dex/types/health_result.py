# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.dex.types.health_info import HealthInfo
from dexteritysdk.codegen.dex.types.liquidation_info import LiquidationInfo
from podite import (
    AutoTagType,
    Enum,
    Option,
    Variant,
    named_fields,
    pod,
)

# LOCK-END


# LOCK-BEGIN[class(HealthResult)]: DON'T MODIFY
@pod
class HealthResult(Enum[AutoTagType]):
    HEALTH = Variant(field=named_fields(health_info=HealthInfo))
    LIQUIDATION = Variant(field=named_fields(liquidation_info=LiquidationInfo))
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
