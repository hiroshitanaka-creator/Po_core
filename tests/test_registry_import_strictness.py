from po_core.philosophers.manifest import PhilosopherSpec
from po_core.philosophers.registry import PhilosopherRegistry


def test_load_raises_for_enabled_spec_import_failure() -> None:
    registry = PhilosopherRegistry(
        specs=[
            PhilosopherSpec(
                philosopher_id="enabled_broken",
                module="po_core.philosophers.__missing_enabled__",
                symbol="Missing",
                enabled=True,
            )
        ],
        cache_instances=False,
    )

    try:
        registry.load(["enabled_broken"])
        assert False, "RuntimeError was not raised"
    except RuntimeError as exc:
        assert "failed_to_load_enabled_philosopher:enabled_broken" in str(exc)


def test_load_collects_error_for_disabled_spec_import_failure() -> None:
    registry = PhilosopherRegistry(
        specs=[
            PhilosopherSpec(
                philosopher_id="disabled_broken",
                module="po_core.philosophers.__missing_disabled__",
                symbol="Missing",
                enabled=False,
            )
        ],
        cache_instances=False,
    )

    loaded, errors = registry.load(["disabled_broken"])

    assert loaded == []
    assert len(errors) == 1
    assert errors[0].philosopher_id == "disabled_broken"
    assert errors[0].error == "ModuleNotFoundError"
