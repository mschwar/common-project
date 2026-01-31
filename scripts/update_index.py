#!/usr/bin/env python3
"""
Update index.md with all generated entries.

This script scans the /entries/ directory for markdown files and rebuilds
the master index with thematic groupings and connection maps.

Usage:
    python update_index.py

The script will:
- Scan all day-*.md files in /entries/
- Extract metadata from each entry
- Generate index.md with:
  - Progress tracking
  - Alphabetical listing
  - Thematic grouping
  - Connection map

Example:
    python update_index.py
    # Output: ✅ Index updated! 5 entries indexed.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Import shared utilities
import sys

from utils import extract_metadata, get_repo_root

REPO_ROOT = get_repo_root()
sys.path.insert(0, str(REPO_ROOT))
import config  # noqa: E402


def _load_tracking(tracking_path: Path) -> Dict[str, Any]:
    """Load tracking metadata from tracking.json."""
    with open(tracking_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _scan_entries(entries_dir: Path) -> List[Dict[str, Any]]:
    """Scan entry markdown files and extract metadata."""
    entries: List[Dict[str, Any]] = []
    for entry_file in sorted(entries_dir.glob('day-*.md')):
        try:
            with open(entry_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"⚠️  Warning: Could not read {entry_file.name}: {e}")
            continue

        day_match = re.search(r'day-(\d{3})', entry_file.name)
        day_num = int(day_match.group(1)) if day_match else 0

        metadata = extract_metadata(content)
        metadata['day'] = day_num
        metadata['filename'] = entry_file.name

        entries.append(metadata)

    return entries


def _group_by_theme(entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group entry metadata by theme."""
    themes: Dict[str, List[Dict[str, Any]]] = {}
    for entry in entries:
        theme = entry['theme']
        themes.setdefault(theme, []).append(entry)
    return themes


def _render_index(entries: List[Dict[str, Any]], themes: Dict[str, List[Dict[str, Any]]], total_concepts: int) -> str:
    """Render index.md content from entries and themes."""
    completed = len(entries)
    index_content = f"""# Common Projects Index

**Progress**: {completed} of {total_concepts} concepts completed

## All Concepts

"""

    for entry in sorted(entries, key=lambda x: x['day']):
        rel_path = f"entries/{entry['filename']}"
        index_content += f"- [Day {entry['day']}: {entry['title']}]({rel_path}) *({entry['theme']})*\n"

    index_content += "\n---\n\n## By Theme\n\n"

    for theme in sorted(themes.keys()):
        index_content += f"### {theme}\n"
        for entry in sorted(themes[theme], key=lambda x: x['day']):
            rel_path = f"entries/{entry['filename']}"
            index_content += f"- [Day {entry['day']}: {entry['title']}]({rel_path})\n"
        index_content += "\n"

    index_content += "---\n\n## Connection Map\n\n"

    for entry in sorted(entries, key=lambda x: x['day']):
        if entry.get('connections'):
            conn_str = ', '.join([f"Day {c}" for c in entry['connections']])
            index_content += f"- **Day {entry['day']}**: {entry['title']} → {conn_str}\n"

    index_content += f"\n---\n\n*Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n"
    return index_content


def _write_entries_json(entries: List[Dict[str, Any]], docs_dir: Path) -> None:
    """Write docs/entries.json for the web UI."""
    docs_dir.mkdir(parents=True, exist_ok=True)
    payload = []
    for entry in entries:
        payload.append({
            "day": entry["day"],
            "title": entry["title"],
            "theme": entry["theme"],
            "file": entry["filename"].replace(".md", ".html"),
            "excerpt": entry.get("description", "")
        })

    entries_json_path = docs_dir / "entries.json"
    with open(entries_json_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def update_index(repo_root: Path | None = None) -> None:
    """
    Scan entries directory and rebuild index.md with current content.
    
    This function:
    1. Loads tracking.json for metadata
    2. Scans all day-*.md files
    3. Extracts metadata from each
    4. Groups entries by theme
    5. Generates formatted index.md
    6. Writes updated index file
    
    Raises:
        FileNotFoundError: If required files/directories don't exist
        json.JSONDecodeError: If tracking.json is malformed
        
    Side Effects:
        - Writes to index.md
        - Prints progress to stdout
    """
    try:
        repo_root = get_repo_root() if repo_root is None else repo_root
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return
    
    entries_dir = repo_root / 'entries'
    index_path = repo_root / 'index.md'
    tracking_path = repo_root / 'tracking.json'
    docs_dir = repo_root / 'docs'
    
    # Validate paths exist
    if not entries_dir.exists():
        print(f"❌ Error: Entries directory not found: {entries_dir}")
        return
    
    if not tracking_path.exists():
        print(f"❌ Error: Tracking file not found: {tracking_path}")
        return
    
    try:
        tracking = _load_tracking(tracking_path)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing tracking.json: {e}")
        return

    entries = _scan_entries(entries_dir)
    themes = _group_by_theme(entries)
    total_concepts = tracking.get('metadata', {}).get('total_concepts', config.TOTAL_CONCEPTS)
    index_content = _render_index(entries, themes, total_concepts)
    completed = len(entries)
    
    # Write index
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
    except OSError as e:
        print(f"❌ Error writing index.md: {e}")
        return

    _write_entries_json(entries, docs_dir)
    
    print(f"✅ Index updated! {completed} entries indexed.")
    print(f"📊 Themes: {', '.join(sorted(themes.keys()))}")


def main() -> int:
    """
    Main entry point for the index update script.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        update_index()
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
