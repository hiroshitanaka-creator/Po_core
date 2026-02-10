"""Shadow Guard - Autonomous brake for shadow philosophy configurations.

Monitors shadow variant performance and automatically disables it when degradation
is detected, ensuring main configuration is never polluted by unstable shadows.

Key Features:
- Policy score monitoring (safety degradation detection)
- Utility degradation detection (action pair monitoring)
- Bad streak tracking with automatic disable/cooldown
- Full audit trail via ShadowDisabled TraceEvents
- State persistence for production resilience
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional, Protocol, Tuple

from po_core.domain.context import Context
from po_core.domain.proposal import Proposal
from po_core.domain.trace_event import TraceEvent


def _as_dict(x: Any) -> dict:
    return dict(x) if isinstance(x, Mapping) else {}


def _to_float(x: Any) -> Optional[float]:
    try:
        return float(x)
    except Exception:
        return None


@dataclass(frozen=True)
class ShadowGuardConfig:
    """
    Shadow's "autonomous brake" configuration.

    - policy_score_drop_threshold:
        If shadow's final policy_score drops below main by this much, treat as degradation.
        (policy_score comes from Gate verdict = close to ground truth of safety)
    - min_shadow_policy_score:
        Absolute minimum policy score for shadow (safety floor)
    - max_bad_streak:
        How many consecutive degradations before disabling (1 = immediate stop)
    - cooldown_s:
        After disabling, skip shadow for this many seconds (then retry = keep nurturing)
    - disable_action_pairs:
        Action pairs that indicate utility degradation.
        e.g., ("answer", "refuse") = "could answer but regressed to refuse"
    - disable_on_override_increase:
        If shadow has more safety overrides (fallback) than main, treat as unstable degradation.
    """

    enabled: bool = True
    policy_score_drop_threshold: float = 0.15
    min_shadow_policy_score: float = 0.0

    max_bad_streak: int = 2
    cooldown_s: float = 3600.0

    disable_action_pairs: Tuple[Tuple[str, str], ...] = (("answer", "refuse"),)
    disable_on_override_increase: bool = True


@dataclass(frozen=True)
class ShadowGuardState:
    """Persistent state for a specific shadow configuration."""

    shadow_key: str
    bad_streak: int = 0
    disabled_until_ts: float = 0.0
    disabled_reason: str = ""
    updated_at_ts: float = 0.0

    def is_disabled(self, now_ts: float) -> bool:
        return now_ts < self.disabled_until_ts


class ShadowGuardStore(Protocol):
    """Protocol for persisting ShadowGuard state."""

    def load(self) -> Optional[Mapping[str, Any]]:
        ...

    def save(self, data: Mapping[str, Any]) -> None:
        ...


class InMemoryShadowGuardStore(ShadowGuardStore):
    """In-memory store for testing."""

    def __init__(self):
        self.data: Optional[dict] = None

    def load(self) -> Optional[Mapping[str, Any]]:
        return self.data

    def save(self, data: Mapping[str, Any]) -> None:
        self.data = dict(data)


class FileShadowGuardStore(ShadowGuardStore):
    """File-based store for production use."""

    def __init__(self, path: str):
        self._path = path

    def load(self) -> Optional[Mapping[str, Any]]:
        if not self._path:
            return None
        if not os.path.exists(self._path):
            return None
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def save(self, data: Mapping[str, Any]) -> None:
        if not self._path:
            return
        d = os.path.dirname(self._path)
        if d:
            os.makedirs(d, exist_ok=True)

        tmp = self._path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(dict(data), f, ensure_ascii=False, indent=2, sort_keys=True)
        os.replace(tmp, self._path)


def _shadow_key(version: str, source: str) -> str:
    """Generate unique key for shadow config (version + source)."""
    return f"v={version} src={source}"


def _policy_score_from(p: Proposal) -> float:
    """Extract policy score from proposal extra._po_core.policy.score."""
    extra = _as_dict(p.extra)
    pc = _as_dict(extra.get("_po_core"))
    pol = _as_dict(pc.get("policy"))
    v = _to_float(pol.get("score"))
    return float(v) if v is not None else 0.0


class ShadowGuard:
    """
    Autonomous brake for shadow philosophy configurations.

    - should_run_shadow(): Check if shadow should run now (skip if disabled + emit event)
    - observe_comparison(): Observe main vs shadow results, update state (disable if degraded + emit event)

    Philosophy: "Shadow is shadow. Never pollute main. Nurture dreams safely."
    """

    def __init__(
        self,
        config: ShadowGuardConfig,
        store: ShadowGuardStore,
        *,
        shadow_config_version: str,
        shadow_config_source: str,
        now_fn: Callable[[], float] = time.time,
    ):
        self._cfg = config
        self._store = store
        self._shadow_version = str(shadow_config_version)
        self._shadow_source = str(shadow_config_source)
        self._key = _shadow_key(self._shadow_version, self._shadow_source)
        self._now = now_fn

    # ---- State I/O ----

    def _deserialize(self, data: Mapping[str, Any]) -> ShadowGuardState:
        d = _as_dict(data)
        return ShadowGuardState(
            shadow_key=str(d.get("shadow_key", "")),
            bad_streak=int(d.get("bad_streak", 0) or 0),
            disabled_until_ts=float(d.get("disabled_until_ts", 0.0) or 0.0),
            disabled_reason=str(d.get("disabled_reason", "")),
            updated_at_ts=float(d.get("updated_at_ts", 0.0) or 0.0),
        )

    def _serialize(self, st: ShadowGuardState) -> dict:
        return {
            "shadow_key": st.shadow_key,
            "bad_streak": st.bad_streak,
            "disabled_until_ts": st.disabled_until_ts,
            "disabled_reason": st.disabled_reason,
            "updated_at_ts": st.updated_at_ts,
        }

    def state(self) -> ShadowGuardState:
        """Get current state (for testing/diagnostics)."""
        now = self._now()
        raw = self._store.load()
        if not raw:
            return ShadowGuardState(shadow_key=self._key, updated_at_ts=now)

        st = self._deserialize(raw)
        if st.shadow_key != self._key:
            # Config changed - don't carry over old disable state (nurture new dreams)
            return ShadowGuardState(shadow_key=self._key, updated_at_ts=now)

        return st

    def _save(self, st: ShadowGuardState) -> None:
        try:
            self._store.save(self._serialize(st))
        except Exception:
            # Never crash main due to shadow state save failure (shadow is auxiliary)
            pass

    # ---- Events ----

    def _event_shadow_disabled(
        self, ctx: Context, *, action: str, reason: str, payload: Mapping[str, Any]
    ) -> TraceEvent:
        """Emit ShadowDisabled TraceEvent for audit trail."""
        base = {
            "variant": "shadow",
            "action": action,  # disabled_now / skipped_disabled
            "reason": reason,
            "shadow_config_version": self._shadow_version,
            "shadow_config_source": self._shadow_source,
        }
        out = dict(base)
        out.update(dict(payload))
        return TraceEvent.now("ShadowDisabled", ctx.request_id, out)

    # ---- Decision Logic ----

    def should_run_shadow(self, ctx: Context) -> Tuple[bool, Optional[TraceEvent]]:
        """
        Check if shadow should run now.

        Returns:
            (should_run, event)
            - If disabled: (False, ShadowDisabled event with action=skipped_disabled)
            - If enabled: (True, None)
        """
        if not self._cfg.enabled:
            return True, None

        now = self._now()
        st = self.state()

        if st.is_disabled(now):
            ev = self._event_shadow_disabled(
                ctx,
                action="skipped_disabled",
                reason=st.disabled_reason or "cooldown_active",
                payload={
                    "disabled_until_ts": st.disabled_until_ts,
                    "bad_streak": st.bad_streak,
                    "max_bad_streak": self._cfg.max_bad_streak,
                    "cooldown_s": self._cfg.cooldown_s,
                },
            )
            return False, ev

        return True, None

    def observe_comparison(
        self,
        ctx: Context,
        *,
        main_candidate: Proposal,
        main_final: Proposal,
        shadow_candidate: Proposal,
        shadow_final: Proposal,
        main_degraded: bool,
        shadow_degraded: bool,
    ) -> Optional[TraceEvent]:
        """
        Observe main vs shadow comparison results and update state.

        If degradation threshold exceeded for consecutive max_bad_streak times,
        disable shadow and emit ShadowDisabled event with action=disabled_now.

        Returns:
            - TraceEvent if shadow was disabled now
            - None if shadow remains enabled
        """
        if not self._cfg.enabled:
            return None

        now = self._now()
        st = self.state()

        # ---- Extract metrics ----
        main_ps = _policy_score_from(main_final)
        shadow_ps = _policy_score_from(shadow_final)
        delta = shadow_ps - main_ps  # positive = shadow safer

        # Utility degradation (specified action pairs only)
        action_pair = (main_final.action_type, shadow_final.action_type)
        utility_drop = action_pair in set(self._cfg.disable_action_pairs)

        # Override increase (shadow degraded but main didn't)
        override_increase = bool(
            self._cfg.disable_on_override_increase
            and shadow_degraded
            and not main_degraded
        )

        # Safety degradation
        safety_drop = False
        if shadow_ps < self._cfg.min_shadow_policy_score:
            safety_drop = True
            reason = "min_shadow_policy_score"
        elif delta < -abs(self._cfg.policy_score_drop_threshold):
            safety_drop = True
            reason = "policy_score_drop"
        elif override_increase:
            reason = "override_increase"
        elif utility_drop:
            reason = "utility_drop_action"
        else:
            reason = ""

        is_bad = safety_drop or override_increase or utility_drop

        # ---- Update state ----
        if is_bad:
            bad_streak = st.bad_streak + 1
        else:
            bad_streak = 0  # Recovery is immediate (don't stop nurturing dreams)

        disabled_now = False
        disabled_until = st.disabled_until_ts
        disabled_reason = st.disabled_reason

        if is_bad and bad_streak >= max(1, int(self._cfg.max_bad_streak)):
            disabled_now = True
            disabled_until = now + float(self._cfg.cooldown_s)
            disabled_reason = reason or "degraded"

        new_state = ShadowGuardState(
            shadow_key=self._key,
            bad_streak=bad_streak,
            disabled_until_ts=disabled_until,
            disabled_reason=disabled_reason if disabled_until > now else "",
            updated_at_ts=now,
        )
        self._save(new_state)

        if not disabled_now:
            return None

        # ---- Emit ShadowDisabled (disabled_now) ----
        ev = self._event_shadow_disabled(
            ctx,
            action="disabled_now",
            reason=reason or "degraded",
            payload={
                "disabled_until_ts": disabled_until,
                "bad_streak": bad_streak,
                "max_bad_streak": self._cfg.max_bad_streak,
                "cooldown_s": self._cfg.cooldown_s,
                "thresholds": {
                    "policy_score_drop_threshold": self._cfg.policy_score_drop_threshold,
                    "min_shadow_policy_score": self._cfg.min_shadow_policy_score,
                    "disable_action_pairs": list(self._cfg.disable_action_pairs),
                    "disable_on_override_increase": self._cfg.disable_on_override_increase,
                },
                "metrics": {
                    "main_policy_score": main_ps,
                    "shadow_policy_score": shadow_ps,
                    "policy_score_delta": delta,
                    "main_final_action": main_final.action_type,
                    "shadow_final_action": shadow_final.action_type,
                    "main_degraded": bool(main_degraded),
                    "shadow_degraded": bool(shadow_degraded),
                    "utility_drop_pair": f"{action_pair[0]}->{action_pair[1]}",
                    "override_increase": bool(override_increase),
                },
            },
        )
        return ev
