"""Step 1-3 of the nightly pipeline: ingest, validate, load.

See docs/05-architecture.md, "Nightly pipeline". Each dataset's provider is
looked up from config/providers.yaml; a provider that errors is skipped so
the run continues, and every attempt is logged via tathya_pipeline.run.record_fetch.
"""

from __future__ import annotations

from datetime import date

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from tathya_pipeline.config import load_provider_config
from tathya_pipeline.providers.registry import ProviderNotRegistered, get_provider
from tathya_pipeline.run import record_fetch


def validate_prices(prices: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Step 2: basic quality checks from docs/07-data-sources.md.

    Returns (rows that passed, problems found). A full pass also checks
    completeness against the previous session and price-sanity on day-on-day
    moves (docs/07) — not meaningful yet with a five-symbol watchlist and no
    prior session loaded, so both are left as a TODO for when the universe
    is bigger.
    """
    errors: list[str] = []
    clean = prices.copy()

    missing_isin = clean["isin"].isna()
    if missing_isin.any():
        errors.append(f"{missing_isin.sum()} row(s) with no ISIN (not in the exchange symbol master)")
        clean = clean[~missing_isin]

    bad_range = clean["high"] < clean["low"]
    if bad_range.any():
        errors.append(f"{bad_range.sum()} row(s) with high < low")
        clean = clean[~bad_range]

    return clean, errors


def load_company_master(session: Session, master: pd.DataFrame) -> None:
    """Step 3: upsert the company master from a provider's symbol list.

    Only isin, nse_symbol and name are known from EODHD's exchange-symbol-list
    endpoint; industry_id is filled later by the seed step (docs/08-roadmap.md).
    """
    for row in master.itertuples():
        if not row.Isin:
            continue
        session.execute(
            text(
                "INSERT INTO company (isin, nse_symbol, name) "
                "VALUES (:isin, :symbol, :name) "
                "ON CONFLICT (isin) DO UPDATE SET nse_symbol = EXCLUDED.nse_symbol, name = EXCLUDED.name"
            ),
            {"isin": row.Isin, "symbol": row.Code, "name": row.Name},
        )


def load_prices(session: Session, prices: pd.DataFrame) -> int:
    """Step 3: upsert validated price rows into price_daily, keyed by ISIN -> company_id."""
    loaded = 0
    for row in prices.itertuples():
        result = session.execute(
            text("SELECT id FROM company WHERE isin = :isin"), {"isin": row.isin}
        )
        company_id = result.scalar_one_or_none()
        if company_id is None:
            continue
        session.execute(
            text(
                "INSERT INTO price_daily (company_id, date, open, high, low, close, adj_close, volume, source) "
                "VALUES (:company_id, :date, :open, :high, :low, :close, :adj_close, :volume, :source) "
                "ON CONFLICT (company_id, date) DO UPDATE SET "
                "open = EXCLUDED.open, high = EXCLUDED.high, low = EXCLUDED.low, "
                "close = EXCLUDED.close, adj_close = EXCLUDED.adj_close, "
                "volume = EXCLUDED.volume, source = EXCLUDED.source"
            ),
            {
                "company_id": company_id,
                "date": row.trade_date,
                "open": row.open,
                "high": row.high,
                "low": row.low,
                "close": row.close,
                "adj_close": row.adj_close,
                "volume": row.volume,
                "source": row.source,
            },
        )
        loaded += 1
    return loaded


def ingest_prices(session: Session, run_id: int, as_of: date) -> None:
    """Fetch, validate and load daily prices for as_of via the configured price provider.

    Skipped (not an error) if no provider is configured — see config/providers.yaml.
    """
    config = load_provider_config()
    dataset = "prices"
    entry = config.get(dataset)
    if entry is None:
        record_fetch(session, run_id, provider="none", dataset=dataset, as_of_date=as_of, status="skipped", error="no provider configured")
        return

    try:
        provider = get_provider(entry.primary)
    except ProviderNotRegistered as exc:
        record_fetch(session, run_id, provider=entry.primary, dataset=dataset, as_of_date=as_of, status="skipped", error=str(exc))
        return

    prices = provider.daily_prices(as_of)
    if prices.empty:
        record_fetch(session, run_id, provider=entry.primary, dataset=dataset, as_of_date=as_of, status="ok", row_count=0)
        return

    clean, problems = validate_prices(prices)

    if hasattr(provider, "symbol_master"):
        load_company_master(session, provider.symbol_master(list(clean["symbol"])))

    loaded = load_prices(session, clean)

    record_fetch(
        session,
        run_id,
        provider=entry.primary,
        dataset=dataset,
        as_of_date=as_of,
        status="ok",
        row_count=loaded,
        error="; ".join(problems) or None,
    )
