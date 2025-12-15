#!/usr/bin/env python3
"""Convert markdown ideation reports to cleanly formatted PDFs."""
import sys
import re
import argparse
from pathlib import Path

import markdown
from weasyprint import HTML, CSS

from src.config import DEFAULT_MODEL


def get_model_display_name() -> str:
    """Get clean model name for display."""
    model = DEFAULT_MODEL
    if "/" in model:
        model = model.split("/")[-1]
    return model


PDF_CSS = """
@page {
    size: letter;
    margin: 1in 0.75in;
    @bottom-center {
        content: "Page " counter(page) " — " """ + f'"{get_model_display_name()}"' + """;
        font-size: 8pt;
        color: #666;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
}

@page :first {
    @bottom-center { content: none; }
}

body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #222;
    max-width: 100%;
}

/* Title page */
h1:first-of-type {
    font-size: 28pt;
    font-weight: 300;
    text-align: center;
    margin-top: 2.5in;
    margin-bottom: 0.5in;
    color: #111;
    border: none;
    page-break-after: always;
}

/* Section headers */
h2 {
    font-size: 18pt;
    font-weight: 600;
    color: #c0392b;
    margin-top: 0;
    margin-bottom: 24pt;
    padding-top: 0;
    page-break-before: always;
    border-bottom: 2pt solid #c0392b;
    padding-bottom: 8pt;
}

/* Idea titles */
h3 {
    font-size: 12pt;
    font-weight: 600;
    color: #2c3e50;
    margin-top: 18pt;
    margin-bottom: 6pt;
    page-break-after: avoid;
}

p {
    margin-bottom: 10pt;
    text-align: left;
    orphans: 3;
    widows: 3;
}

/* Bold text for labels */
strong, b {
    font-weight: 600;
    color: #333;
}

/* Italic for hooks */
em, i {
    font-style: italic;
    color: #555;
}

/* Horizontal rules - subtle separator, no page break */
hr {
    border: none;
    border-top: 1pt solid #ddd;
    margin: 20pt 0;
}

/* Lists */
ul, ol {
    margin-left: 18pt;
    margin-bottom: 10pt;
    padding-left: 0;
}

li {
    margin-bottom: 4pt;
}

/* Metadata line */
.meta {
    font-size: 9pt;
    color: #888;
    text-align: center;
    margin-bottom: 0;
}

/* Idea blocks */
.idea-block {
    margin-bottom: 20pt;
    page-break-inside: avoid;
}

/* Hook styling */
.hook {
    background: #f8f8f8;
    padding: 8pt 12pt;
    border-left: 3pt solid #3498db;
    margin: 10pt 0;
    font-style: italic;
}
"""


def clean_markdown(content: str) -> str:
    """Clean up markdown content for better PDF rendering."""
    # Remove any preamble sentences from reviewers
    content = re.sub(
        r'^(I will evaluate|I\'ll evaluate|Here are|Okay,|Let me).*?\n\n',
        '',
        content,
        flags=re.MULTILINE | re.IGNORECASE
    )

    # Convert numbered list items with **Title:** format to h3
    content = re.sub(
        r'^\d+\.\s+\*\*(?:Title:?\s*)?\*\*\s*(.+?)$',
        r'### \1',
        content,
        flags=re.MULTILINE
    )

    # Convert ## N. Title format to ### Title (cleaner hierarchy)
    content = re.sub(
        r'^##\s+\d+\.\s+(.+)$',
        r'### \1',
        content,
        flags=re.MULTILINE
    )

    # Clean up **Hook:** to be on its own styled line
    content = re.sub(
        r'\*\*Hook:?\*\*:?\s*',
        '\n\n**Hook:** ',
        content
    )

    # Clean up **The Idea:** and **The Hook:** labels
    content = re.sub(r'\*\*The Idea\*\*:?\s*', '', content)
    content = re.sub(r'\*\*The Hook\*\*:?\s*', '\n\n**Hook:** ', content)

    return content


def markdown_to_pdf(markdown_path: str, output_path: str = None) -> str:
    """Convert a markdown file to a cleanly formatted PDF."""
    md_path = Path(markdown_path)

    if output_path is None:
        output_path = md_path.with_suffix('.pdf')

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Clean up the markdown
    md_content = clean_markdown(md_content)

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['extra', 'smarty', 'sane_lists'])
    html_content = md.convert(md_content)

    html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Weird AI Experiments</title>
</head>
<body>
{html_content}
</body>
</html>"""

    HTML(string=html_doc).write_pdf(output_path, stylesheets=[CSS(string=PDF_CSS)])
    print(f"PDF generated: {output_path}")
    return str(output_path)


def convert_latest():
    """Find and convert the latest markdown file."""
    md_dir = Path("output/markdown")
    pdf_dir = Path("output/pdf")
    pdf_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(md_dir.glob("*.md"), reverse=True)

    if not files:
        print("No markdown files found in output/markdown")
        sys.exit(1)

    latest = files[0]
    print(f"Converting: {latest.name}")

    output = pdf_dir / (latest.stem.replace("_ideas", "") + ".pdf")
    return markdown_to_pdf(str(latest), str(output))


def main():
    parser = argparse.ArgumentParser(description="Convert markdown to PDF")
    parser.add_argument("input", nargs="?", help="Markdown file (or 'latest')")
    parser.add_argument("-o", "--output", help="Output PDF path")
    args = parser.parse_args()

    if args.input is None or args.input == "latest":
        convert_latest()
    else:
        markdown_to_pdf(args.input, args.output)


if __name__ == "__main__":
    main()
