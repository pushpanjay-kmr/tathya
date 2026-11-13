# 10. Decision log

Short records of decisions and their reasons. Newest last.

| # | Date | Decision | Reason | Status |
|---|---|---|---|---|
| 1 | 2026-11-13 | Build an analysis tool, not a trading app | Scope is research: no broker integration or order placement | Accepted |
| 2 | 2026-11-13 | Own brand and design under the name Tathya | Independent product; no copying of any other product's branding, text or visual design | Accepted |
| 3 | 2026-11-13 | Personal-use scope for now | Lets regulatory and data-licensing questions be deferred; both become gates before any public version | Accepted |
| 4 | 2026-11-13 | Free end-of-day data first, licensed feed later | No budget commitment during the build; all sources sit behind a provider interface so the swap is contained | Accepted |
| 5 | 2026-11-13 | Show a "not investment advice" disclaimer on every page | Good practice even for personal use | Accepted |
| 6 | 2026-11-13 | Next.js, PostgreSQL and a Python nightly pipeline | Read-heavy app over daily data: precompute in batch, serve thin | Accepted |
| 8 | 2026-11-13 | Fonts are bundled from npm packages, not fetched from Google at build time | Builds work offline and do not depend on a third-party service | Accepted |
| 7 | 2026-11-13 | Ledger (light) is the default visual direction; Terminal is the dark theme | Chosen after home page mockups in both directions: Ledger reads as the more professional, premium research product | Accepted |

## Open questions

- Local only, or a private hosted deployment?
- Which LLM provider and monthly budget for the AI layer?
- Consolidated or standalone financials as the default basis?
- Which licence for the repository, if it stays public?
