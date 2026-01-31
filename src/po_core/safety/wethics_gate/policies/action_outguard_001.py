"""
WG.ACT.OUTGUARD.001 - Dangerous Output Guard
=============================================

Detects potential secrets and dangerous execution patterns in output.
Not perfect, but catches the majority of accidents.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Tuple

from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.safety_verdict import Decision, SafetyVerdict
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.safety.wethics_gate.policies.base import ActionPolicy


@dataclass(frozen=True)
class DangerousOutputGuardPolicy(ActionPolicy):
    """
    WG.ACT.OUTGUARD.001
    Guards against secrets and dangerous execution patterns in output.
    """

    rule_id: str = "WG.ACT.OUTGUARD.001"
    priority: int = 20

    # Patterns for secret-like content
    secret_patterns: Tuple[Tuple[str, str], ...] = (
        ("private_key_block", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        ("aws_access_key_like", r"\bAKIA[0-9A-Z]{16}\b"),
        ("generic_password_assign", r"(?i)\bpassword\s*[:=]\s*\S+"),
        ("generic_api_key_assign", r"(?i)\bapi[_-]?key\s*[:=]\s*\S+"),
    )

    # Patterns for dangerous execution hints
    exec_patterns: Tuple[Tuple[str, str], ...] = (
        ("destructive_shell_hint", r"(?i)\brm\s+-rf\b"),
        ("pipe_to_shell_hint", r"\|\s*(?:sh|bash)\b"),
    )

    max_len: int = 4000  # Prevent excessive output

    def check(
        self,
        ctx: Context,
        intent: Intent,
        proposal: Proposal,
        tensors: TensorSnapshot,
        memory: MemorySnapshot,
    ) -> Optional[SafetyVerdict]:
        text = proposal.content or ""

        # Length check
        if len(text) > self.max_len:
            return SafetyVerdict(
                decision=Decision.REVISE,
                rule_ids=[self.rule_id],
                reasons=[f"[{self.rule_id}] 出力が長すぎるため要約が必要（len={len(text)}）"],
                required_changes=[f"出力を {self.max_len} 文字以内に要約してください。"],
                meta={"stage": "action", "kind": "length"},
            )

        # Secret patterns check (REJECT)
        for name, pat in self.secret_patterns:
            if re.search(pat, text):
                return SafetyVerdict(
                    decision=Decision.REJECT,
                    rule_ids=[self.rule_id],
                    reasons=[f"[{self.rule_id}] 秘密情報の可能性があるパターンを検出: {name}"],
                    required_changes=["秘密情報・認証情報を出力しないでください。必要ならマスクしてください。"],
                    meta={"stage": "action", "kind": "secret", "match": name},
                )

        # Dangerous execution patterns check (REVISE)
        for name, pat in self.exec_patterns:
            if re.search(pat, text):
                return SafetyVerdict(
                    decision=Decision.REVISE,
                    rule_ids=[self.rule_id],
                    reasons=[f"[{self.rule_id}] 危険な実行につながり得る表現を検出: {name}"],
                    required_changes=[
                        "危険な実行手順に該当する表現を削除/一般化してください。",
                        "安全な代替（例: 注意喚起、原理説明、無害な手順）に置き換えてください。",
                    ],
                    meta={"stage": "action", "kind": "exec", "match": name},
                )

        return None


__all__ = ["DangerousOutputGuardPolicy"]
