# 07. Data sources

## Current position

Tathya starts on **free, end-of-day data** for personal use. A licensed market-data feed is deferred and tracked in [TODO.md](../TODO.md). The architecture assumes that swap will happen, so no source is called directly from application code.

> [!NOTE]
> Every source below needs its terms of use read and recorded before it is wired in. That check is a TODO item per source. Nothing here is a statement that a particular use is permitted.

## Provider interface

All data arrives through providers that implement one small contract. Swapping a free source for a licensed one means writing a new provider and changing config.

```python
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
```

Rules for providers:

- Return data in Tathya's schema and units. All source-specific cleaning stays inside the provider.
- Identify companies by ISIN.
- Be idempotent for a given date.
- Rate-limit themselves and cache raw responses under `data/raw/` (git-ignored).
- Record a `provider_fetch` row for every call.

Config selects one provider per dataset, with an optional fallback:

```yaml
providers:
  prices:        { primary: exchange_eod, fallback: community_api }
  fundamentals:  { primary: filings_derived }
  ownership:     { primary: exchange_shareholding }
  filings:       { primary: exchange_announcements }
```

## Datasets and candidate sources

| Dataset | Needed for | Free candidate (now) | Licensed option (later) |
|---|---|---|---|
| Daily prices and volume | Everything | End-of-day files published by the exchanges | Exchange-authorised data vendor |
| Index levels | Market overview | Exchange index data files | Same vendor |
| Corporate actions | Adjusted prices | Exchange corporate-action listings | Same vendor |
| Company master and industry mapping | Universe, rotation | Exchange listing files plus a maintained mapping in `db/seed/` | Vendor classification |
| Financial statements | Ratios, screener, growth scans | Results filings in structured (XBRL) form where available | Fundamentals vendor |
| Shareholding pattern | Smart money | Quarterly shareholding filings | Fundamentals vendor |
| Announcements and documents | Filings feed, AI layer | Exchange announcement feeds and attached PDFs | Vendor or direct feed |
| Concall transcripts | Guidance signals, Ask Tathya | Transcripts companies file with the exchanges | Transcript vendor |
| IPO details | IPO calendar | Exchange and regulator issue pages | Vendor |
| Live or delayed intraday prices | Not in scope | None | Licensed feed only |

A community Python library for market data may be used as a development convenience and price fallback. It is unofficial, can break without notice and is not suitable for anything beyond personal use.

## Known limits of the free setup

- **End-of-day only.** The header always shows the "as of" date. No intraday anything.
- **Fundamentals coverage will be uneven.** Deriving statements from filings takes work and small companies will have gaps. The UI shows `–` for missing values and never fills gaps with guesses.
- **History depth is limited** to what can be backfilled from public files.
- **Sources can change format.** The validation step and `provider_fetch` log exist to catch this early.
- **No redistribution.** Data fetched for personal use stays local. It is not committed to the repo, exposed through a public API or shown on a public deployment.

## Data quality checks

| Check | Rule |
|---|---|
| Completeness | Row count for the day within 2% of the previous session |
| Price sanity | Day-on-day move above 40% requires a matching corporate action or is quarantined |
| Continuity | No gaps in trading dates per active company |
| Fundamentals | Balance sheet balances within tolerance; revenue is non-negative |
| Identity | Every row resolves to a known ISIN |

## Licensed feed plan (deferred)

Before any public or multi-user version:

1. Choose a vendor authorised to distribute exchange data, covering prices and fundamentals.
2. Confirm the licence allows display to end users, and at what delay.
3. Implement the vendor as new providers behind the interfaces above.
4. Backfill, reconcile against the free data, then switch config.
5. Remove unofficial sources from the production config.
