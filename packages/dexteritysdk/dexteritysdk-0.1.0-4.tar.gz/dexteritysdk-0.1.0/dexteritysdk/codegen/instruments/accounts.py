# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.instruments.types.derivative_metadata import DerivativeMetadata
from dexteritysdk.solmate.anchor import AccountDiscriminant
from podite import (
    Enum,
    U64,
    pod,
)

# LOCK-END


# LOCK-BEGIN[accounts]: DON'T MODIFY
@pod
class Accounts(Enum[U64]):
    DERIVATIVE_METADATA = AccountDiscriminant(field=DerivativeMetadata)
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
