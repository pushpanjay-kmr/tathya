# TODO

Deferred items and open questions. Build tasks live in the [roadmap](docs/08-roadmap.md).

## Deferred by decision

- [ ] **Licensed market-data feed.** Choose a vendor, confirm display rights, implement as providers, backfill and switch. See [Data sources](docs/07-data-sources.md).
- [ ] **Regulatory review before any public launch.** Confirm with a qualified professional whether scores, verdicts, estimates and AI answers need SEBI registration. See [Compliance and disclaimer](docs/09-compliance-and-disclaimer.md).
- [ ] **Terms of use check for each free data source** before it is wired in. Record the result in `docs/07-data-sources.md`. NSE and BSE checked (2026-11-13): both block scraping and/or storing their data without written permission. EODHD's terms are fine (personal-use licence) but it doesn't serve NSE/BSE on the current plan — confirmed by live API test, not just docs. Still need a source that both permits this and actually covers India; the pipeline's ingest code is proven against EODHD's US coverage in the meantime.
- [ ] **Live or delayed intraday prices.** Blocked on the licensed feed.
- [ ] **Purge sample data and switch to a real price provider before any real use, demo or public version.** `config/providers.yaml` currently points `prices` at the `sample` provider (synthetic OHLCV, `source = 'sample'`), approved 2026-11-13 as a time-boxed exception to "no fake data in the app" purely to unblock app development. See `docs/10-decisions.md` #10. The owner plans to get an NSE/BSE subscription once the project is ready to go public — do this then: `TRUNCATE price_daily, company, provider_fetch, pipeline_run`, implement the real provider, switch `config/providers.yaml`.

## Design phase

- [x] Home page mockups in both visual directions (Ledger, Terminal)
- [x] Choose the default direction and record it in the decision log (Ledger)
- [x] Mockups: stock page, scanner, screener
- [ ] Wordmark and favicon

## Engineering follow-ups

- [ ] Add a migration tool so new SQL files apply to an existing database automatically
- [ ] Theme toggle for the Terminal (dark) theme
- [ ] Favicon

## Open questions

- [ ] Local only, or private hosted deployment?
- [ ] LLM provider and monthly budget for the AI layer
- [ ] Default financial basis: consolidated or standalone
- [ ] Repository licence
- [ ] Is the GitHub repository public or private? If public, keep data and secrets out and make sure the README warning stays prominent
