from __future__ import annotations

from typing import Iterable, List, Union

from ._layouts.slab import SlabType
from .serum_types import OrderInfo, Order

from .enums import Side
from ._internal.slab import Slab, SlabInnerNode, SlabLeafNode


class OrderBook:
    """Represents an order book."""

    _is_bids: bool
    _slab: Slab

    def __init__(self, slab: Slab, decimals: int) -> None:
        self._is_bids = (slab._header.tag == SlabType.BIDS)
        print(f"Slab tag {slab._header.tag}")
        self._slab = slab
        self._decimals = decimals

    @staticmethod
    def __get_price_from_slab(node: Union[SlabInnerNode, SlabLeafNode]) -> int:
        """Get price from a slab node key.

        The key is constructed as the (price << 64) + (seq_no if ask_order else !seq_no).
        """
        return node.key >> 96

    @staticmethod
    def from_bytes(buffer: bytes, decimals: int) -> OrderBook:
        """Decode the given buffer into an order book."""
        slab = Slab.from_bytes(buffer[:])
        return OrderBook(slab, decimals)

    def get_l2(self, depth: int) -> List[OrderInfo]:
        """Get the Level 2 market information."""
        descending = self._is_bids
        # The first element of the inner list is price, the second is quantity.
        levels: List[List[int]] = []
        for node in self._slab.items(descending):
            price = self.__get_price_from_slab(node)
            if len(levels) > 0 and levels[len(levels) - 1][0] == price:
                levels[len(levels) - 1][1] += node.quantity
            elif len(levels) == depth:
                break
            else:
                levels.append([price, node.quantity])
        return [
            OrderInfo(
                price=price_lots,
                size=size_lots / (10 ** self._decimals),
            )
            for price_lots, size_lots in levels
        ]

    def __iter__(self) -> Iterable[Order]:
        return self.orders()

    def orders(self) -> Iterable[Order]:
        for node in self._slab.items():
            price = self.__get_price_from_slab(node)

            yield Order(
                order_id=node.key,
                client_id=node.client_order_id,
                info=OrderInfo(
                    price=price,
                    size=node.quantity / (10 ** self._decimals),
                ),
                side=Side.BUY if self._is_bids else Side.SELL,
            )
