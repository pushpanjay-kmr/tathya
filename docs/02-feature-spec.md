# 02. Feature specification

Each module lists what it does, what data it needs and which release it lands in. Release tags:

- **MVP**: Phases 1 to 3 of the [roadmap](08-roadmap.md)
- **V1**: Phases 4 and 5
- **Later**: after V1, or blocked on licensed data

## Global elements

| Element | Behaviour | Release |
|---|---|---|
| Search | One box for companies (name, NSE symbol, BSE code). Keyboard shortcut `/`. Later extends to filings and research | MVP |
| Market-cap filter | Global chips: All, Large, Mid, Small, Micro. Applies to every module on the page | MVP |
| Sector filter | Pick a macro sector, sector or industry; the whole page narrows to it | MVP |
| Period switch | 1D, 1W, 1M, 3M, 1Y on overview tiles | MVP |
| Theme | Light and dark | MVP |
| Disclaimer | Persistent footer line plus a full page | MVP |
| Data freshness badge | "Prices as of <date>" in the header | MVP |
| Sign-in | Single user at first; accounts only if the project goes multi-user | Later |

### Market-cap buckets

| Bucket | Range (market cap) |
|---|---|
| Large | ₹1,00,000 Cr and above |
| Mid | ₹30,000 Cr to ₹1,00,000 Cr |
| Small | ₹5,000 Cr to ₹30,000 Cr |
| Micro | Below ₹5,000 Cr |

Thresholds live in config so they can be changed without code edits.

## 1. Market overview (MVP)

The home page.

- **Indices:** headline indices and India VIX with level, change for the selected period and a sparkline. Click opens a chart.
- **Sector indices:** sorted by change for the selected period.
- **Market breadth:** advances, declines, unchanged; advance/decline ratio; count at 52-week high and low; share of companies above 50-day and 200-day moving averages.
- **Industry rotation strip:** market-cap-weighted return per macro sector with "n of m up". Click filters the page.
- **Movers:** top gainers, top losers, volume shockers, most active by value, 52-week highs and lows, breakouts with volume.

Data needed: daily prices, index constituents and levels, company-to-industry mapping, market cap.

## 2. Scanner (MVP, expanding)

A scan is a named rule that returns the set of companies passing it on a given day.

- Library of scans grouped by category. MVP ships about 20; the target is 100+.
- Each scan runs nightly over the whole universe. Results are stored per day.
- For every scan: current members, **new entries** and **exits** versus the previous session, and a daily count history.
- Scan detail page: plain-language rule, result table with the columns relevant to that rule, history chart.
- Per stock: every scan it is currently in.
- **Combine** 2 to 4 scans (intersection). V1.
- **Past hit rates:** forward returns of stocks after entering a scan (1W, 1M, 3M). V1.
- Each scan is tagged bullish, bearish or neutral, and "red flag" scans are a separate group.

### Scan categories and MVP set

| Category | MVP scans | Release |
|---|---|---|
| Technical | RSI crosses 50 up, RSI overbought, RSI oversold, MACD bullish crossover, golden cross, death cross, supertrend turns up, 20-day range breakout, strong uptrend (price > 50-DMA > 200-DMA) | MVP |
| Volume | Volume shocker (3x 20-day average, price up), volume shocker down | MVP |
| Candlestick | Bullish engulfing, bearish engulfing, hammer, shooting star | MVP |
| Price levels | New 52-week high, new 52-week low, near all-time high | MVP |
| Growth | EPS accelerating, revenue accelerating | MVP |
| Quality | Margin expanders, low debt with high ROCE | MVP |
| Value | Low PEG fast growers | V1 |
| Smart money | New 1%+ holder this quarter, promoter buying | V1 |
| Results | Results beat previous quarter and year-ago quarter | V1 |
| Red flags | Promoter pledge rising, receivables growing faster than sales, auditor change | V1 |
| Guidance | Management guided faster growth, guidance accuracy | V1 (needs AI layer) |
| Corporate actions | Capex announced, capital raise | V1 (needs filings classifier) |

Exact rule definitions live with the code, one file per scan, and are rendered on the scan page.

## 3. Screener (MVP)

- Filter the universe on any field with comparison operators.
- **Formula mode:** expressions such as `ROCE > 20 AND PEG < 1 AND MarketCap > 5000`. Supports `AND`, `OR`, `NOT`, parentheses, arithmetic between fields.
- Choose result columns; sort; export CSV.
- Saved screens and a library of quick screens.
- MVP ships about 60 fields; the target is 300+.

Field groups: price and returns, valuation, profitability, growth, balance sheet, cash flow, shareholding, technical indicators, scores.

The formula language is parsed into an AST and compiled to SQL. User input never reaches the database as raw text.

## 4. Stock page (MVP, expanding)

| Section | Content | Release |
|---|---|---|
| Header | Name, symbols, industry, price, change, market cap, key ratios | MVP |
| Chart | Daily candles, volume, moving averages, period switch | MVP |
| Financials | Quarterly and annual P&L, balance sheet, cash flow | MVP |
| Ratios | Valuation, profitability and growth, with 5-year history | MVP |
| Scans | Scans this stock is in today, with entry dates | MVP |
| Peers | Industry peers table | MVP |
| Shareholding | Quarterly pattern and notable holders | V1 |
| Filings | Classified exchange filings | V1 |
| Research | AI summary of latest results and concall | V1 |
| Score | Tathya Score with pillar breakdown | V1 |
| Estimates | Forward estimates with evidence | Later |

## 5. Compare and scatter (V1)

- Compare up to 10 stocks side by side across chosen metrics.
- Scatter plot of any two fields across the filtered universe, with preset pairs (for example ROCE against P/E).

## 6. Strategy tools (V1)

Three rule-based lenses, each producing a score and a verdict per company:

- **Cyclicals:** input-cost and selling-price trends against margins.
- **Fast growers:** growth quality and price paid for it.
- **Turnarounds:** stages from deteriorating to recovery confirmed.

## 7. Smart money (V1)

- Quarterly shareholding by category: promoters, FIIs, mutual funds, insurers, public.
- A curated list of tracked investors and their holdings of 1% or more, with adds, trims, entries and exits each quarter.
- Estimated entry price range for a quarter's change (the quarter's price range, clearly labelled as an estimate).
- Capital raises with allottees and issue price.

## 8. Forward signals and estimates (V1 and Later)

- **Signals (V1):** guidance extracted from concalls and presentations (revenue, margin, order book, capex), each with the quote, the document and its date, then checked against later reported results.
- **Estimates (Later):** multi-year revenue, margin and profit estimates, each tied to stated evidence.

## 9. Tathya Score (V1)

- Five pillars: Quality, Growth, Governance, Valuation, Momentum. Each 0 to 100.
- A weighted composite with a letter grade. The user can move the weights and the ranking updates.
- The score page shows the inputs behind every pillar.

## 10. Industry rotation (MVP basic, V1 full)

- Returns per industry and sector over periods from 1 day to several years, market-cap weighted.
- Breadth per group.
- Group valuation and profitability (P/E, P/B, ROE, margins). V1.
- Leaders and laggards per group.

## 11. Results and filings (V1)

- **Results calendar:** board-meeting dates and results as they arrive.
- **Filings feed:** exchange announcements classified by document type, event and priority, searchable, with a link to the source document.

## 12. IPO calendar (V1)

Open, upcoming and recently listed issues for mainboard and SME: dates, size, price band, and listing performance against issue price.

## 13. Ask Tathya (V1)

- Question box scoped to one company.
- Answers come only from that company's stored documents and data, with citations to the document and page.
- If the documents do not contain the answer, it says so.
- Every answer carries the "not investment advice" line.
