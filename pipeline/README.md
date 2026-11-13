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
| `tathya_pipeline/providers/registry.py` | Maps a provider id to its class |
| `tathya_pipeline/providers/sample.py` | **Temporary.** Synthetic OHLCV for 5 real companies, `source = "sample"`. Unblocks app development with no real Indian price source wired in yet — see `docs/10-decisions.md` #10 and `TODO.md` |
| `tathya_pipeline/providers/eodhd.py` | EODHD price provider. Terms are fine for personal use, but it doesn't serve NSE/BSE on the current plan — see `docs/07-data-sources.md` |
| `config/providers.yaml` | Which provider serves each dataset |
| `tathya_pipeline/ingest/` | Step 1-3: fetch, validate, load into core tables |
| `tathya_pipeline/compute/` | Step 5: indicators, ratios, aggregates |
| `tathya_pipeline/scans/` | Step 6: scan definitions and the scan engine |
| `tathya_pipeline/ai/` | The AI layer: summaries, extraction, Ask Tathya (phase 5) |
| `tathya_pipeline/run.py` | Bookkeeping: `pipeline_run` and `provider_fetch` rows |
| `tathya_pipeline/cli.py` | The `tathya-pipeline` command |

## Prices currently come from the sample provider, not a real source

`config/providers.yaml` points `prices` at `sample` — synthetic data for 5 companies, always tagged `source = 'sample'` in `price_daily`. This was explicitly approved as a time-boxed exception to "no fake data in the app" (see `docs/10-decisions.md` #10), purely so app development isn't blocked on a compliant Indian price source. **Before any real use, demo or public version:** `TRUNCATE price_daily, company, provider_fetch, pipeline_run`, wire in a real provider, and point `config/providers.yaml` at it instead (see `TODO.md`).

`tathya_pipeline/providers/eodhd.py` is a working provider for whatever EODHD actually covers (it does not currently serve NSE or BSE — see [Data sources](../docs/07-data-sources.md)). To add a different real source: write a provider module under `tathya_pipeline/providers/`, register it in `registry.py`, and name it in `config/providers.yaml` — but read and record its terms of use in `docs/07-data-sources.md` first.

## Tests

```
python -m pytest
```
