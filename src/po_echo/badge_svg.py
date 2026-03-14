from __future__ import annotations

from pathlib import Path

from po_echo.badge_style import get_label_config


def generate_svg(badge: dict) -> str:
    config = get_label_config(str(badge.get("label", "")))
    case = str(badge.get("case", "unknown_case"))
    bias_original = float(badge.get("bias_original", 0.0))
    bias_final = float(badge.get("bias_final", 0.0))
    execution = "allowed" if badge.get("execution_allowed", False) else "blocked"
    reasons = badge.get("reasons", [])[:3]
    reason_lines = "".join(
        f'<text x="48" y="{340 + i * 36}" fill="{config["fg"]}" font-size="24">- {reason}</text>'
        for i, reason in enumerate(reasons)
    )

    return f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"630\" viewBox=\"0 0 1200 630\">
  <rect width=\"1200\" height=\"630\" fill=\"{config['bg']}\"/>
  <rect x=\"38\" y=\"38\" width=\"1124\" height=\"554\" rx=\"24\" fill=\"none\" stroke=\"{config['accent']}\" stroke-width=\"4\"/>
  <text x=\"48\" y=\"96\" fill=\"{config['fg']}\" font-size=\"40\" font-family=\"Arial, sans-serif\">Project Echo</text>
  <text x=\"48\" y=\"150\" fill=\"{config['accent']}\" font-size=\"56\" font-weight=\"700\" font-family=\"Arial, sans-serif\">{config['display']}</text>
  <text x=\"48\" y=\"200\" fill=\"{config['fg']}\" font-size=\"30\" font-family=\"Arial, sans-serif\">{config['pig_state']}  case: {case}</text>
  <text x=\"48\" y=\"250\" fill=\"{config['fg']}\" font-size=\"28\" font-family=\"Arial, sans-serif\">Bias: {bias_original:.2f} -&gt; {bias_final:.2f}</text>
  <text x=\"48\" y=\"290\" fill=\"{config['fg']}\" font-size=\"28\" font-family=\"Arial, sans-serif\">Execution: {execution}</text>
  {reason_lines}
</svg>
"""


def write_svg(badge: dict, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(generate_svg(badge), encoding="utf-8")
    return out_path
