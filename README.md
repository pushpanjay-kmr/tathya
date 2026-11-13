# Tathya

> **तथ्य** (*tathya*) means "fact". Tathya is a research and analysis workbench for Indian stocks: market overview, nightly scans, a formula screener, shareholding tracking and AI-assisted reading of company filings.

**Status:** design phase. No application code yet. This repository currently holds the product and design documents that the build will follow.

> [!WARNING]
> Tathya is a personal project for learning and private research. Nothing in it is investment advice or a recommendation to buy or sell any security. See [Compliance and disclaimer](docs/09-compliance-and-disclaimer.md).

## What Tathya does

| Module | Summary |
|---|---|
| Market overview | Indices, sector moves, market breadth and industry rotation, filterable by market-cap bucket |
| Scanner | Ready-made technical and fundamental scans, re-run every night, with entry and exit history |
| Screener | Filter the whole market on fields and formulas such as `ROCE > 20 AND PEG < 1` |
| Stock page | Price chart, financials, ratios, shareholding, filings and scan membership for one company |
| Compare and plot | Side-by-side comparison and scatter plots of any two metrics |
| Smart money | Quarterly shareholding changes for promoters, institutions and well-known investors |
| Results and filings | Results calendar and classified exchange filings |
| IPO calendar | Open, upcoming and recently listed issues |
| Tathya Score | One composite score from quality, growth, governance, valuation and momentum, with adjustable weights |
| Ask Tathya | Question answering over a company's filings and concall transcripts |

Tathya is an analysis tool. It does not place orders or connect to a broker.

## Documentation

| # | Document | What it covers |
|---|---|---|
| 01 | [Product vision](docs/01-product-vision.md) | Why this exists, who it is for, goals and non-goals |
| 02 | [Feature specification](docs/02-feature-spec.md) | Every module, with scope per release |
| 03 | [Information architecture](docs/03-information-architecture.md) | Sitemap, navigation and screen wireframes |
| 04 | [Design system](docs/04-design-system.md) | Brand, colour, type, components and the two visual directions under review |
| 05 | [Architecture](docs/05-architecture.md) | System design, tech stack and repository layout |
| 06 | [Data model](docs/06-data-model.md) | Database schema |
| 07 | [Data sources](docs/07-data-sources.md) | Free sources used now, the provider interface and the licensed-feed plan |
| 08 | [Roadmap](docs/08-roadmap.md) | Phases and exit criteria |
| 09 | [Compliance and disclaimer](docs/09-compliance-and-disclaimer.md) | Personal-use scope and what changes before any public launch |
| 10 | [Decision log](docs/10-decisions.md) | Decisions taken so far and why |

Open items are tracked in [TODO.md](TODO.md).

## Planned tech stack

| Layer | Choice |
|---|---|
| Web app | Next.js (App Router) with TypeScript |
| Styling | Tailwind CSS with design tokens from the design system |
| Charts | Lightweight Charts for price, a general chart library for the rest |
| Database | PostgreSQL |
| Data jobs | Python (pandas) run on a nightly schedule |
| AI | LLM calls behind a single service module, with retrieval over stored filings |

Details and reasoning are in [Architecture](docs/05-architecture.md). The stack is a proposal until Phase 1 starts.

## Roadmap at a glance

| Phase | Outcome | State |
|---|---|---|
| 0. Design | Documents in this repo, visual direction chosen, mockups of core screens | In progress |
| 1. Foundation | Repo scaffold, database, ingestion of end-of-day prices | Not started |
| 2. Core | Market overview, stock page, charts | Not started |
| 3. Scanner and screener | Nightly scan engine, formula screener | Not started |
| 4. Ownership and events | Smart money, results, filings, IPOs | Not started |
| 5. AI layer | Ask Tathya, guidance signals, Tathya Score | Not started |
| 6. Polish | Performance, licensed data, launch review | Not started |

## Data

Tathya currently plans for free, end-of-day data only. There are no live prices. A licensed market-data feed is a tracked TODO and plugs in through the provider interface described in [Data sources](docs/07-data-sources.md).

## Licence

No licence has been chosen yet. Until one is added, all rights are reserved by the author.
