"""Step 6 of the nightly pipeline: evaluate scans, write memberships.

See docs/05-architecture.md, "Scan engine":

- A scan is a Python object: id, name, category, stance, plain-language
  description, required fields, and a function from a universe DataFrame
  to a boolean mask.
- The engine builds one wide DataFrame for the day (plus the lookback each
  scan declares), evaluates all scans, and writes scan_result rows.
- Entries and exits are computed by set difference with the previous
  session.
- The description stored with the scan is what the UI shows, so the rule
  on screen is always the rule that ran.

No scans are defined yet — this waits on real price and fundamentals data
from ingest/compute. Add one scan per file in this package and register it
in SCANS below.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

import pandas as pd

Stance = Literal["bullish", "bearish", "neutral", "red_flag"]


@dataclass(frozen=True)
class Scan:
    id: str
    name: str
    category: str
    stance: Stance
    description: str
    required_fields: tuple[str, ...]
    predicate: Callable[[pd.DataFrame], pd.Series]


SCANS: list[Scan] = []


def run_scans(
    universe: pd.DataFrame, scans: list[Scan] | None = None
) -> dict[str, pd.Series]:
    """Evaluate scans (default: SCANS, the registered set) against the day's universe."""
    return {scan.id: scan.predicate(universe) for scan in (scans if scans is not None else SCANS)}
