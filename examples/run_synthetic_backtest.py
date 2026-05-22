from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mini_event_backtester import Bar, BacktestEngine, MovingAverageCrossStrategy


def synthetic_bars(count: int = 240, seed: int = 7) -> list[Bar]:
    rng = random.Random(seed)
    price = 100.0
    bars: list[Bar] = []

    for i in range(count):
        trend = math.sin(i / 18.0) * 0.25
        noise = rng.uniform(-0.55, 0.55)
        previous = price
        price = max(1.0, price + trend + noise)
        high = max(previous, price) + rng.uniform(0.0, 0.35)
        low = min(previous, price) - rng.uniform(0.0, 0.35)

        bars.append(
            Bar(
                timestamp=f"2026-01-01T{i:04d}",
                open=previous,
                high=high,
                low=low,
                close=price,
                volume=1_000.0 + rng.uniform(-120.0, 120.0),
            )
        )

    return bars


def main() -> None:
    engine = BacktestEngine(initial_cash=10_000.0, fee_bps=2.0)
    strategy = MovingAverageCrossStrategy(short_window=8, long_window=24, trade_quantity=10.0)
    result = engine.run(synthetic_bars(), strategy)

    print(f"Final equity: {result.final_equity:.2f}")
    print(f"Return: {result.return_pct:.2f}%")
    print(f"Trades: {len(result.trades)}")


if __name__ == "__main__":
    main()

