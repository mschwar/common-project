#!/usr/bin/env python3
"""
Convert markdown entries to HTML for GitHub Pages.
Reads entries from /entries/ and generates HTML files in /docs/entries/
"""

import re
from pathlib import Path
import json


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} - Common Project</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        .entry-content {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        .entry-header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        .day-number {{
            color: var(--accent);
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        .entry-title {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        .theme-badge {{
            display: inline-block;
            background: var(--primary-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
        }}
        .section {{
            background: var(--surface);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border-left: 4px solid var(--primary-color);
        }}
        .section h2 {{
            color: var(--accent);
            margin-bottom: 1rem;
        }}
        .section p {{
            margin-bottom: 1rem;
            line-height: 1.8;
        }}
        .connections {{
            background: var(--background);
        }}
        .connections ul {{
            list-style: none;
            padding: 0;
        }}
        .connections li {{
            margin-bottom: 0.5rem;
            padding-left: 1.5rem;
            position: relative;
        }}
        .connections li:before {{
            content: "→";
            position: absolute;
            left: 0;
            color: var(--accent);
        }}
        .exercise {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-left-color: #fbbf24;
        }}
        .back-link {{
            display: inline-block;
            margin: 2rem 0;
            color: var(--accent);
            text-decoration: none;
            font-weight: 600;
        }}
        .back-link:hover {{
            color: var(--primary-color);
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="../index.html" style="color: inherit; text-decoration: none;">🧠 Common Project</a></h1>
        </div>
    </header>

    <main class="entry-content">
        <a href="../index.html" class="back-link">← Back to all concepts</a>
        
        <div class="entry-header">
            <div class="day-number">Day {day_padded}</div>
            <h1 class="entry-title">{title}</h1>
            <span class="theme-badge">{theme}</span>
        </div>

        {content_html}

        <a href="../index.html" class="back-link">← Back to all concepts</a>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 Matthew Schwartz | MIT License</p>
        </div>
    </footer>
</body>
</html>
"""


def markdown_to_html(md_content):
    """Convert markdown content to HTML sections."""
    
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
        content = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', content, flags=re.DOTALL)
        
        # Convert paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith('<')]
        for para in paragraphs:
            if para:
                content = content.replace(para, f'<p>{para}</p>')
        
        html_parts.append(f'<div class="{section_class}"><h2>{heading}</h2>{content}</div>')
    
    return '\n'.join(html_parts)


def extract_metadata(content):
    """Extract metadata from markdown."""
    
    metadata = {
        'title': '',
        'theme': 'Other',
        'day': 0,
        'description': ''
    }
    
    # Extract title
    title_match = re.search(r'^# (.+)', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    
    # Extract theme
    theme_match = re.search(r'\*\*Theme\*\*:\s*(.+)', content)
    if theme_match:
        metadata['theme'] = theme_match.group(1).strip()
    
    # Extract day
    day_match = re.search(r'\*\*Day\*\*:\s*(\d+)', content)
    if day_match:
        metadata['day'] = int(day_match.group(1))
    
    # Extract first paragraph for description
    para_match = re.search(r'## Kindergarten Explanation\n\n(.+?)(?:\n\n|\n##)', content, re.DOTALL)
    if para_match:
        desc = para_match.group(1).strip()
        metadata['description'] = desc[:150] + '...' if len(desc) > 150 else desc
    
    return metadata


def convert_all_entries():
    """Convert all markdown entries to HTML."""
    
    repo_root = Path(__file__).parent.parent
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
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        converted += 1
        print(f"✅ Converted: {md_file.name} → {html_filename}")
    
    print(f"\n🎉 Total converted: {converted} entries")


if __name__ == "__main__":
    convert_all_entries()
