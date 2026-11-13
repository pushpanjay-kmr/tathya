"""Synthetic OHLCV for a handful of real companies — NOT a real data source.

Approved as a time-boxed, scoped exception to this repo's "no fake data in
the app" rule, purely to unblock app development while no compliant Indian
price source is wired in (see docs/07-data-sources.md and
docs/10-decisions.md #10). Every row this provider produces carries
source = "sample" so it is never mistaken for real data, and it must be
purged before any real use, demo or public version (see TODO.md).

Company names and ISINs below are real, public identifiers (not licensed
data); the prices are a deterministic random walk, not actual market data.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from datetime import date

COMPANIES = [
    {"symbol": "RELIANCE", "isin": "INE002A01018", "name": "Reliance Industries Ltd", "base_price": 2900.0},
    {"symbol": "TCS", "isin": "INE467B01029", "name": "Tata Consultancy Services Ltd", "base_price": 4100.0},
    {"symbol": "HDFCBANK", "isin": "INE040A01034", "name": "HDFC Bank Ltd", "base_price": 1750.0},
    {"symbol": "INFY", "isin": "INE009A01021", "name": "Infosys Ltd", "base_price": 1850.0},
    {"symbol": "ICICIBANK", "isin": "INE090A01021", "name": "ICICI Bank Ltd", "base_price": 1300.0},
]

HISTORY_START = date(2024, 1, 1)


class SampleProvider:
    """Implements PriceProvider with generated, clearly-labelled sample data."""

    id = "sample"

    def symbol_master(self, symbols: list[str]) -> pd.DataFrame:
        rows = [c for c in COMPANIES if c["symbol"] in symbols]
        return pd.DataFrame(rows).rename(columns={"symbol": "Code", "isin": "Isin", "name": "Name"})

    def _walk(self, company: dict, as_of: date) -> pd.DataFrame:
        """A deterministic random walk from HISTORY_START to as_of, business days only."""
        dates = pd.bdate_range(HISTORY_START, as_of)
        rng = np.random.default_rng(seed=abs(hash(company["symbol"])) % (2**32))
        daily_returns = rng.normal(loc=0.0003, scale=0.015, size=len(dates))
        close = company["base_price"] * (1 + daily_returns).cumprod()
        open_ = close * (1 + rng.normal(0, 0.003, size=len(dates)))
        high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.004, size=len(dates))))
        low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.004, size=len(dates))))
        volume = rng.integers(200_000, 5_000_000, size=len(dates))

        return pd.DataFrame(
            {
                "trade_date": dates.strftime("%Y-%m-%d"),
                "open": open_.round(2),
                "high": high.round(2),
                "low": low.round(2),
                "close": close.round(2),
                "adj_close": close.round(2),
                "volume": volume,
            }
        )

    def daily_prices(self, as_of: date) -> pd.DataFrame:
        frames = []
        for company in COMPANIES:
            walk = self._walk(company, as_of)
            row = walk[walk["trade_date"] == as_of.isoformat()].copy()
            if row.empty:
                continue
            row["isin"] = company["isin"]
            row["symbol"] = company["symbol"]
            row["source"] = self.id
            frames.append(row)

        if not frames:
            return pd.DataFrame()

        result = pd.concat(frames, ignore_index=True)
        return result[
            ["isin", "symbol", "trade_date", "open", "high", "low", "close", "adj_close", "volume", "source"]
        ]

    def index_levels(self, as_of: date) -> pd.DataFrame:
        raise NotImplementedError("SampleProvider.index_levels: not wired in yet")

    def corporate_actions(self, since: date) -> pd.DataFrame:
        raise NotImplementedError("SampleProvider.corporate_actions: not wired in yet")
