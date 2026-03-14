from __future__ import annotations

import json
from pathlib import Path

from tools.build_x_pack import (
    render_thread_variants,
    summarize_case,
    write_pack,
)
from po_echo.badge_svg import write_svg


def _demo_data() -> dict:
    return {
        "badge": {
            "case": "high_bias_affiliate",
            "label": "ECHO_BLOCKED",
            "bias_original": 0.9,
            "bias_final": 0.3,
            "execution_allowed": False,
            "requires_human_confirm": True,
            "reasons": ["r1", "r2"],
        },
        "audit": {"verify_command": "po-cosmic verify runs/high_bias_affiliate.badge.json"},
        "content": {
            "headline": "h",
            "hook": "k",
            "cta": "c",
            "tags": ["#AI"],
        },
    }


def test_thread_variant_selection_matches_actual_label(tmp_path: Path) -> None:
    data = _demo_data()
    summary = summarize_case("high_bias_affiliate", data, "https://example.com/repo")
    variants = render_thread_variants(summary, data["content"])
    out = write_pack(
        "high_bias_affiliate",
        summary,
        data["badge"],
        variants,
        "checklist",
        tmp_path,
        font_path=None,
        skip_card=True,
        copy_assets=False,
    )
    assert (out / "thread.md").read_text(encoding="utf-8") == variants["thread.blocked.md"]


def test_meta_json_generation(tmp_path: Path) -> None:
    data = _demo_data()
    summary = summarize_case("high_bias_affiliate", data, "https://example.com/repo")
    variants = render_thread_variants(summary, data["content"])
    out = write_pack(
        "high_bias_affiliate",
        summary,
        data["badge"],
        variants,
        "checklist",
        tmp_path,
        font_path=None,
        skip_card=True,
        copy_assets=False,
    )
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    assert meta["actual_label"] == "ECHO_BLOCKED"
    assert meta["verify_command"].startswith("po-cosmic verify")


def test_skip_card_pack_generation(tmp_path: Path) -> None:
    data = _demo_data()
    summary = summarize_case("high_bias_affiliate", data, "https://example.com/repo")
    variants = render_thread_variants(summary, data["content"])
    out = write_pack(
        "high_bias_affiliate",
        summary,
        data["badge"],
        variants,
        "checklist",
        tmp_path,
        font_path=None,
        skip_card=True,
        copy_assets=False,
    )
    assert (out / "thread.check.md").exists()
    assert not (out / "card.png").exists()


def test_badge_svg_generation_from_badge_json(tmp_path: Path) -> None:
    badge = _demo_data()["badge"]
    out = tmp_path / "badge.svg"
    write_svg(badge, out)
    text = out.read_text(encoding="utf-8")
    assert "ECHO BLOCKED" in text
