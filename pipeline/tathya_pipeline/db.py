"""SQLAlchemy engine and session for the pipeline.

The pipeline writes directly with SQLAlchemy Core (no ORM models): the
schema is owned by db/migrations/*.sql, and pandas DataFrames map onto it
more directly through Core than through an ORM layer.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from tathya_pipeline.config import database_url

_engine: Engine | None = None
_SessionFactory: sessionmaker[Session] | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(database_url())
    return _engine


@contextmanager
def session_scope() -> Iterator[Session]:
    """Yield a session in a transaction; commits on success, rolls back on error."""
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(bind=get_engine())

    session = _SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
