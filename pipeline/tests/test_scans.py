from __future__ import annotations

import pandas as pd

from tathya_pipeline.scans import Scan, run_scans


def test_run_scans_evaluates_each_registered_scan():
    universe = pd.DataFrame({"roce": [25, 10, 30]})
    high_roce = Scan(
        id="high_roce",
        name="High ROCE",
        category="quality",
        stance="bullish",
        description="ROCE above 20%",
        required_fields=("roce",),
        predicate=lambda df: df["roce"] > 20,
    )

    result = run_scans(universe, scans=[high_roce])

    assert list(result["high_roce"]) == [True, False, True]
