#!/usr/bin/env python3
"""Convert markdown ideation reports to PDF."""
import argparse
import re
import json
from pathlib import Path
from typing import List, Dict
from src.pdf_generator import generate_ideas_pdf


def parse_markdown_to_ideas(markdown_content: str) -> List[Dict]:
    """
    Parse markdown report to extract structured ideas.

    This is a simple parser that attempts to extract ideas from the
    markdown format. It looks for numbered ideas with sections.
    """
    ideas = []

    # Try to find numbered ideas (e.g., "1. Title" or "# 1: Title")
    # This is a best-effort parser
    idea_pattern = r"(?:^|\n)(?:#{1,3}\s*)?(\d+)[:\.\)]\s*(.+?)(?=\n(?:#{1,3}\s*)?\d+[:\.\)]|\Z)"

    matches = re.finditer(idea_pattern, markdown_content, re.DOTALL)

    for match in matches:
        idea_num = int(match.group(1))
        idea_content = match.group(2).strip()

        # Extract title (first line)
        lines = idea_content.split("\n")
        title = lines[0].strip().strip("*#").strip()

        # Try to extract sections
        description = ""
        implementation = ""
        feasibility = ""
        potential_impact = ""
        elevator_pitch = ""

        # Look for section headers
        section_map = {
            "description": ["description", "what is it", "overview"],
            "implementation": ["implementation", "how to build", "technical"],
            "feasibility": ["feasibility", "difficulty", "resources"],
            "potential_impact": ["impact", "potential", "value", "outcome"],
            "elevator_pitch": ["pitch", "summary", "tldr"],
        }

        current_section = None
        current_content = []

        for line in lines[1:]:
            line_lower = line.lower().strip()

            # Check if this is a section header
            found_section = False
            for section_key, keywords in section_map.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Save previous section
                    if current_section and current_content:
                        if current_section == "description":
                            description = "\n".join(current_content)
                        elif current_section == "implementation":
                            implementation = "\n".join(current_content)
                        elif current_section == "feasibility":
                            feasibility = "\n".join(current_content)
                        elif current_section == "potential_impact":
                            potential_impact = "\n".join(current_content)
                        elif current_section == "elevator_pitch":
                            elevator_pitch = "\n".join(current_content)

                    # Start new section
                    current_section = section_key
                    current_content = []
                    found_section = True
                    break

            if not found_section and current_section:
                current_content.append(line)

        # Save last section
        if current_section and current_content:
            content_str = "\n".join(current_content).strip()
            if current_section == "description":
                description = content_str
            elif current_section == "implementation":
                implementation = content_str
            elif current_section == "feasibility":
                feasibility = content_str
            elif current_section == "potential_impact":
                potential_impact = content_str
            elif current_section == "elevator_pitch":
                elevator_pitch = content_str

        # If no elevator pitch found, use first sentence of description
        if not elevator_pitch and description:
            first_sentence = re.split(r"[.!?]", description)[0]
            elevator_pitch = first_sentence[:200] if len(first_sentence) > 200 else first_sentence

        idea = {
            "id": idea_num,
            "title": title,
            "elevator_pitch": elevator_pitch or f"AI experiment idea: {title}",
            "description": description or idea_content,
            "implementation": implementation,
            "feasibility": feasibility,
            "potential_impact": potential_impact,
        }

        ideas.append(idea)

    return ideas


def convert_markdown_to_pdf(markdown_file: Path, output_pdf: Path = None):
    """Convert a markdown ideation report to PDF."""
    if not markdown_file.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_file}")

    # Read markdown
    with open(markdown_file, "r") as f:
        markdown_content = f.read()

    # Parse ideas from markdown
    ideas = parse_markdown_to_ideas(markdown_content)

    if not ideas:
        print("⚠ No ideas found in markdown. Creating PDF from raw content.")
        ideas = [
            {
                "id": 1,
                "title": "Ideation Report",
                "elevator_pitch": "Full ideation session output",
                "description": markdown_content[:5000],  # First 5000 chars
            }
        ]

    # Determine output path
    if output_pdf is None:
        output_pdf = markdown_file.with_suffix(".pdf")

    # Generate PDF
    generate_ideas_pdf(ideas, str(output_pdf))
    return output_pdf


def main():
    """CLI for converting markdown reports to PDF."""
    parser = argparse.ArgumentParser(
        description="Convert markdown ideation reports to PDF"
    )
    parser.add_argument("input", type=Path, help="Input markdown file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output PDF file (default: same name as input with .pdf extension)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all .md files in the input directory",
    )

    args = parser.parse_args()

    if args.batch:
        # Process all markdown files in directory
        if not args.input.is_dir():
            print(f"❌ Error: {args.input} is not a directory")
            return

        markdown_files = list(args.input.glob("*.md"))
        if not markdown_files:
            print(f"❌ No markdown files found in {args.input}")
            return

        print(f"📚 Converting {len(markdown_files)} markdown files to PDF...")
        for md_file in markdown_files:
            try:
                pdf_file = md_file.with_suffix(".pdf")
                print(f"\n  Converting: {md_file.name}")
                convert_markdown_to_pdf(md_file, pdf_file)
                print(f"  ✓ Created: {pdf_file.name}")
            except Exception as e:
                print(f"  ✗ Error converting {md_file.name}: {e}")

    else:
        # Process single file
        try:
            print(f"📄 Converting {args.input} to PDF...")
            output_pdf = convert_markdown_to_pdf(args.input, args.output)
            print(f"✓ PDF created: {output_pdf}")
            print(f"  Size: {output_pdf.stat().st_size / 1024:.2f} KB")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main()
