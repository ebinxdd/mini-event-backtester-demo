from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Bar:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class Order:
    side: str
    quantity: float


@dataclass
class Position:
    quantity: float = 0.0
    average_price: float = 0.0

    @property
    def is_open(self) -> bool:
        return self.quantity != 0.0

    def market_value(self, price: float) -> float:
        return self.quantity * price


@dataclass(frozen=True)
class Trade:
    timestamp: str
    side: str
    quantity: float
    price: float
    fee: float

