#!/usr/bin/env python3
"""
Shared utility functions for Common Projects scripts.

This module provides common functionality used across multiple scripts
to avoid code duplication and maintain consistency.
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def _extract_title(content: str) -> str:
    title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    return title_match.group(1).strip() if title_match else ''


def _extract_theme(content: str) -> str:
    theme_match = re.search(r'\*\*Theme\*\*:\s*(.+)', content)
    return theme_match.group(1).strip() if theme_match else 'Other'


def _extract_day(content: str) -> int:
    day_match = re.search(r'\*\*Day\*\*:\s*(\d+)', content)
    return int(day_match.group(1)) if day_match else 0


def _extract_description(content: str) -> str:
    para_match = re.search(
        r'## Kindergarten Explanation\n\n(.+?)(?:\n\n|\n##)',
        content,
        re.DOTALL
    )
    if not para_match:
        return ''

    desc = para_match.group(1).strip()
    return desc[:150] + '...' if len(desc) > 150 else desc


def _extract_connections(content: str) -> List[int]:
    connections_section = re.search(
        r'##\s*Connections.*?(?=##|$)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if not connections_section:
        return []

    day_refs = re.findall(r'\bDay\s+(\d+)\b', connections_section.group(0))
    return [int(d) for d in day_refs]


def extract_metadata(content: str) -> Dict[str, Any]:
    """
    Extract metadata from markdown entry content.
    
    Args:
        content: Raw markdown file content
        
    Returns:
        Dictionary containing:
            - title (str): Concept title from H1 heading
            - theme (str): Theme/category (default: 'Other')
            - day (int): Day number (default: 0)
            - description (str): First paragraph excerpt
            - connections (list[int]): List of related day numbers
            
    Example:
        >>> content = "# Probability\\n\\n**Theme**: Statistics"
        >>> meta = extract_metadata(content)
        >>> meta['title']
        'Probability'
    """
    return {
        'title': _extract_title(content),
        'theme': _extract_theme(content),
        'day': _extract_day(content),
        'description': _extract_description(content),
        'connections': _extract_connections(content)
    }


def validate_section_presence(content: str, sections: List[str]) -> List[str]:
    """
    Check if required sections are present in markdown content.
    
    Args:
        content: Markdown file content
        sections: List of required section names (case-insensitive)
        
    Returns:
        List of missing section names (empty if all present)
        
    Example:
        >>> content = "# Title\\n\\n## Why It Matters\\n\\nText"
        >>> validate_section_presence(content, ["Why It Matters", "Connections"])
        ['Connections']
    """
    missing = []
    
    for section in sections:
        # Create regex pattern for case-insensitive section match
        pattern = rf'##\s*{re.escape(section)}'
        if not re.search(pattern, content, re.IGNORECASE):
            missing.append(section)
    
    return missing


def get_repo_root(start_path: Optional[Path] = None) -> Path:
    """
    Find the repository root directory.
    
    Searches upward from the start path until it finds a directory
    containing key repository markers (.git, README.md, etc.)
    
    Args:
        start_path: Starting path for search (default: __file__ location)
        
    Returns:
        Path object pointing to repository root
        
    Raises:
        FileNotFoundError: If repository root cannot be found
    """
    if start_path is None:
        start_path = Path(__file__).parent
    
    current = start_path.resolve()
    
    # Look for repository markers
    markers = ['.git', 'README.md', 'tracking.json', 'entries']
    
    # Search up to 10 levels
    for _ in range(10):
        # Check if any marker exists
        if any((current / marker).exists() for marker in markers):
            return current
        
        # Move up one level
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent
    
    raise FileNotFoundError(
        f"Could not find repository root from {start_path}. "
        f"Ensure script is run from within the repository."
    )


def count_words(text: str) -> int:
    """
    Count words in text, excluding markdown formatting.
    
    Args:
        text: Text content to count
        
    Returns:
        Number of words
    """
    # Remove markdown formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # Split and count
    words = text.split()
    return len(words)


if __name__ == "__main__":
    # Example usage
    sample_content = """# Example Concept

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
    
    print("Testing extract_metadata:")
    meta = extract_metadata(sample_content)
    print(f"  Title: {meta['title']}")
    print(f"  Theme: {meta['theme']}")
    print(f"  Day: {meta['day']}")
    print(f"  Connections: {meta['connections']}")
    print(f"  Description: {meta['description'][:50]}...")
