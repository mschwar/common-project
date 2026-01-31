"""
Tests for update_index.py script.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from update_index import update_index


def test_update_index_writes_index_and_entries_json(repo_structure, sample_entry_content):
    entry_path = repo_structure / "entries" / "day-002-sample.md"
    entry_path.write_text(sample_entry_content, encoding="utf-8")

    update_index(repo_root=repo_structure)

    index_path = repo_structure / "index.md"
    entries_json_path = repo_structure / "docs" / "entries.json"

    assert index_path.exists()
    assert entries_json_path.exists()

    payload = json.loads(entries_json_path.read_text(encoding="utf-8"))
    assert len(payload) == 1
    assert payload[0]["file"].endswith(".html")
