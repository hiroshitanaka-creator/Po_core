from __future__ import annotations

import argparse
import json
from pathlib import Path


PDF_HEADER = b"%PDF-1.4\n"


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _render_single_page_pdf(lines: list[str]) -> bytes:
    content_lines = ["BT", "/F1 11 Tf", "50 780 Td", "14 TL"]
    for idx, line in enumerate(lines):
        escaped = _escape_pdf_text(line)
        if idx == 0:
            content_lines.append(f"({_escaped_or_blank(escaped)}) Tj")
        else:
            content_lines.append("T*")
            content_lines.append(f"({_escaped_or_blank(escaped)}) Tj")
    content_lines.append("ET")
    stream = "\n".join(content_lines).encode("utf-8")

    objects = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append(b"2 0 obj << /Type /Pages /Count 1 /Kids [3 0 R] >> endobj\n")
    objects.append(
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
    )
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    objects.append(
        f"5 0 obj << /Length {len(stream)} >> stream\n".encode("utf-8")
        + stream
        + b"\nendstream endobj\n"
    )

    body = b""
    offsets = [0]
    for obj in objects:
        offsets.append(len(PDF_HEADER) + len(body))
        body += obj

    xref_start = len(PDF_HEADER) + len(body)
    xref_entries = [b"0000000000 65535 f "]
    for off in offsets[1:]:
        xref_entries.append(f"{off:010d} 00000 n ".encode("utf-8"))
    xref = b"xref\n0 6\n" + b"\n".join(xref_entries) + b"\n"
    trailer = b"trailer << /Size 6 /Root 1 0 R >>\n"
    startxref = f"startxref\n{xref_start}\n%%EOF\n".encode("utf-8")
    return PDF_HEADER + body + xref + trailer + startxref


def _escaped_or_blank(value: str) -> str:
    return value if value else " "


def build_compiled_markdown(paper_source: str, experiment_payload: dict) -> str:
    stats = experiment_payload.get("stats", {})
    lines = [
        paper_source.rstrip(),
        "",
        "## Embedded Experiment Snapshot",
        f"- scenario_count: {stats.get('scenario_count', 0)}",
        f"- golden_count: {stats.get('golden_count', 0)}",
        f"- scenario_digest: {stats.get('scenario_digest', '')}",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build deterministic paper PDF")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--paper", default="docs/paper/paper.md")
    parser.add_argument("--experiments", default="docs/paper/experiments/results_latest.json")
    parser.add_argument("--compiled", default="docs/paper/build/paper_compiled.md")
    parser.add_argument("--pdf", default="docs/paper/build/paper.pdf")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    paper_path = (repo_root / args.paper).resolve()
    experiments_path = (repo_root / args.experiments).resolve()
    compiled_path = (repo_root / args.compiled).resolve()
    pdf_path = (repo_root / args.pdf).resolve()

    paper_source = paper_path.read_text(encoding="utf-8")
    experiment_payload = json.loads(experiments_path.read_text(encoding="utf-8"))

    compiled = build_compiled_markdown(paper_source=paper_source, experiment_payload=experiment_payload)
    compiled_path.parent.mkdir(parents=True, exist_ok=True)
    compiled_path.write_text(compiled, encoding="utf-8")

    preview_lines = [line[:100] for line in compiled.splitlines()[:45]]
    pdf_bytes = _render_single_page_pdf(preview_lines)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.write_bytes(pdf_bytes)


if __name__ == "__main__":
    main()
