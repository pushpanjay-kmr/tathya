"""Maps a provider id (as used in config/providers.yaml) to its class.

Empty until the first provider is written and its terms of use recorded in
docs/07-data-sources.md (see TODO.md). Register a provider by adding it
here, e.g.:

    from tathya_pipeline.providers.exchange_eod import ExchangeEodProvider
    _REGISTRY["exchange_eod"] = ExchangeEodProvider
"""

from __future__ import annotations

from typing import Callable

def _eodhd():
    from tathya_pipeline.providers.eodhd import EodhdProvider

    return EodhdProvider()


_REGISTRY: dict[str, Callable[[], object]] = {
    "eodhd": _eodhd,
}


class ProviderNotRegistered(Exception):
    pass


def get_provider(provider_id: str) -> object:
    try:
        factory = _REGISTRY[provider_id]
    except KeyError as exc:
        raise ProviderNotRegistered(
            f"No provider registered for id {provider_id!r}. "
            "See tathya_pipeline/providers/registry.py."
        ) from exc
    return factory()
