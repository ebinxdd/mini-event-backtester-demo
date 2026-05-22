# Mini Event Backtester Demo

This is a sanitized public demo of an event-driven backtesting workflow.

The real production projects are private because they contain proprietary strategy logic,
research notes, execution rules, prompts, datasets, model artifacts, and security-sensitive
configuration. This repository intentionally uses synthetic data and a simple educational
strategy so it can be shared publicly without exposing private edge.

## What This Shows

- Event-driven candle iteration
- Strategy interface with `on_bar`
- Position and cash accounting
- Trade log generation
- Basic performance summary
- A runnable synthetic example

## What Is Not Included

- Real trading strategies
- Real exchange adapters
- Private configuration
- Market datasets
- ML models
- Production execution code
- API keys or credentials

## Quick Start

```bash
python examples/run_synthetic_backtest.py
```

Expected output:

```text
Final equity: ...
Return: ...
Trades: ...
```

