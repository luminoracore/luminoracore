"""
Snapshot command for LuminoraCore CLI

Export and import personality snapshots.
"""

import click
import json
from pathlib import Path
from datetime import datetime


@click.group()
def snapshot():
    """Snapshot operations (export/import personality states)"""
    pass


@snapshot.command()
@click.argument('session_id')
@click.option('--output', '-o', help='Output file path')
@click.option('--include-history/--no-history', default=True, help='Include conversation history')
@click.option('--include-embeddings/--no-embeddings', default=False, help='Include embeddings')
def export(session_id, output, include_history, include_embeddings):
    """
    Export personality snapshot
    
    Examples:
        luminora-cli snapshot export session123
        luminora-cli snapshot export session123 -o backup.json
        luminora-cli snapshot export session123 --no-history
    """
    # Generate output filename if not provided
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"snapshot_{session_id}_{timestamp}.json"
    
    click.echo(f"\n📦 Exporting snapshot...")
    click.echo(f"   Session: {session_id}")
    click.echo(f"   Output: {output}")
    click.echo(f"   Include history: {include_history}")
    click.echo(f"   Include embeddings: {include_embeddings}")
    
    # Placeholder - would use SDK
    snapshot_data = {
        "_snapshot_info": {
            "created_at": datetime.now().isoformat(),
            "session_id": session_id,
            "template_name": "alicia",
            "total_messages": 150
        },
        "current_state": {
            "affinity": {"points": 50, "level": "friend"},
            "learned_facts": [],
            "memorable_episodes": []
        }
    }
    
    # Save to file
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(snapshot_data, f, indent=2, ensure_ascii=False)
    
    click.echo(f"\n✅ Snapshot exported successfully!")
    click.echo(f"   File: {output_path.absolute()}")


@snapshot.command()
@click.argument('snapshot_file', type=click.Path(exists=True))
@click.option('--user-id', required=True, help='User ID to associate with')
@click.option('--restore-history/--no-history', default=False, help='Restore conversation history')
def import_cmd(snapshot_file, user_id, restore_history):
    """
    Import personality snapshot
    
    Examples:
        luminora-cli snapshot import backup.json --user-id user123
        luminora-cli snapshot import backup.json --user-id user123 --restore-history
    """
    click.echo(f"\n📥 Importing snapshot...")
    click.echo(f"   File: {snapshot_file}")
    click.echo(f"   User ID: {user_id}")
    click.echo(f"   Restore history: {restore_history}")
    
    # Load snapshot
    with open(snapshot_file, 'r', encoding='utf-8') as f:
        snapshot_data = json.load(f)
    
    # Validate
    if "_snapshot_info" not in snapshot_data:
        click.echo("❌ Error: Invalid snapshot file (missing _snapshot_info)", err=True)
        sys.exit(1)
    
    # Placeholder - would use SDK
    new_session_id = f"session_{datetime.now().timestamp()}"
    
    click.echo(f"\n✅ Snapshot imported successfully!")
    click.echo(f"   New session ID: {new_session_id}")
    click.echo(f"   Template: {snapshot_data['_snapshot_info'].get('template_name', 'unknown')}")


@snapshot.command()
def list():
    """
    List available snapshots
    
    Examples:
        luminora-cli snapshot list
    """
    click.echo("\n📂 Available snapshots:")
    
    # Find snapshot files in current directory
    snapshot_files = list(Path(".").glob("snapshot_*.json"))
    
    if not snapshot_files:
        click.echo("   No snapshots found in current directory")
    else:
        for file in sorted(snapshot_files):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    info = data.get("_snapshot_info", {})
                    click.echo(f"\n   📄 {file.name}")
                    click.echo(f"      Session: {info.get('session_id', 'unknown')}")
                    click.echo(f"      Created: {info.get('created_at', 'unknown')}")
                    click.echo(f"      Template: {info.get('template_name', 'unknown')}")
            except:
                click.echo(f"\n   ⚠️  {file.name} (invalid format)")


if __name__ == '__main__':
    snapshot()

