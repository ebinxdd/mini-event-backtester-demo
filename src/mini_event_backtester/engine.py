from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import Bar, Order, Position, Trade
from .strategies import Strategy


@dataclass(frozen=True)
class BacktestResult:
    initial_cash: float
    final_equity: float
    return_pct: float
    trades: list[Trade]
    equity_curve: list[tuple[str, float]]


class BacktestEngine:
    def __init__(self, initial_cash: float = 10_000.0, fee_bps: float = 2.0) -> None:
        self.initial_cash = initial_cash
        self.fee_rate = fee_bps / 10_000.0

    def run(self, bars: Iterable[Bar], strategy: Strategy) -> BacktestResult:
        cash = self.initial_cash
        position = Position()
        trades: list[Trade] = []
        equity_curve: list[tuple[str, float]] = []
        last_price = 0.0

        for bar in bars:
            last_price = bar.close
            order = strategy.on_bar(bar, position)

            if order is not None:
                cash, position, trade = self._execute_order(cash, position, order, bar)
                trades.append(trade)

            equity = cash + position.market_value(bar.close)
            equity_curve.append((bar.timestamp, equity))

        final_equity = cash + position.market_value(last_price)
        return_pct = (final_equity / self.initial_cash - 1.0) * 100.0

        return BacktestResult(
            initial_cash=self.initial_cash,
            final_equity=final_equity,
            return_pct=return_pct,
            trades=trades,
            equity_curve=equity_curve,
        )

    def _execute_order(
        self,
        cash: float,
        position: Position,
        order: Order,
        bar: Bar,
    ) -> tuple[float, Position, Trade]:
        if order.quantity <= 0:
            raise ValueError("Order quantity must be positive.")
        if order.side not in {"buy", "sell"}:
            raise ValueError("Order side must be 'buy' or 'sell'.")

        notional = order.quantity * bar.close
        fee = notional * self.fee_rate

        if order.side == "buy":
            if cash < notional + fee:
                raise ValueError("Insufficient cash for order.")

            new_quantity = position.quantity + order.quantity
            new_average = (
                (position.quantity * position.average_price + notional) / new_quantity
                if new_quantity
                else 0.0
            )
            cash -= notional + fee
            position = Position(quantity=new_quantity, average_price=new_average)
        else:
            sell_quantity = min(order.quantity, abs(position.quantity))
            notional = sell_quantity * bar.close
            fee = notional * self.fee_rate
            cash += notional - fee
            position = Position(quantity=position.quantity - sell_quantity, average_price=position.average_price)
            if abs(position.quantity) < 1e-12:
                position = Position()

        trade = Trade(
            timestamp=bar.timestamp,
            side=order.side,
            quantity=order.quantity,
            price=bar.close,
            fee=fee,
        )
        return cash, position, trade

