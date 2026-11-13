"""The provider contract. See docs/07-data-sources.md, "Provider interface".

Every data source — free or licensed — is reached through one of these
Protocols. Nothing in the pipeline imports a source-specific library
directly outside of a provider module; swapping a free source for a
licensed one means writing a new provider and changing config/providers.yaml.

Rules for providers (docs/07-data-sources.md):

- Return data in Tathya's schema and units. Source-specific cleaning stays
  inside the provider.
- Identify companies by ISIN.
- Be idempotent for a given date.
- Rate-limit themselves and cache raw responses under data/raw/ (git-ignored).
- Record a provider_fetch row for every call (see tathya_pipeline.run).
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Protocol

import pandas as pd


class PriceProvider(Protocol):
    id: str

    def daily_prices(self, as_of: date) -> pd.DataFrame: ...
    def index_levels(self, as_of: date) -> pd.DataFrame: ...
    def corporate_actions(self, since: date) -> pd.DataFrame: ...


class FundamentalsProvider(Protocol):
    id: str

    def financials(self, isin: str) -> pd.DataFrame: ...


class OwnershipProvider(Protocol):
    id: str

    def shareholding(self, isin: str, quarter_end: date) -> pd.DataFrame: ...


class FilingsProvider(Protocol):
    id: str

    def filings(self, since: datetime) -> pd.DataFrame: ...
    def document(self, filing_id: str) -> bytes: ...
