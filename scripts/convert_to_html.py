#!/usr/bin/env python3
"""
Convert markdown entries to HTML for GitHub Pages.
Reads entries from /entries/ and generates HTML files in /docs/entries/
"""

import html
import re
from typing import List

from utils import extract_metadata, get_repo_root


REPO_ROOT = get_repo_root()
TEMPLATE_PATH = REPO_ROOT / "templates" / "entry.html"
HTML_TEMPLATE = TEMPLATE_PATH.read_text(encoding="utf-8")


def _wrap_paragraphs(content: str) -> str:
    """Wrap plain text blocks in paragraph tags."""
    blocks = [b.strip() for b in content.split('\n\n') if b.strip()]
    rendered: List[str] = []
    for block in blocks:
        if block.startswith('<ul>') or block.startswith('<ol>') or block.startswith('<h'):
            rendered.append(block)
        else:
            rendered.append(f'<p>{block}</p>')
    return '\n'.join(rendered)


def markdown_to_html(md_content: str) -> str:
    """Convert markdown content to HTML sections."""

    md_content = html.escape(md_content)

    # Split by H2 headings
    sections = re.split(r'\n## ', md_content)
    
    html_parts = []
    
    for i, section in enumerate(sections):
        if i == 0:  # Skip the first title (H1)
            continue
            
        lines = section.split('\n', 1)
        heading = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        
        # Determine section class
        section_class = "section"
        if "connection" in heading.lower():
            section_class += " connections"
        elif "exercise" in heading.lower():
            section_class += " exercise"
        
        # Convert basic markdown
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)

        # Convert bullet lists
        content = re.sub(r'^\- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
        content = re.sub(r'(?:<li>.*</li>\n?)+', lambda m: f"<ul>{m.group(0)}</ul>", content, flags=re.DOTALL)

        # Convert paragraphs
        content = _wrap_paragraphs(content)
        
        html_parts.append(f'<div class="{section_class}"><h2>{heading}</h2>{content}</div>')
    
    return '\n'.join(html_parts)


def convert_all_entries() -> None:
    """Convert all markdown entries to HTML."""

    repo_root = get_repo_root()
    entries_dir = repo_root / 'entries'
    docs_entries_dir = repo_root / 'docs' / 'entries'
    
    docs_entries_dir.mkdir(parents=True, exist_ok=True)
    
    converted = 0
    
    for md_file in sorted(entries_dir.glob('day-*.md')):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = extract_metadata(content)
        content_html = markdown_to_html(content)
        
        # Generate HTML
        html = HTML_TEMPLATE.format(
            title=metadata['title'],
            description=metadata['description'],
            theme=metadata['theme'],
            day_padded=str(metadata['day']).zfill(3),
            content_html=content_html
        )
        
        # Write HTML file
        html_filename = md_file.stem + '.html'
        html_path = docs_entries_dir / html_filename

        if html_path.exists():
            if html_path.stat().st_mtime >= md_file.stat().st_mtime:
                print(f"⏩ Skipped (unchanged): {md_file.name}")
                continue

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

        converted += 1
        print(f"✅ Converted: {md_file.name} → {html_filename}")
    
    print(f"\n🎉 Total converted: {converted} entries")


if __name__ == "__main__":
    convert_all_entries()
