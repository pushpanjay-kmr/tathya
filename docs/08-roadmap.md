# 08. Roadmap

Phases are sequential. Each has an exit test: the phase is done when the test passes, not when the tasks are ticked.

## Phase 0. Design (in progress)

- [x] Product and design documents in the repo
- [ ] Home page mockups in both visual directions
- [ ] Choose a direction and record it
- [ ] Mockups: stock page, scanner, screener
- [ ] Confirm tech stack

**Exit test:** the four core screens are mocked up in the chosen direction and approved.

## Phase 1. Foundation

- [ ] Repository scaffold: `apps/web`, `pipeline`, `db`, Docker Compose
- [ ] Database migrations for reference and market-data tables
- [ ] Seed data: industries, indices, cap buckets
- [ ] Price provider for end-of-day data, with validation
- [ ] Backfill at least 2 years of daily prices
- [ ] Design tokens in Tailwind; base components (table, chip, tile, delta)
- [ ] App shell: top bar, search, theme toggle, disclaimer footer

**Exit test:** one command runs the pipeline for a date and the app shell shows the correct "as of" date and a working company search.

## Phase 2. Core screens

- [ ] Indicator computation (moving averages, RSI, MACD, 52-week levels)
- [ ] Market overview: indices, sector indices, breadth, rotation strip, movers
- [ ] Global cap and sector filters, held in the URL
- [ ] Stock page: header, price chart, peers
- [ ] Fundamentals provider and financial tables on the stock page
- [ ] Ratio snapshot

**Exit test:** the home page and any stock page render fully from the database for the latest trading day, in both themes.

## Phase 3. Scanner and screener (MVP complete)

- [ ] Scan engine and the first 20 scans
- [ ] Scan results, entries, exits and daily history
- [ ] Scanner pages and the "firing today" strip on the home page
- [ ] Scans on the stock page
- [ ] Field registry and `screener_snapshot`
- [ ] Formula parser with tests
- [ ] Screener page with columns, sort, saved screens and CSV export
- [ ] Nightly schedule

**Exit test:** the pipeline runs unattended for 5 trading days in a row, and a formula such as `ROCE > 20 AND PEG < 1` returns correct results in under 500 ms.

## Phase 4. Ownership and events

- [ ] Shareholding provider and stock-page section
- [ ] Tracked investors and the smart-money pages
- [ ] Filings ingestion and document storage
- [ ] Results calendar
- [ ] IPO calendar
- [ ] Industry rotation page with group valuation
- [ ] Compare and scatter tools

**Exit test:** a new quarterly shareholding filing shows up as adds and trims on the smart-money page after the next nightly run.

## Phase 5. AI layer

- [ ] Document chunking and embeddings
- [ ] Filing classifier (type, event, priority)
- [ ] Result and concall summaries
- [ ] Guidance extraction and the forward-signals page
- [ ] Ask Tathya with citations
- [ ] Tathya Score with adjustable weights
- [ ] Strategy tools: cyclicals, fast growers, turnarounds
- [ ] Cost tracking and caching

**Exit test:** for 20 sample companies, every Ask Tathya answer cites a real passage, and questions the documents cannot answer are declined.

## Phase 6. Polish and launch review

- [ ] Scan library grown towards 100+
- [ ] Screener fields grown towards 300+
- [ ] Scan hit-rate statistics
- [ ] Performance pass
- [ ] Licensed data feed (see [Data sources](07-data-sources.md))
- [ ] Compliance review (see [Compliance and disclaimer](09-compliance-and-disclaimer.md))
- [ ] Forward estimates

**Exit test:** only relevant if the project goes beyond personal use. Both the data licence and the compliance review are complete.
