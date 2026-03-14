#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

CASES = ["high_bias_affiliate", "mixed_contaminated", "clean_multi_merchant"]
THREAD_BY_LABEL = {
    "ECHO_BLOCKED": "thread.blocked.md",
    "ECHO_CHECK": "thread.check.md",
    "ECHO_VERIFIED": "thread.verified.md",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build X runway distribution pack")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--case", choices=CASES)
    g.add_argument("--all", action="store_true")
    p.add_argument("--repo-url", required=True)
    p.add_argument("--out-dir", type=Path, default=Path("dist/x"))
    p.add_argument("--font-path", type=Path, default=None)
    p.add_argument("--skip-card", action="store_true")
    p.add_argument("--copy-assets", dest="copy_assets", action="store_true", default=True)
    p.add_argument("--no-copy-assets", dest="copy_assets", action="store_false")
    return p.parse_args()


def load_case_inputs(case: str) -> dict[str, Any]:
    badge_path = ROOT / "runs" / f"{case}.badge.json"
    audit_path = ROOT / "runs" / f"{case}.audit.json"
    content_path = ROOT / "content" / "x_cases" / f"{case}.json"
    missing = [str(p) for p in [badge_path, audit_path, content_path] if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required inputs: " + ", ".join(missing) + ". Try `make x-assets` first."
        )
    return {
        "badge": json.loads(badge_path.read_text(encoding="utf-8")),
        "audit": json.loads(audit_path.read_text(encoding="utf-8")),
        "content": json.loads(content_path.read_text(encoding="utf-8")),
    }


def summarize_case(case: str, data: dict[str, Any], repo_url: str) -> dict[str, Any]:
    badge = data["badge"]
    from po_echo.badge_style import PIG_STATE_BY_LABEL, normalize_label

    label = normalize_label(str(badge.get("label", "")))
    verify_command = data["audit"].get(
        "verify_command", f"po-cosmic verify runs/{case}.badge.json"
    )
    return {
        "case": case,
        "actual_label": label,
        "available_thread_variants": [
            "thread.blocked.md",
            "thread.check.md",
            "thread.verified.md",
        ],
        "pig_state": PIG_STATE_BY_LABEL[label],
        "bias_original": float(badge.get("bias_original", 0.0)),
        "bias_final": float(badge.get("bias_final", 0.0)),
        "execution_allowed": bool(badge.get("execution_allowed", False)),
        "requires_human_confirm": bool(badge.get("requires_human_confirm", False)),
        "reasons": list(badge.get("reasons", [])),
        "repo_url": repo_url,
        "verify_command": str(verify_command),
    }


def _render_template(template_path: Path, context: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, value in context.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def render_thread_variants(summary: dict[str, Any], content: dict[str, Any]) -> dict[str, str]:
    reasons = "\n".join(f"- {item}" for item in summary["reasons"])
    context = {
        "case": summary["case"],
        "headline": content["headline"],
        "hook": content["hook"],
        "cta": content["cta"],
        "label": summary["actual_label"],
        "pig_state": summary["pig_state"],
        "bias_original": f"{summary['bias_original']:.2f}",
        "bias_final": f"{summary['bias_final']:.2f}",
        "execution_allowed": "allowed" if summary["execution_allowed"] else "blocked",
        "requires_human_confirm": "yes" if summary["requires_human_confirm"] else "no",
        "reasons": reasons,
        "repo_url": summary["repo_url"],
        "verify_command": summary["verify_command"],
        "tags": " ".join(content.get("tags", [])),
    }
    templates = {
        "thread.blocked.md": ROOT / "content" / "templates" / "x_thread_blocked.md.tmpl",
        "thread.check.md": ROOT / "content" / "templates" / "x_thread_check.md.tmpl",
        "thread.verified.md": ROOT / "content" / "templates" / "x_thread_verified.md.tmpl",
    }
    return {name: _render_template(path, context) for name, path in templates.items()}


def render_checklist(summary: dict[str, Any]) -> str:
    return _render_template(
        ROOT / "content" / "templates" / "x_checklist.md.tmpl",
        {
            "case": summary["case"],
            "repo_url": summary["repo_url"],
            "verify_command": summary["verify_command"],
        },
    )


def render_card_png(summary: dict[str, Any], out_path: Path, font_path: Path | None = None) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception as exc:
        raise RuntimeError(
            "Pillow is required for card generation. Use --skip-card to continue without image output."
        ) from exc

    from po_echo.badge_style import get_label_config

    cfg = get_label_config(summary["actual_label"])
    img = Image.new("RGB", (1600, 900), cfg["bg"])
    draw = ImageDraw.Draw(img)

    def _font(size: int):
        if font_path:
            try:
                return ImageFont.truetype(str(font_path), size)
            except Exception:
                pass
        return ImageFont.load_default()

    draw.text((60, 60), "Project Echo", fill=cfg["fg"], font=_font(60))
    draw.text((60, 130), cfg["display"], fill=cfg["accent"], font=_font(76))
    draw.text((60, 220), summary["pig_state"], fill=cfg["fg"], font=_font(64))
    draw.text(
        (60, 300),
        f"Bias: {summary['bias_original']:.2f} -> {summary['bias_final']:.2f}",
        fill=cfg["fg"],
        font=_font(44),
    )
    exec_label = "allowed" if summary["execution_allowed"] else "blocked"
    draw.text((60, 360), f"Execution: {exec_label}", fill=cfg["fg"], font=_font(44))
    for i, reason in enumerate(summary["reasons"][:3]):
        draw.text((60, 430 + i * 54), f"- {reason}", fill=cfg["fg"], font=_font(34))
    draw.text((60, 800), "GitHub: project-echo", fill=cfg["fg"], font=_font(30))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)


def _prepare_badge_svg(case: str, badge: dict[str, Any], out_path: Path) -> None:
    from po_echo.badge_svg import write_svg

    src = ROOT / "runs" / f"{case}.badge.svg"
    if src.exists():
        shutil.copy2(src, out_path)
    else:
        write_svg(badge, out_path)


def write_pack(
    case: str,
    summary: dict[str, Any],
    badge: dict[str, Any],
    thread_variants: dict[str, str],
    checklist: str,
    out_dir: Path,
    font_path: Path | None,
    skip_card: bool,
    copy_assets: bool,
) -> Path:
    case_dir = out_dir / case
    case_dir.mkdir(parents=True, exist_ok=True)

    for filename, text in thread_variants.items():
        (case_dir / filename).write_text(text, encoding="utf-8")
    active = THREAD_BY_LABEL[summary["actual_label"]]
    (case_dir / "thread.md").write_text(thread_variants[active], encoding="utf-8")
    (case_dir / "checklist.md").write_text(checklist, encoding="utf-8")
    (case_dir / "meta.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if not skip_card:
        render_card_png(summary, case_dir / "card.png", font_path=font_path)

    if copy_assets:
        _prepare_badge_svg(case, badge, case_dir / "badge.svg")
        gif = ROOT / "assets" / "pig_flying.gif"
        if gif.exists():
            shutil.copy2(gif, case_dir / "pig_flying.gif")
    return case_dir


def main() -> int:
    args = parse_args()
    targets = CASES if args.all else [args.case]
    for case in targets:
        data = load_case_inputs(case)
        summary = summarize_case(case, data, args.repo_url)
        threads = render_thread_variants(summary, data["content"])
        checklist = render_checklist(summary)
        path = write_pack(
            case,
            summary,
            data["badge"],
            threads,
            checklist,
            args.out_dir,
            args.font_path,
            args.skip_card,
            args.copy_assets,
        )
        print(f"generated: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
