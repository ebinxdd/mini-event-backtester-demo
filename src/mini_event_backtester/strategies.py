from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from .models import Bar, Order, Position


class Strategy:
    def on_bar(self, bar: Bar, position: Position) -> Order | None:
        raise NotImplementedError


@dataclass
class MovingAverageCrossStrategy(Strategy):
    short_window: int = 8
    long_window: int = 24
    trade_quantity: float = 1.0
    _short_prices: deque[float] = field(default_factory=deque, init=False)
    _long_prices: deque[float] = field(default_factory=deque, init=False)
    _last_signal: str | None = field(default=None, init=False)

    def on_bar(self, bar: Bar, position: Position) -> Order | None:
        self._short_prices.append(bar.close)
        self._long_prices.append(bar.close)

        if len(self._short_prices) > self.short_window:
            self._short_prices.popleft()
        if len(self._long_prices) > self.long_window:
            self._long_prices.popleft()

        if len(self._long_prices) < self.long_window:
            return None

        short_avg = sum(self._short_prices) / len(self._short_prices)
        long_avg = sum(self._long_prices) / len(self._long_prices)
        signal = "long" if short_avg > long_avg else "flat"

        if signal == self._last_signal:
            return None

        self._last_signal = signal

        if signal == "long" and not position.is_open:
            return Order(side="buy", quantity=self.trade_quantity)
        if signal == "flat" and position.is_open:
            return Order(side="sell", quantity=abs(position.quantity))

        return None

