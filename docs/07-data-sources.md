# 07. Data sources

## Current position

Tathya starts on **free, end-of-day data** for personal use. A licensed market-data feed is deferred and tracked in [TODO.md](../TODO.md). The architecture assumes that swap will happen, so no source is called directly from application code.

> [!NOTE]
> Every source below needs its terms of use read and recorded before it is wired in. That check is a TODO item per source. Nothing here is a statement that a particular use is permitted.

## Terms of use checks

Results of the per-source check required before wiring anything in (see `TODO.md`). Each row is what the source's own terms say today; re-check before relying on an old result.

| Source | Checked | Result | Key clause |
|---|---|---|---|
| NSE (`nseindia.com`) | 2026-11-13 | **Blocked.** Do not scrape, do not download and store bhavcopy/EOD files from the public site without a paid licence. | Terms of Use: "User is prohibited to conduct any systematic or automated data collection activities (including scraping, data mining, data extraction and data harvesting)..." and separately bars copying, storing or reproducing any Content "without prior written permission of NSE." NSE's EOD historical data is sold as a subscription product (arranged via marketdata@nse.co.in, under a signed agreement), not offered as a free public download. |
| BSE (`bseindia.com`) | 2026-11-13 | **Blocked for storage/reproduction.** No explicit anti-scraping clause found, but reproduction is restricted. | Disclaimer: "Any reproduction, redistribution or transmission, for consideration or otherwise, of any such information contained on the Website is strictly prohibited..." and the Copyright Notice bars reproducing or transmitting any part of the site's content "without the express written consent of BSE." |

**What this means for the plan:** the "free, end-of-day data" approach in `## Current position` above assumed the exchanges' own sites could be used for personal research without a licence. They cannot — both explicitly restrict scraping and/or storing their data without written permission, with no carve-out for personal or non-commercial use. No provider has been wired in, and none should be, until a compliant source is chosen.

| Source | Checked | Result | Key clause |
|---|---|---|---|
| EODHD (`eodhd.com`) | 2026-11-13 | **Usable.** Explicit personal-use licence. | Terms: "Non-Professional Users are permitted to store, manipulate, and analyze the data for private, non-commercial purposes," prohibited only from sharing account access or reselling/redistributing the data. Covers NSE and BSE (exchange codes confirmed via the Exchanges API; ticker format e.g. `RELIANCE.NSE`). Plans: Free ($0/mo, 20 calls/day, 1 year of EOD history, includes dividends/splits) up to "EOD Historical" ($19.99/mo, 30+ years of history, 100,000 calls/day). Fundamentals (financial statements) need the separate $59.99/mo Fundamentals plan, not needed yet. |

EODHD is the first source found whose terms actually permit what this project does: fetch EOD prices and keep them locally for personal analysis. It has a genuine $0 tier, not just a free trial — useful to validate the pipeline before committing to a paid plan for full history and universe coverage.

**Update, 2026-11-13, after wiring in a real API key:** EODHD does not actually serve NSE or BSE tickers on this account. `GET /api/exchanges-list/` returns 70 exchanges and none of them is India; `GET /api/eod/TCS.NSE` and `GET /api/eod/TCS.BSE` both return `404 Ticker Not Found`, while the same call for `AAPL.US` works (200, real data) — so the key itself is fine, India specifically isn't included. EODHD's public website has marketing pages for individual NSE tickers (e.g. `eodhd.com/financial-summary/TCS.NSE`), which is what made it look covered; that's not the same as the API serving it on this plan. Not yet confirmed whether India needs a paid plan, a separate add-on, or isn't offered at all — worth asking EODHD support directly. Terms-of-use verdict above still stands for whatever EODHD does cover; it's just not usable for Indian equities until India access is confirmed one way or another.

**Pipeline validated anyway, 2026-11-13:** with no India source wired in yet, the ingest → validate → load path (`tathya_pipeline.providers.eodhd`, `tathya_pipeline.ingest`) was proven end to end against EODHD's confirmed-working US coverage (AAPL, MSFT, GOOGL) — real, licensed data under EODHD's personal-use terms, loaded into `company`/`price_daily`, verified in the database, then truncated. `nse_symbol` specifically means NSE-listed, so no non-Indian rows were left in place; this was a one-off code check, not a seed. A quick pass over other vendors (Alpha Vantage, Finnhub, marketstack, Twelve Data) turned up nothing with both confirmed India coverage and a clear personal-use free/cheap tier — Alpha Vantage dropped NSE support years ago, Finnhub's India coverage is unconfirmed, marketstack doesn't list India, Twelve Data wants a custom quote for non-US redistribution. TrueData is an authorised NSE/BSE/MCX vendor but looks broker-grade/commercial, not checked further. **Open:** either ask EODHD support whether India is available on a paid plan, or evaluate TrueData or another vendor properly.

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
