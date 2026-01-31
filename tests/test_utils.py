"""
Unit tests for Common Projects utility functions.

This test suite validates the shared utility functions used across
the project's Python scripts.

Run with:
    pytest tests/test_utils.py -v
"""

import pytest
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from utils import (
    extract_metadata,
    validate_section_presence,
    count_words
)


class TestExtractMetadata:
    """Test metadata extraction from markdown content."""
    
    def test_extract_title(self):
        """Test H1 title extraction."""
        content = "# Probability Basics\n\nSome content"
        meta = extract_metadata(content)
        assert meta['title'] == "Probability Basics"
    
    def test_extract_theme(self):
        """Test theme extraction."""
        content = "# Title\n\n**Theme**: Statistics"
        meta = extract_metadata(content)
        assert meta['theme'] == "Statistics"
    
    def test_default_theme(self):
        """Test default theme when not specified."""
        content = "# Title\n\nNo theme specified"
        meta = extract_metadata(content)
        assert meta['theme'] == "Other"
    
    def test_extract_day(self):
        """Test day number extraction."""
        content = "# Title\n\n**Day**: 005"
        meta = extract_metadata(content)
        assert meta['day'] == 5
    
    def test_extract_connections(self):
        """Test connection extraction."""
        content = """# Title

## Connections

- **Builds on**: Day 1: Previous
- **Leads to**: Day 3: Next
"""
        meta = extract_metadata(content)
        assert 1 in meta['connections']
        assert 3 in meta['connections']
    
    def test_extract_description(self):
        """Test description extraction."""
        content = """# Title

## Kindergarten Explanation

This is a test description that should be extracted.

More content here.
"""
        meta = extract_metadata(content)
        assert "This is a test description" in meta['description']
    
    def test_description_truncation(self):
        """Test that long descriptions are truncated."""
        long_text = "A" * 200
        content = f"""# Title

## Kindergarten Explanation

{long_text}
"""
        meta = extract_metadata(content)
        assert len(meta['description']) <= 153  # 150 + "..."
        assert meta['description'].endswith('...')


class TestValidateSectionPresence:
    """Test section validation."""
    
    def test_all_sections_present(self):
        """Test when all required sections are present."""
        content = """# Title

## Why It Matters

Content

## Connections

Content
"""
        sections = ["Why It Matters", "Connections"]
        missing = validate_section_presence(content, sections)
        assert len(missing) == 0
    
    def test_missing_section(self):
        """Test detection of missing section."""
        content = """# Title

## Why It Matters

Content
"""
        sections = ["Why It Matters", "Connections"]
        missing = validate_section_presence(content, sections)
        assert "Connections" in missing
    
    def test_case_insensitive(self):
        """Test case-insensitive matching."""
        content = """# Title

## why it matters

Content
"""
        sections = ["Why It Matters"]
        missing = validate_section_presence(content, sections)
        assert len(missing) == 0


class TestCountWords:
    """Test word counting functionality."""
    
    def test_simple_text(self):
        """Test counting plaintext."""
        text = "This is a simple test"
        assert count_words(text) == 5
    
    def test_with_bold(self):
        """Test word count with bold formatting."""
        text = "This is **bold text** here"
        assert count_words(text) == 5
    
    def test_with_italic(self):
        """Test word count with italic formatting."""
        text = "This is *italic text* here"
        assert count_words(text) == 5
    
    def test_with_links(self):
        """Test word count with markdown links."""
        text = "Check [this link](http://example.com) out"
        assert count_words(text) == 4
    
    def test_empty_string(self):
        """Test edge case: empty string."""
        assert count_words("") == 0
    
    def test_whitespace_only(self):
        """Test edge case: whitespace only."""
        assert count_words("   \n\t  ") == 0


# Integration tests
class TestIntegration:
    """Integration tests for combined functionality."""
    
    def test_full_entry_metadata(self):
        """Test extracting all metadata from a complete entry."""
        content = """# Example Concept

## Kindergarten Explanation

This is a simple explanation of the concept.

## Why It Matters

It helps you understand things better.

## Connections Unlocked

- **Builds on**: Day 1: Previous Concept
- **Leads to**: Day 3: Next Concept

## Quick Exercise

Try this simple exercise.

---

**Theme**: Systems  
**Day**: 002  
**Word Count**: ~50
"""
        meta = extract_metadata(content)
        
        assert meta['title'] == "Example Concept"
        assert meta['theme'] == "Systems"
        assert meta['day'] == 2
        assert len(meta['connections']) == 2
        assert 1 in meta['connections']
        assert 3 in meta['connections']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
