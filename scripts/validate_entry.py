#!/usr/bin/env python3
"""
Validate entry format andcontent for Common Projects.

This script checks markdown entry files for compliance with the Common Projects
format guidelines, including section structure, word count, and naming conventions.

Usage:
    python validate_entry.py <entry_file_path>

Example:
    python validate_entry.py entries/day-001-probability-basics.md

Exit Codes:
    0: All validation checks passed
    1: Validation errors found
"""

import sys
import re
from pathlib import Path
from typing import Tuple, List

# Import shared utilities
from utils import validate_section_presence, count_words, get_repo_root


REPO_ROOT = get_repo_root()
sys.path.insert(0, str(REPO_ROOT))
import config  # noqa: E402

# Validation constants (centralized in config)
REQUIRED_SECTIONS = config.REQUIRED_SECTIONS
MIN_WORD_COUNT = config.MIN_WORD_COUNT
RECOMMENDED_MAX_WORD_COUNT = config.RECOMMENDED_MAX_WORD_COUNT
FILENAME_PATTERN = config.ENTRY_FILENAME_PATTERN


def _load_content(file_path: Path) -> str:
    """Load file content as UTF-8 text."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def _validate_sections(content: str) -> List[str]:
    """Return error messages for missing required sections."""
    missing = validate_section_presence(content, REQUIRED_SECTIONS)
    return [f"Missing section: {section}" for section in missing]


def _validate_word_count(content: str) -> List[str]:
    """Return warning messages for out-of-range word counts."""
    warnings: List[str] = []
    word_count = count_words(content)
    if word_count < MIN_WORD_COUNT:
        warnings.append(
            f"Word count ({word_count}) below recommended minimum ({MIN_WORD_COUNT})"
        )
    elif word_count > RECOMMENDED_MAX_WORD_COUNT:
        warnings.append(
            f"Word count ({word_count}) above recommended maximum ({RECOMMENDED_MAX_WORD_COUNT})"
        )
    return warnings


def _validate_title(content: str) -> List[str]:
    """Return error messages if H1 title is missing."""
    if not re.search(r'^#\s+.+', content, re.MULTILINE):
        return ["Missing title (H1 heading)"]
    return []


def _validate_filename(filename: str) -> List[str]:
    """Return warning messages for nonconforming filenames."""
    if not re.match(FILENAME_PATTERN, filename):
        return [f"Filename doesn't follow convention: {FILENAME_PATTERN}"]
    return []


def _validate_connections(content: str) -> List[str]:
    """Return warning messages if connections section lacks references."""
    warnings: List[str] = []
    connection_pattern = r'\b(Builds on|Leads to|Related)\b'
    if not re.search(connection_pattern, content, re.IGNORECASE):
        warnings.append("No clear connections to other concepts found")
    return warnings


def validate_entry(file_path: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate that an entry follows all Common Projects guidelines.
    
    Checks performed:
    - File existence
    - Required section presence
    - Word count (200-500 recommended)
    - H1 title presence
    - Filename convention (day-XXX-title.md)
    - Connection references
    
    Args:
        file_path: Path to the markdown entry file to validate
        
    Returns:
        Tuple containing:
            - success (bool): True if no errors, False otherwise
            - errors (list[str]): List of error messages
            - warnings (list[str]): List of warning messages
            
    Example:
        >>> success, errors, warnings = validate_entry("entries/day-001-probability.md")
        >>> if not success:
        ...     print(f"Errors: {errors}")
    """
    errors: List[str] = []
    warnings: List[str] = []
    
    # Check file exists
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        return False, [f"File not found: {file_path}"], []
    
    # Read file content
    content = _load_content(file_path_obj)
    
    # 1. Check required sections
    errors.extend(_validate_sections(content))
    
    # 2. Word count validation
    warnings.extend(_validate_word_count(content))
    
    # 3. Check for H1 title
    errors.extend(_validate_title(content))
    
    # 4. Filename convention
    filename = file_path_obj.name
    warnings.extend(_validate_filename(filename))
    
    # 5. Check for connections (using proper regex)
    warnings.extend(_validate_connections(content))
    
    # Print results
    print(f"\n{'='*60}")
    print(f"Validating: {filename}")
    print(f"{'='*60}")
    print(f"Word count: {word_count}")
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("\n✅ All validation checks passed!")
    elif not errors:
        print("\n✅ No errors, but please review warnings.")
    
    print(f"{'='*60}\n")
    
    return len(errors) == 0, errors, warnings


def main() -> int:
    """
    Main entry point for the validation script.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    if len(sys.argv) < 2:
        print("Usage: python validate_entry.py <entry_file_path>")
        print("\nExample:")
        print("  python validate_entry.py entries/day-001-probability-basics.md")
        return 1
    
    file_path = sys.argv[1]
    success, errors, warnings = validate_entry(file_path)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
