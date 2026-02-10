"""
Migration Utility: JSON to Database
====================================

Migrate existing JSON-based Po_trace data to database
"""

from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from po_core.po_trace import PoTrace
from po_core.po_trace_db import PoTraceDB

console = Console()


def migrate_json_to_db(
    json_storage_dir: Optional[Path] = None,
    db_url: Optional[str] = None,
    verbose: bool = False,
) -> dict:
    """
    Migrate JSON-based Po_trace data to database.

    Args:
        json_storage_dir: JSON storage directory (default: ~/.po_core/traces)
        db_url: Database URL (default: SQLite in ~/.po_core/po_trace.db)
        verbose: Show detailed progress

    Returns:
        Migration statistics
    """
    # Initialize source and target
    json_trace = PoTrace(storage_dir=json_storage_dir)
    db_trace = PoTraceDB(db_url=db_url)

    # Get all sessions from JSON
    sessions_list = json_trace.list_sessions()

    stats = {
        "total_sessions": len(sessions_list),
        "migrated_sessions": 0,
        "total_events": 0,
        "total_metrics": 0,
        "errors": 0,
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"[cyan]Migrating {stats['total_sessions']} sessions...",
            total=stats["total_sessions"],
        )

        for session_meta in sessions_list:
            session_id = session_meta["session_id"]

            try:
                # Load full session from JSON
                session = json_trace.get_session(session_id)
                if session is None:
                    if verbose:
                        console.print(
                            f"[yellow]Warning: Session {session_id} not found[/yellow]"
                        )
                    stats["errors"] += 1
                    continue

                # Create session in database
                db_trace.db.create_session(
                    session_id=session.session_id,
                    prompt=session.prompt,
                    philosophers=session.philosophers,
                    metadata=session.metadata,
                )

                # Migrate events
                for event in session.events:
                    db_trace.db.add_event(
                        event_id=event.event_id,
                        session_id=event.session_id,
                        event_type=event.event_type.value,
                        source=event.source,
                        data=event.data,
                        metadata=event.metadata,
                    )
                    stats["total_events"] += 1

                # Migrate metrics
                if session.metrics:
                    db_trace.update_metrics(session.session_id, session.metrics)
                    stats["total_metrics"] += len(session.metrics)

                stats["migrated_sessions"] += 1

                if verbose:
                    console.print(
                        f"[green]✓[/green] Migrated session {session_id[:8]}... "
                        f"({len(session.events)} events, {len(session.metrics)} metrics)"
                    )

            except Exception as e:
                stats["errors"] += 1
                if verbose:
                    console.print(
                        f"[red]✗[/red] Error migrating session {session_id}: {e}"
                    )

            progress.update(task, advance=1)

    return stats


@click.command()
@click.option(
    "--json-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="JSON storage directory (default: ~/.po_core/traces)",
)
@click.option("--db-url", type=str, help="Database URL (default: SQLite)")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed progress")
@click.option("--verify", is_flag=True, help="Verify migration after completion")
def migrate(
    json_dir: Optional[Path], db_url: Optional[str], verbose: bool, verify: bool
) -> None:
    """Migrate Po_trace data from JSON to database."""
    console.print("\n[bold cyan]Po_trace Migration: JSON → Database[/bold cyan]\n")

    # Run migration
    stats = migrate_json_to_db(
        json_storage_dir=json_dir, db_url=db_url, verbose=verbose
    )

    # Display results
    console.print("\n[bold green]Migration Complete![/bold green]\n")
    console.print(f"  Total sessions found:  {stats['total_sessions']}")
    console.print(f"  Successfully migrated: {stats['migrated_sessions']}")
    console.print(f"  Total events:          {stats['total_events']}")
    console.print(f"  Total metrics:         {stats['total_metrics']}")

    if stats["errors"] > 0:
        console.print(f"  [yellow]Errors:                {stats['errors']}[/yellow]")

    # Verification
    if verify:
        console.print("\n[bold cyan]Verifying migration...[/bold cyan]")
        db_trace = PoTraceDB(db_url=db_url)
        db_stats = db_trace.get_statistics()

        console.print(f"  Database sessions: {db_stats['total_sessions']}")
        console.print(f"  Database events:   {db_stats['total_events']}")

        if db_stats["total_sessions"] == stats["migrated_sessions"]:
            console.print("[bold green]✓ Verification passed![/bold green]")
        else:
            console.print(
                "[bold red]✗ Verification failed: Session count mismatch[/bold red]"
            )


if __name__ == "__main__":
    migrate()
