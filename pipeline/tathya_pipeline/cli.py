"""Entry points: ingest, compute, scan, all.

See docs/05-architecture.md, "Nightly pipeline". Each command opens one
pipeline_run row for the given date (default: today) and records a step
status as it goes, so the web app can always show the as-of date of the
last good run.
"""

from __future__ import annotations

import datetime as dt

import click

from tathya_pipeline import db
from tathya_pipeline import ingest as ingest_step
from tathya_pipeline.run import finish_run, record_step, start_run

DATE_OPTION = click.option(
    "--date",
    "as_of",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
    help="Trading date to run for (YYYY-MM-DD). Defaults to today.",
)


def _resolve_date(as_of: dt.datetime | None) -> dt.date:
    return as_of.date() if as_of else dt.date.today()


@click.group()
def cli() -> None:
    """Tathya's nightly data pipeline."""


@cli.command()
@DATE_OPTION
def ingest(as_of: dt.datetime | None) -> None:
    """Fetch raw data from each configured provider into staging."""
    target_date = _resolve_date(as_of)
    with db.session_scope() as session:
        run_id = start_run(session, target_date)
        ingest_step.ingest_prices(session, run_id, target_date)
        record_step(session, run_id, "ingest", "succeeded")
        finish_run(session, run_id, "succeeded")
    click.echo(f"Ingest run {run_id} for {target_date} recorded.")


@cli.command()
@DATE_OPTION
def compute(as_of: dt.datetime | None) -> None:
    """Compute indicators, ratios and aggregates for the given date."""
    target_date = _resolve_date(as_of)
    click.echo(f"compute: nothing to do yet for {target_date} (see tathya_pipeline/compute).")


@cli.command()
@DATE_OPTION
def scan(as_of: dt.datetime | None) -> None:
    """Evaluate all registered scans for the given date."""
    target_date = _resolve_date(as_of)
    click.echo(f"scan: no scans registered yet for {target_date} (see tathya_pipeline/scans).")


@cli.command(name="all")
@DATE_OPTION
@click.pass_context
def run_all(ctx: click.Context, as_of: dt.datetime | None) -> None:
    """Run ingest, compute and scan in sequence for the given date."""
    ctx.invoke(ingest, as_of=as_of)
    ctx.invoke(compute, as_of=as_of)
    ctx.invoke(scan, as_of=as_of)


if __name__ == "__main__":
    cli()
