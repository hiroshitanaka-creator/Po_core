"""Tests for ShadowGuard autonomous brake system."""

from datetime import datetime, timezone

from po_core.domain.context import Context
from po_core.domain.proposal import Proposal
from po_core.runtime.shadow_guard import (
    InMemoryShadowGuardStore,
    ShadowGuard,
    ShadowGuardConfig,
)


def _p(pid: str, action: str, policy_score: float) -> Proposal:
    """Create test proposal with policy score."""
    return Proposal(
        proposal_id=pid,
        action_type=action,
        content="x",
        confidence=0.5,
        extra={"_po_core": {"policy": {"score": f"{policy_score:.3f}"}}},
    )


def test_shadow_guard_degradation_disables_shadow():
    """Test that policy_score drop immediately disables shadow (max_bad_streak=1)."""
    now = 1000.0
    store = InMemoryShadowGuardStore()
    guard = ShadowGuard(
        ShadowGuardConfig(
            enabled=True,
            policy_score_drop_threshold=0.10,
            max_bad_streak=1,
            cooldown_s=100.0,
            disable_action_pairs=(),  # Test safety metric only
            disable_on_override_increase=False,
        ),
        store,
        shadow_config_version="9",
        shadow_config_source="file:shadow.yaml",
        now_fn=lambda: now,
    )

    ctx = Context("r1", datetime.now(timezone.utc), "x")

    main_c = _p("mc", "answer", 1.0)
    main_f = _p("mf", "answer", 1.0)

    shadow_c = _p("sc", "answer", 1.0)
    shadow_f = _p("sf", "answer", 0.6)  # drop = 0.4 > threshold

    ev = guard.observe_comparison(
        ctx,
        main_candidate=main_c,
        main_final=main_f,
        shadow_candidate=shadow_c,
        shadow_final=shadow_f,
        main_degraded=False,
        shadow_degraded=False,
    )
    assert ev is not None
    assert ev.event_type == "ShadowDisabled"
    assert ev.payload["action"] == "disabled_now"
    assert ev.payload["reason"] == "policy_score_drop"

    # Now shadow should be skipped
    run, ev2 = guard.should_run_shadow(ctx)
    assert run is False
    assert ev2 is not None
    assert ev2.event_type == "ShadowDisabled"
    assert ev2.payload["action"] == "skipped_disabled"


def test_shadow_guard_equal_keeps_enabled():
    """Test that small policy_score differences keep shadow enabled."""
    now = 1000.0
    store = InMemoryShadowGuardStore()
    guard = ShadowGuard(
        ShadowGuardConfig(
            enabled=True,
            policy_score_drop_threshold=0.15,
            max_bad_streak=1,
            cooldown_s=100.0,
        ),
        store,
        shadow_config_version="9",
        shadow_config_source="file:shadow.yaml",
        now_fn=lambda: now,
    )

    ctx = Context("r1", datetime.now(timezone.utc), "x")

    main_c = _p("mc", "answer", 0.90)
    main_f = _p("mf", "answer", 0.90)

    shadow_c = _p("sc", "answer", 0.90)
    shadow_f = _p("sf", "answer", 0.88)  # drop = 0.02 < 0.15 threshold, OK

    ev = guard.observe_comparison(
        ctx,
        main_candidate=main_c,
        main_final=main_f,
        shadow_candidate=shadow_c,
        shadow_final=shadow_f,
        main_degraded=False,
        shadow_degraded=False,
    )
    assert ev is None

    run, ev2 = guard.should_run_shadow(ctx)
    assert run is True
    assert ev2 is None


def test_shadow_guard_improvement_recovers_from_bad_streak():
    """Test that improvement immediately recovers from bad streak."""
    now = 1000.0
    store = InMemoryShadowGuardStore()
    guard = ShadowGuard(
        ShadowGuardConfig(
            enabled=True,
            policy_score_drop_threshold=0.10,
            max_bad_streak=2,  # Don't disable on first degradation
            cooldown_s=100.0,
            disable_action_pairs=(),
            disable_on_override_increase=False,
        ),
        store,
        shadow_config_version="9",
        shadow_config_source="file:shadow.yaml",
        now_fn=lambda: now,
    )
    ctx = Context("r1", datetime.now(timezone.utc), "x")

    # Round 1: Degradation (bad_streak=1)
    ev1 = guard.observe_comparison(
        ctx,
        main_candidate=_p("mc1", "answer", 1.00),
        main_final=_p("mf1", "answer", 1.00),
        shadow_candidate=_p("sc1", "answer", 1.00),
        shadow_final=_p("sf1", "answer", 0.80),  # drop = 0.20
        main_degraded=False,
        shadow_degraded=False,
    )
    assert ev1 is None  # Not disabled yet (max_bad_streak=2)

    # Round 2: Improvement (bad_streak → 0)
    ev2 = guard.observe_comparison(
        ctx,
        main_candidate=_p("mc2", "answer", 0.90),
        main_final=_p("mf2", "answer", 0.90),
        shadow_candidate=_p("sc2", "answer", 0.90),
        shadow_final=_p("sf2", "answer", 0.95),  # improvement
        main_degraded=False,
        shadow_degraded=False,
    )
    assert ev2 is None

    # Shadow should still be enabled
    run, _ = guard.should_run_shadow(ctx)
    assert run is True
