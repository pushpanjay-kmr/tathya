# TODO

Deferred items and open questions. Build tasks live in the [roadmap](docs/08-roadmap.md).

## Deferred by decision

- [ ] **Licensed market-data feed.** Choose a vendor, confirm display rights, implement as providers, backfill and switch. See [Data sources](docs/07-data-sources.md).
- [ ] **Regulatory review before any public launch.** Confirm with a qualified professional whether scores, verdicts, estimates and AI answers need SEBI registration. See [Compliance and disclaimer](docs/09-compliance-and-disclaimer.md).
- [ ] **Terms of use check for each free data source** before it is wired in. Record the result in `docs/07-data-sources.md`.
- [ ] **Live or delayed intraday prices.** Blocked on the licensed feed.

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
