"""Step 1-3 of the nightly pipeline: ingest, validate, load.

See docs/05-architecture.md, "Nightly pipeline". Each dataset's provider is
looked up from config/providers.yaml; a provider that errors is skipped so
the run continues, and every attempt is logged via tathya_pipeline.run.record_fetch.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from tathya_pipeline.config import load_provider_config
from tathya_pipeline.providers.registry import ProviderNotRegistered, get_provider
from tathya_pipeline.run import record_fetch


def ingest_prices(session: Session, run_id: int, as_of: date) -> None:
    """Fetch daily prices for as_of via the configured price provider.

    No-op until a price provider is registered (see providers/registry.py)
    and config/providers.yaml names one for the "prices" dataset.
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
    record_fetch(session, run_id, provider=entry.primary, dataset=dataset, as_of_date=as_of, status="ok", row_count=len(prices))
    # TODO: validate (docs/07 "Data quality checks") and upsert into price_daily.
