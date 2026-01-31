"""
Integration tests for entry validation script.

Tests the validate_entry.py script with real and mock entry files.

Run with:
    pytest tests/test_validate_entry.py -v
"""

import pytest
from pathlib import Path
import sys
import tempfile

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validate_entry import validate_entry, REQUIRED_SECTIONS


class TestValidateEntry:
    """Test entry validation functionality."""
    
    def test_valid_entry(self, tmp_path):
        """Test validation of a compliant entry."""
        entry_content = """# Probability Basics

## Kindergarten Explanation

Imagine you have a coin in your hand. When you flip it, it can land on heads or tails.
But which one? You can't know for sure before you flip it! That's where probability comes in.

Think of it this way: You have a jar with 10 marbles—5 red and 5 blue. Close your eyes
and pick one. What color will it be? You don't know yet, but you DO know you have a 50%
chance of getting red and a 50% chance of getting blue.

Here's the trick: probability isn't magic or fortune-telling. It's organized counting.
If there are 4 possible outcomes and all are equally likely, each one has a 1-in-4 chance.

## Why It Matters

Probability helps you make smarter decisions every day.

## Connections Unlocked

-  **Builds on**: Day 2: Bayesian Statistics
- **Leads to**: Day 15: Game Theory

## Quick Exercise

What's the probability you'll eat pizza this week?

---

**Theme**: Statistics  
**Day**: 001
"""
        # Create temporary file
        entry_file = tmp_path / "day-001-probability-basics.md"
        entry_file.write_text(entry_content, encoding='utf-8')
        
        success, errors, warnings = validate_entry(str(entry_file))
        
        assert success is True
        assert len(errors) == 0
    
    def test_missing_section(self, tmp_path):
        """Test detection of missing required section."""
        entry_content = """# Test Title

## Kindergarten Explanation

Content here.

## Why It Matters

Reason here.
"""
        entry_file = tmp_path / "day-001-test.md"
        entry_file.write_text(entry_content, encoding='utf-8')
        
        success, errors, warnings = validate_entry(str(entry_file))
        
        assert success is False
        assert any("Connections" in error for error in errors)
    
    def test_missing_title(self, tmp_path):
        """Test detection of missing H1 title."""
        entry_content = """## Kindergarten Explanation

Content without title.

## Why It Matters

Reason.

## Connections

Links.

## Exercise

Task.
"""
        entry_file = tmp_path / "day-001-test.md"
        entry_file.write_text(entry_content, encoding='utf-8')
        
        success, errors, warnings = validate_entry(str(entry_file))
        
        assert success is False
        assert any("title" in error.lower() for error in errors)
    
    def test_low_word_count(self, tmp_path):
        """Test warning for low word count."""
        entry_content = """# Short Entry

## Kindergarten Explanation

Too short.

## Why It Matters

Brief.

## Connections

- Day 1

## Exercise

Quick task.
"""
        entry_file = tmp_path / "day-001-short.md"
        entry_file.write_text(entry_content, encoding='utf-8')
        
        success, errors, warnings = validate_entry(str(entry_file))
        
        # Should succeed but with warnings
        assert len(errors) == 0
        assert any("word count" in warning.lower() for warning in warnings)
    
    def test_invalid_filename(self, tmp_path):
        """Test warning for non-standard filename."""
        entry_content = """# Test

## Kindergarten Explanation

Content here with enough words to pass the word count check.
More content to make it longer. Even more words here.
And some additional text to reach the minimum.

## Why It Matters

Reason here.

## Connections

- Day 1

## Exercise

Task description.
"""
        # Non-standard filename
        entry_file = tmp_path / "invalid-name.md"
        entry_file.write_text(entry_content, encoding='utf-8')
        
        success, errors, warnings = validate_entry(str(entry_file))
        
        assert any("convention" in warning.lower() for warning in warnings)
    
    def test_file_not_found(self):
        """Test error handling for non-existent file."""
        success, errors, warnings = validate_entry("/nonexistent/file.md")
        
        assert success is False
        assert len(errors) == 1
        assert "not found" in errors[0].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
