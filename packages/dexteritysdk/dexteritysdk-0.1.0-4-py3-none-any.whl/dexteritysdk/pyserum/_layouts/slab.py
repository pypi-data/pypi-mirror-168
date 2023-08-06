"""Slab data stucture that is used to represent Order book."""
from __future__ import annotations

from enum import IntEnum

from construct import Bytes, Int8ul, Int32ul, Int64ul, Padding
from construct import Struct as cStruct
from construct import Switch
from borsh_construct import CStruct, I8, I32, I64

KEY = Bytes(16)

SLAB_HEADER_LAYOUT = CStruct(
    "tag" / I8,
    "bump_index" / I64,
    "free_list_length" / I64,
    "free_list_head" / I32,
    "callback_memory_offset" / I64,
    "callback_free_list_len" / I64,
    "callback_free_list_head" / I64,
    "callback_bump_index" / I64,
    "root" / I32,
    "leaf_count" / I64,
    "market" / Bytes(32),
)


class SlabType(IntEnum):
    UNINITIALIZED = 0
    MARKET = 1
    EVENT_QUEUE = 2
    BIDS = 3
    ASKS = 4


class NodeType(IntEnum):
    UNINITIALIZED = 0
    INNER_NODE = 1
    LEAF_NODE = 2
    FREE_NODE = 3
    LAST_FREE_NODE = 4


# Different node types, we pad it all to size of 40 bytes.
UNINITIALIZED = cStruct(Padding(32))
INNER_NODE = cStruct("prefix_len" / Int64ul, "key" / KEY, "children" / Int32ul[2])
LEAF_NODE = cStruct(
    "key" / KEY,
    "callback" / Int64ul,
    "quantity" / Int64ul,
)
FREE_NODE = cStruct("next" / Int32ul, Padding(28))
LAST_FREE_NODE = cStruct(Padding(32))

SLAB_NODE_LAYOUT = cStruct(
    "tag" / Int8ul,
    Padding(7),
    "node"
    / Switch(
        lambda this: this.tag,
        {
            NodeType.UNINITIALIZED: UNINITIALIZED,
            NodeType.INNER_NODE: INNER_NODE,
            NodeType.LEAF_NODE: LEAF_NODE,
            NodeType.FREE_NODE: FREE_NODE,
            NodeType.LAST_FREE_NODE: LAST_FREE_NODE,
        },
    ),
)

SLAB_LAYOUT = cStruct("header" / SLAB_HEADER_LAYOUT, Padding(7),
                      "nodes" / SLAB_NODE_LAYOUT[lambda this: this.header.bump_index])
