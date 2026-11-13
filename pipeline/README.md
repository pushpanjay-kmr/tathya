# Tathya data pipeline

The Python package that fetches, validates, computes and scans market data, nightly. See [Architecture](../docs/05-architecture.md), "Nightly pipeline", for what each step does.

## Set up

Needs Python 3.11+ and a running database (`docker compose up -d` from the repository root).

```
cd pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run it

```
tathya-pipeline ingest --date 2026-11-13   # fetch raw data into staging
tathya-pipeline compute --date 2026-11-13  # indicators, ratios, aggregates
tathya-pipeline scan --date 2026-11-13     # evaluate scans
tathya-pipeline all --date 2026-11-13      # all three, in order
```

`--date` defaults to today. Every run writes a row to `pipeline_run`, and every provider call writes a row to `provider_fetch` — see them with:

```
docker compose exec -T db psql -U tathya -d tathya -c "SELECT * FROM pipeline_run ORDER BY id DESC LIMIT 5;"
```

## Where things are

| Path | What it holds |
|---|---|
| `tathya_pipeline/providers/base.py` | The provider contract (`PriceProvider`, `FundamentalsProvider`, ...). See [Data sources](../docs/07-data-sources.md) |
| `tathya_pipeline/providers/registry.py` | Maps a provider id to its class. Empty until a provider is written |
| `config/providers.yaml` | Which provider serves each dataset. Empty until a source's terms of use are recorded (see `TODO.md`) |
| `tathya_pipeline/ingest/` | Step 1-3: fetch, validate, load into core tables |
| `tathya_pipeline/compute/` | Step 5: indicators, ratios, aggregates |
| `tathya_pipeline/scans/` | Step 6: scan definitions and the scan engine |
| `tathya_pipeline/ai/` | The AI layer: summaries, extraction, Ask Tathya (phase 5) |
| `tathya_pipeline/run.py` | Bookkeeping: `pipeline_run` and `provider_fetch` rows |
| `tathya_pipeline/cli.py` | The `tathya-pipeline` command |

## No provider is wired in yet

`tathya-pipeline ingest` runs, but every dataset is skipped and logged as `skipped` in `provider_fetch` with reason "no provider configured". That's expected: each free data source needs its terms of use read and recorded in [Data sources](../docs/07-data-sources.md) before it's wired in (tracked in `TODO.md`). Once one is, add the provider module under `tathya_pipeline/providers/`, register it in `registry.py`, and name it in `config/providers.yaml`.

## Tests

```
python -m pytest
```
