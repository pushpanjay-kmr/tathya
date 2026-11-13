"""Pipeline configuration: database URL and provider selection.

The pipeline lives in a subdirectory of the repo but shares the repo-root
``.env`` with the web app (see ``docker-compose.yml`` and ``.env.example``).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
PIPELINE_ROOT = Path(__file__).resolve().parents[1]
PROVIDERS_CONFIG_PATH = PIPELINE_ROOT / "config" / "providers.yaml"

load_dotenv(REPO_ROOT / ".env")


@dataclass(frozen=True)
class DatasetProviders:
    primary: str
    fallback: str | None = None


def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy .env.example to .env at the repo root."
        )
    return url


def load_provider_config(
    path: Path = PROVIDERS_CONFIG_PATH,
) -> dict[str, DatasetProviders]:
    """Read config/providers.yaml: which provider serves each dataset.

    See docs/07-data-sources.md for the expected shape. Returns an empty
    dict if the file is missing or has no `providers` section yet — no
    provider has been wired in while the terms-of-use TODO is open.
    """
    if not path.exists():
        return {}

    raw = yaml.safe_load(path.read_text()) or {}
    datasets = raw.get("providers", {}) or {}
    return {
        dataset: DatasetProviders(primary=entry["primary"], fallback=entry.get("fallback"))
        for dataset, entry in datasets.items()
    }
