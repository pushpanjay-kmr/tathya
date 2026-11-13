"""EODHD (eodhd.com) as a PriceProvider. See docs/07-data-sources.md for the
terms-of-use check: a Non-Professional (personal, non-commercial) user may
store and analyze the data locally, just not share or resell it.

We're on the free tier (20 calls/day), so every raw response is cached to
disk under data/raw/eodhd/ and reused on later runs — see
_cached_get. That also makes the provider idempotent for a given request,
as the interface in providers/base.py requires.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import requests

from tathya_pipeline.config import DATA_RAW_DIR, eodhd_api_key, load_watchlist

API_BASE = "https://eodhd.com/api"
CACHE_DIR = DATA_RAW_DIR / "eodhd"


class EodhdProvider:
    """Implements PriceProvider against EODHD's per-symbol endpoints.

    index_levels and corporate_actions are not implemented yet — nothing
    in the pipeline calls them so far (see tathya_pipeline/ingest).
    """

    id = "eodhd"

    def __init__(self, exchange: str = "NSE") -> None:
        self._api_key = eodhd_api_key()
        self._watchlist = load_watchlist()
        self.exchange = exchange
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _cached_get(self, cache_key: str, path: str, params: dict) -> list[dict]:
        """GET path with params, using a cached response for cache_key if one exists."""
        cache_file = CACHE_DIR / f"{cache_key}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())

        response = requests.get(
            f"{API_BASE}/{path}",
            params={**params, "api_token": self._api_key, "fmt": "json"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        cache_file.write_text(json.dumps(data))
        return data

    def symbol_master(self, symbols: list[str]) -> pd.DataFrame:
        """Code, Name and Isin for the given symbols on self.exchange (one cheap bulk call)."""
        key = f"master-{self.exchange}-" + "-".join(sorted(symbols))
        rows = self._cached_get(
            key, f"exchange-symbol-list/{self.exchange}", {"symbols": ",".join(symbols)}
        )
        return pd.DataFrame(rows)

    def daily_prices(self, as_of: date) -> pd.DataFrame:
        """EOD prices for as_of, for every symbol in the watchlist.

        Pulls a multi-year range per symbol (one API call each) rather than
        one call per day, and caches it, so repeated runs for different
        as_of dates don't re-spend quota once a symbol's range is cached.
        """
        symbols = self._watchlist
        if not symbols:
            return pd.DataFrame()

        master = self.symbol_master(symbols)
        isin_by_symbol = dict(zip(master["Code"], master["Isin"]))

        frames = []
        for symbol in symbols:
            key = f"eod-{self.exchange}-{symbol}"
            rows = self._cached_get(
                key,
                f"eod/{symbol}.{self.exchange}",
                {"from": "2023-01-01", "to": as_of.isoformat()},
            )
            df = pd.DataFrame(rows)
            if df.empty:
                continue
            df["symbol"] = symbol
            df["isin"] = isin_by_symbol.get(symbol)
            frames.append(df)

        if not frames:
            return pd.DataFrame()

        all_history = pd.concat(frames, ignore_index=True)
        today = all_history[all_history["date"] == as_of.isoformat()].copy()
        today = today.rename(
            columns={
                "adjusted_close": "adj_close",
                "date": "trade_date",
            }
        )
        today["source"] = self.id
        return today[
            ["isin", "symbol", "trade_date", "open", "high", "low", "close", "adj_close", "volume", "source"]
        ]

    def index_levels(self, as_of: date) -> pd.DataFrame:
        raise NotImplementedError("EodhdProvider.index_levels: not wired in yet")

    def corporate_actions(self, since: date) -> pd.DataFrame:
        raise NotImplementedError("EodhdProvider.corporate_actions: not wired in yet")
