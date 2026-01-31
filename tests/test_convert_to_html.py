"""
Tests for convert_to_html.py helpers.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from convert_to_html import markdown_to_html


def test_markdown_to_html_escapes_html():
    content = """# Title

## Kindergarten Explanation

Hello <script>alert('x')</script>
"""
    html = markdown_to_html(content)
    assert "&lt;script&gt;" in html


def test_markdown_to_html_lists():
    content = """# Title

## Connections

- Item one
- Item two
"""
    html = markdown_to_html(content)
    assert "<ul>" in html
    assert "<li>Item one</li>" in html
