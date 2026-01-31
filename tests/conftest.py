"""Test configuration and fixtures for pytest."""

import pytest
from pathlib import Path


@pytest.fixture
def sample_entry_content():
    """Provide sample valid entry content for tests."""
    return """# Example Concept

## Kindergarten Explanation

This is a comprehensive explanation of the concept that meets the minimum
word count requirements. It uses clear analogies and builds understanding
incrementally. More content here to ensure we have enough words for validation.

Additional paragraphs provide depth without losing simplicity. The explanation
walks through the concept step by step, making it accessible to everyone.

## Why It Matters

This concept helps you make better decisions and understand complex patterns in everyday life.

## Connections Unlocked

- **Builds on**: Day 1: Probability Basics  
- **Leads to**: Day 3: Power Laws
- **Related**: Day 10: Another Concept

## Quick Exercise

Think of three examples where this concept appears in your daily life.
Write them down and explain how the concept applies to each.

---

**Theme**: Systems  
**Day**: 002  
**Word Count**: ~150
"""


@pytest.fixture
def repo_structure(tmp_path):
    """Create a temporary repository structure for testing."""
    # Create directories
    (tmp_path / "entries").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "scripts").mkdir()
    
    # Create tracking.json
    tracking_content = """{
  "completed": [],
  "in_progress": null,
  "last_generated": null,
  "last_day_number": 0,
  "connections": {},
  "metadata": {
    "total_concepts": 50,
    "created": "2026-01-31",
    "version": "1.0"
  }
}"""
    (tmp_path / "tracking.json").write_text(tracking_content)
    
    # Create README.md marker
    (tmp_path / "README.md").write_text("# Test Repo")
    
    return tmp_path
