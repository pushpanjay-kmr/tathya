"""Bookkeeping for a pipeline run: the pipeline_run and provider_fetch tables.

See docs/05-architecture.md, "Nightly pipeline", step 7 (Publish): the web
app keeps showing the last good run, so every run — even one that fails —
gets a row here with a status.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Literal

from sqlalchemy import text
from sqlalchemy.orm import Session

RunStatus = Literal["running", "succeeded", "failed"]
FetchStatus = Literal["ok", "failed", "skipped"]


def start_run(session: Session, as_of_date: date) -> int:
    result = session.execute(
        text(
            "INSERT INTO pipeline_run (as_of_date, status) "
            "VALUES (:as_of_date, 'running') RETURNING id"
        ),
        {"as_of_date": as_of_date},
    )
    return result.scalar_one()


def record_step(session: Session, run_id: int, step: str, status: str) -> None:
    """Merge one step's status into pipeline_run.step_status (jsonb)."""
    session.execute(
        text(
            "UPDATE pipeline_run "
            "SET step_status = step_status || jsonb_build_object(CAST(:step AS text), CAST(:status AS text)) "
            "WHERE id = :run_id"
        ),
        {"run_id": run_id, "step": step, "status": status},
    )


def finish_run(
    session: Session, run_id: int, status: RunStatus, notes: str | None = None
) -> None:
    session.execute(
        text(
            "UPDATE pipeline_run "
            "SET status = :status, finished_at = :finished_at, notes = :notes "
            "WHERE id = :run_id"
        ),
        {
            "run_id": run_id,
            "status": status,
            "finished_at": datetime.now(timezone.utc),
            "notes": notes,
        },
    )


def record_fetch(
    session: Session,
    run_id: int | None,
    provider: str,
    dataset: str,
    as_of_date: date,
    status: FetchStatus,
    row_count: int | None = None,
    error: str | None = None,
) -> None:
    session.execute(
        text(
            "INSERT INTO provider_fetch "
            "(run_id, provider, dataset, as_of_date, row_count, status, error) "
            "VALUES (:run_id, :provider, :dataset, :as_of_date, :row_count, :status, :error)"
        ),
        {
            "run_id": run_id,
            "provider": provider,
            "dataset": dataset,
            "as_of_date": as_of_date,
            "row_count": row_count,
            "status": status,
            "error": error,
        },
    )
