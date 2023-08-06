# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.dex.types.fractional import Fractional
from dexteritysdk.codegen.dex.types.product_metadata import ProductMetadata
from dexteritysdk.codegen.dex.types.product_status import ProductStatus
from dexteritysdk.solmate.dtypes import Usize
from podite import (
    FixedLenArray,
    U64,
    pod,
)

# LOCK-END


# LOCK-BEGIN[class(Outright)]: DON'T MODIFY
@pod
class Outright:
    metadata: "ProductMetadata"
    num_queue_events: Usize
    product_status: "ProductStatus"
    dust: "Fractional"
    cum_funding_per_share: "Fractional"
    cum_social_loss_per_share: "Fractional"
    open_long_interest: "Fractional"
    open_short_interest: "Fractional"
    padding: FixedLenArray[U64, 14]
    # LOCK-END

    def is_expired(self) -> bool:
        return product_status == ProductStatus.EXPIRED

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
