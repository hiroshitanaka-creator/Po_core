"""
Po_trace: Reasoning Audit Log Module

Tracks and persists the reasoning process of Po_self,
including aggregate metrics and per-philosopher responses.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from rich.console import Console
from rich.table import Table

from po_core.po_self import PoSelf, PoSelfResponse

console = Console()

# デフォルトのログ保存先（必要なら設定で変えられるようにしてもよい）
DEFAULT_TRACE_DIR = Path("traces")


@dataclass
class TraceHeader:
    """メタ情報：トレースの概要"""

    trace_id: str
    created_at: str
    prompt: str
    philosophers: List[str]
    consensus_leader: Optional[str]
    metrics: Dict[str, float]


@dataclass
class TraceRecord:
    """1つの Po_self 実行結果に対応する完全なトレース"""

    header: TraceHeader
    text: str
    responses: List[Dict[str, Any]]
    log: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        # JSON にそのまま書ける形に落とす
        return {
            "header": asdict(self.header),
            "text": self.text,
            "responses": self.responses,
            "log": self.log,
        }


class PoTrace:
    """Po_self の実行結果をトレースとして保存する責務を持つクラス"""

    def __init__(self, trace_dir: Path | str = DEFAULT_TRACE_DIR) -> None:
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(parents=True, exist_ok=True)

    def build_trace(self, response: PoSelfResponse) -> TraceRecord:
        """PoSelfResponse から TraceRecord を構築する"""

        # trace_id はとりあえずタイムスタンプ＋簡易カウンタみたいなものにしておく
        now = datetime.utcnow()
        trace_id = now.strftime("%Y%m%dT%H%M%S%fZ")
        created_at = now.isoformat() + "Z"

        header = TraceHeader(
            trace_id=trace_id,
            created_at=created_at,
            prompt=response.prompt,
            philosophers=response.philosophers,
            consensus_leader=response.consensus_leader,
            metrics=response.metrics,
        )

        return TraceRecord(
            header=header,
            text=response.text,
            responses=response.responses,
            log=response.log,
        )

    def save_trace(self, record: TraceRecord) -> Path:
        """TraceRecord を JSON ファイルとして保存して、パスを返す"""

        path = self.trace_dir / f"{record.header.trace_id}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(record.to_dict(), f, ensure_ascii=False, indent=2)
        return path


@click.command()
@click.argument("prompt", nargs=-1)
@click.option(
    "--trace-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=DEFAULT_TRACE_DIR,
    help="Directory to store trace JSON files.",
)
def cli(prompt: List[str], trace_dir: Path) -> None:
    """Run the Po_self ensemble and persist a reasoning trace."""

    text_prompt = " ".join(prompt).strip()
    if not text_prompt:
        console.print(
            "[red]No prompt provided.[/red] "
            "Usage: po-core trace \"What is meaning?\""
        )
        raise SystemExit(1)

    console.print("[bold magenta]🧠 Po_self x Po_trace[/bold magenta]")
    console.print(f"[cyan]Prompt:[/cyan] {text_prompt}")

    # 1. Po_self を実行
    po_self = PoSelf()
    response: PoSelfResponse = po_self.generate(text_prompt)

    # 2. トレースを構築・保存
    tracer = PoTrace(trace_dir=trace_dir)
    record = tracer.build_trace(response)
    path = tracer.save_trace(record)

    console.print(
        f"[green]Trace saved:[/green] {path} "
        f"(trace_id={record.header.trace_id})"
    )

    # 3. ついでに要約だけ標準出力に出す
    console.print("\n[bold]Final text:[/bold]")
    console.print(response.text)
    console.print("\n[bold]Metrics:[/bold] " + repr(response.metrics))


if __name__ == "__main__":
    cli()