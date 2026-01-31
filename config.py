# Configuration file for Common Projects
# This file contains centralized settings used across scripts

# File Paths
ENTRIES_DIR = "entries"
DOCS_DIR = "docs"
SCRIPTS_DIR = "scripts"
TEMPLATES_DIR = "templates"

# Entry Validation
MIN_WORD_COUNT = 200
RECOMMENDED_MAX_WORD_COUNT = 500
REQUIRED_SECTIONS = [
    "Kindergarten Explanation",
    "Why It Matters",
    "Connections",
    "Exercise"
]

# Project Constants
TOTAL_CONCEPTS = 50

# File Patterns
ENTRY_FILENAME_PATTERN = r"day-\d{3}-.+\.md"

# Animation Timing (JavaScript - documented here for reference)
PROGRESS_ANIMATION_DELAY = 500  # milliseconds
CARD_ANIMATION_STAGGER = 100    # milliseconds
