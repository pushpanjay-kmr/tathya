from __future__ import annotations

import pytest

from tathya_pipeline.providers.registry import ProviderNotRegistered, get_provider


def test_unregistered_provider_raises_clear_error():
    with pytest.raises(ProviderNotRegistered, match="unknown_provider"):
        get_provider("unknown_provider")


def test_registered_provider_is_constructed():
    from tathya_pipeline.providers import registry

    registry._REGISTRY["dummy"] = lambda: "a provider instance"
    assert get_provider("dummy") == "a provider instance"
