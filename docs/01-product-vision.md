# 01. Product vision

## Problem

Researching an Indian listed company means stitching together several places: a charting site for price, a screener for ratios, the exchange website for filings and shareholding, and PDFs of concall transcripts for what management actually said. The facts exist, but they are scattered, and the reading takes hours per company.

## Vision

Tathya puts the facts about every listed Indian company in one place and does the first pass of reading for you. You should be able to go from "what moved today" to "why, and is it worth a closer look" without leaving the app.

The name is the brief: **तथ्य** means "fact". Every number on screen should be traceable to a source and a date.

## Who it is for

Right now, one user: the author, as a personal research tool. Design choices favour information density and keyboard speed over onboarding.

A possible later audience is the self-directed Indian retail investor who already uses a screener and reads annual reports. That audience is out of scope until the items in [Compliance and disclaimer](09-compliance-and-disclaimer.md) are resolved.

## Product principles

1. **Facts first, opinions labelled.** Reported numbers and filings are shown as they are. Anything computed or generated (scores, verdicts, AI answers) is visibly marked as derived and links to its inputs.
2. **Every number has a source and a date.** No figure appears without "as of" context.
3. **Rules you can read.** Each scan and score has a plain-language definition on screen. No black boxes.
4. **Start from the market, end at the company.** The home page shows what is happening today. Every tile leads down to a list, and every list leads to a stock page.
5. **Dense, not cluttered.** Tables and numbers are the content. Decoration stays out of the way.

## Goals

- Cover the full listed universe (roughly 2,000+ companies) with end-of-day prices and core fundamentals.
- Re-run every scan nightly and keep the history, so "what is new today" is always answerable.
- Make any idea screenable with a formula.
- Cut the time to understand a company's latest quarter from an hour to a few minutes.

## Non-goals

- **No trading.** No broker integration, no order placement, no portfolio execution.
- **No live prices.** End-of-day data only until a licensed feed is added.
- **No buy or sell recommendations.** Scores and verdicts describe rule outcomes, not advice.
- **No mobile app.** The web app is responsive; a native app is not planned.
- **No social features.** No feeds, comments or following.

## Inspiration

Tathya is inspired by the category of Indian stock-research tools that combine screeners, scans and AI reading of filings. It is an independent build with its own name, design, code and rule definitions. It does not copy any other product's branding, text or visual design.

## Success measures (personal use)

| Measure | Target |
|---|---|
| Nightly pipeline completes without manual fixes | 95% of trading days |
| Home page load on a warm cache | Under 1.5 seconds |
| Screener query over the full universe | Under 500 ms |
| Universe coverage with price and core fundamentals | Over 95% of listed companies |
