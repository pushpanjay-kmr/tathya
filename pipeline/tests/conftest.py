from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _clear_provider_registry():
    """Each test starts with an empty provider registry."""
    from tathya_pipeline.providers import registry

    saved = dict(registry._REGISTRY)
    registry._REGISTRY.clear()
    yield
    registry._REGISTRY.clear()
    registry._REGISTRY.update(saved)
