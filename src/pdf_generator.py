"""PDF generation for AI experiment ideas."""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class IdeaPDFGenerator:
    """Generate professional PDF compilations of AI experiment ideas."""

    def __init__(self, output_path: str):
        """Initialize PDF generator."""
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        self.story = []

    def _create_custom_styles(self):
        """Create custom paragraph styles."""
        # Title style
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#1a1a1a"),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            )
        )

        # Idea title style
        self.styles.add(
            ParagraphStyle(
                name="IdeaTitle",
                parent=self.styles["Heading2"],
                fontSize=16,
                textColor=colors.HexColor("#2c3e50"),
                spaceAfter=10,
                spaceBefore=20,
                fontName="Helvetica-Bold",
            )
        )

        # Elevator pitch style
        self.styles.add(
            ParagraphStyle(
                name="ElevatorPitch",
                parent=self.styles["Normal"],
                fontSize=11,
                textColor=colors.HexColor("#7f8c8d"),
                fontName="Helvetica-Oblique",
                spaceAfter=15,
                leftIndent=20,
                rightIndent=20,
            )
        )

        # Section header style
        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading3"],
                fontSize=12,
                textColor=colors.HexColor("#34495e"),
                spaceAfter=8,
                spaceBefore=12,
                fontName="Helvetica-Bold",
            )
        )

        # Body text style
        self.styles.add(
            ParagraphStyle(
                name="BodyText",
                parent=self.styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("#2c3e50"),
                spaceAfter=10,
                alignment=TA_JUSTIFY,
            )
        )

        # Metadata style
        self.styles.add(
            ParagraphStyle(
                name="Metadata",
                parent=self.styles["Normal"],
                fontSize=9,
                textColor=colors.HexColor("#95a5a6"),
                spaceAfter=5,
            )
        )

    def add_cover_page(self, num_ideas: int, timestamp: str):
        """Add cover page to PDF."""
        self.story.append(Spacer(1, 2 * inch))

        title = Paragraph(
            "Weird AI Experiments<br/>Ideation Report", self.styles["CustomTitle"]
        )
        self.story.append(title)
        self.story.append(Spacer(1, 0.5 * inch))

        subtitle = Paragraph(
            f"{num_ideas} Creative AI Experiment Ideas", self.styles["Heading2"]
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.3 * inch))

        date_para = Paragraph(
            f"Generated: {timestamp}", self.styles["Metadata"]
        )
        self.story.append(date_para)

        self.story.append(PageBreak())

    def add_idea(self, idea: Dict[str, Any], rank: int = None):
        """Add a single idea to the PDF."""
        elements = []

        # Idea number and title
        title_text = idea.get("title", "Untitled Idea")
        if rank:
            title_text = f"#{rank}: {title_text}"

        title = Paragraph(title_text, self.styles["IdeaTitle"])
        elements.append(title)

        # Elevator pitch
        if "elevator_pitch" in idea:
            pitch = Paragraph(
                f'"{idea["elevator_pitch"]}"', self.styles["ElevatorPitch"]
            )
            elements.append(pitch)

        # Scores table (if available)
        if "scores" in idea and idea["scores"]:
            elements.append(Spacer(1, 10))
            self._add_scores_table(elements, idea["scores"])

        # Description
        if "description" in idea:
            elements.append(Paragraph("Description", self.styles["SectionHeader"]))
            desc = Paragraph(idea["description"], self.styles["BodyText"])
            elements.append(desc)

        # Implementation
        if "implementation" in idea:
            elements.append(Paragraph("Implementation", self.styles["SectionHeader"]))
            impl = Paragraph(idea["implementation"], self.styles["BodyText"])
            elements.append(impl)

        # Feasibility
        if "feasibility" in idea:
            elements.append(Paragraph("Feasibility", self.styles["SectionHeader"]))
            feas = Paragraph(idea["feasibility"], self.styles["BodyText"])
            elements.append(feas)

        # Potential Impact
        if "potential_impact" in idea:
            elements.append(Paragraph("Potential Impact", self.styles["SectionHeader"]))
            impact = Paragraph(idea["potential_impact"], self.styles["BodyText"])
            elements.append(impact)

        # Commercial Viability
        if idea.get("commercial_viability"):
            elements.append(
                Paragraph("Commercial Viability", self.styles["SectionHeader"])
            )
            comm = Paragraph(idea["commercial_viability"], self.styles["BodyText"])
            elements.append(comm)

        # Domains and technologies
        metadata_parts = []
        if "domain" in idea and idea["domain"]:
            domains = ", ".join(idea["domain"])
            metadata_parts.append(f"<b>Domains:</b> {domains}")

        if "ai_technologies" in idea and idea["ai_technologies"]:
            techs = ", ".join(idea["ai_technologies"])
            metadata_parts.append(f"<b>Technologies:</b> {techs}")

        if metadata_parts:
            elements.append(Spacer(1, 10))
            meta = Paragraph(" | ".join(metadata_parts), self.styles["Metadata"])
            elements.append(meta)

        # Keep idea together on same page
        self.story.append(KeepTogether(elements))
        self.story.append(Spacer(1, 20))

    def _add_scores_table(self, elements: List, scores: Dict[str, Any]):
        """Add evaluation scores as a table."""
        data = [
            ["Creativity", f"{scores.get('creativity_score', 'N/A')}/10"],
            ["Feasibility", f"{scores.get('feasibility_score', 'N/A')}/10"],
            ["Uniqueness", f"{scores.get('uniqueness_score', 'N/A')}/10"],
            ["Impact", f"{scores.get('impact_score', 'N/A')}/10"],
            [
                "Overall",
                f"{scores.get('overall_score', 'N/A'):.1f}/10"
                if isinstance(scores.get("overall_score"), (int, float))
                else "N/A",
            ],
        ]

        table = Table(data, colWidths=[1.5 * inch, 1 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ecf0f1")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#2c3e50")),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
                ]
            )
        )
        elements.append(table)

    def add_section_divider(self, title: str):
        """Add a section divider page."""
        self.story.append(PageBreak())
        self.story.append(Spacer(1, 3 * inch))
        section = Paragraph(title, self.styles["CustomTitle"])
        self.story.append(section)
        self.story.append(PageBreak())

    def build(self):
        """Build the PDF file."""
        self.doc.build(self.story)


def generate_ideas_pdf(
    ideas: List[Dict[str, Any]],
    output_path: str,
    evaluations: List[Dict[str, Any]] = None,
    top_ideas_only: bool = False,
    num_top_ideas: int = 15,
) -> str:
    """
    Generate a PDF compilation of AI experiment ideas.

    Args:
        ideas: List of idea dictionaries
        output_path: Path where PDF should be saved
        evaluations: Optional list of evaluation dictionaries
        top_ideas_only: If True, only include top-rated ideas
        num_top_ideas: Number of top ideas to include if top_ideas_only is True

    Returns:
        Path to generated PDF file
    """
    generator = IdeaPDFGenerator(output_path)

    # Add cover page
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    num_ideas = len(ideas) if not top_ideas_only else min(num_top_ideas, len(ideas))
    generator.add_cover_page(num_ideas, timestamp)

    # Merge evaluations into ideas if provided
    if evaluations:
        eval_map = {e.get("idea_id"): e for e in evaluations if "idea_id" in e}
        for idea in ideas:
            if "id" in idea and idea["id"] in eval_map:
                idea["scores"] = eval_map[idea["id"]]

    # Sort by score if evaluations available
    if evaluations and not top_ideas_only:
        ideas_sorted = sorted(
            ideas,
            key=lambda x: x.get("scores", {}).get("overall_score", 0),
            reverse=True,
        )
    else:
        ideas_sorted = ideas

    # Filter to top ideas if requested
    if top_ideas_only:
        ideas_sorted = ideas_sorted[:num_top_ideas]
        generator.add_section_divider(f"Top {num_top_ideas} Ideas")

    # Add each idea
    for rank, idea in enumerate(ideas_sorted, 1):
        generator.add_idea(idea, rank if evaluations else None)

    # Build PDF
    generator.build()
    return output_path


def batch_generate_pdf_from_json(json_path: str, output_dir: str = None) -> str:
    """
    Generate PDF from a JSON file containing ideas.

    Args:
        json_path: Path to JSON file
        output_dir: Output directory (defaults to same as input)

    Returns:
        Path to generated PDF
    """
    with open(json_path, "r") as f:
        data = json.load(f)

    ideas = data.get("ideas", [])
    evaluations = data.get("evaluations", [])

    if output_dir is None:
        output_dir = Path(json_path).parent

    pdf_name = Path(json_path).stem + ".pdf"
    pdf_path = Path(output_dir) / pdf_name

    return generate_ideas_pdf(ideas, str(pdf_path), evaluations)


def generate_full_run_pdf(result, output_path: str) -> str:
    """
    Generate a comprehensive PDF with ALL agent outputs from an ideation session.

    Args:
        result: IdeationResult containing all agent outputs
        output_path: Path where PDF should be saved

    Returns:
        Path to generated PDF
    """
    from reportlab.platypus import Preformatted
    from reportlab.lib.styles import ParagraphStyle

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        name="CoverTitle",
        parent=styles["Heading1"],
        fontSize=28,
        textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )

    section_style = ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=15,
        spaceBefore=10,
        fontName="Helvetica-Bold",
    )

    subsection_style = ParagraphStyle(
        name="SubsectionTitle",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#34495e"),
        spaceAfter=10,
        spaceBefore=15,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        name="BodyContent",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=8,
        leading=12,
    )

    intro_style = ParagraphStyle(
        name="Intro",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#7f8c8d"),
        fontName="Helvetica-Oblique",
        spaceAfter=15,
    )

    story = []

    # Cover page
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("Weird AI Experiments", title_style))
    story.append(Paragraph("Complete Ideation Run", styles["Heading2"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        "<b>Pipeline:</b> Generator → Amplifier #1 (blinded) → Amplifier #2 (blinded) → Evaluator → Categorizer → Synthesizer",
        styles["Normal"]
    ))
    story.append(PageBreak())

    # Table of contents
    story.append(Paragraph("Contents", section_style))
    toc_items = [
        "1. Initial Weird Ideas Generation",
        "2. First Weirdness Amplification (Blinded)",
        "3. Second Weirdness Amplification - MAXIMUM CHAOS",
        "4. Evaluation",
        "5. Categorization",
        "6. Final Synthesis",
    ]
    for item in toc_items:
        story.append(Paragraph(item, body_style))
    story.append(PageBreak())

    # Helper to add content sections
    def add_section(title: str, intro_text: str, content: str):
        story.append(Paragraph(title, section_style))
        story.append(Paragraph(intro_text, intro_style))
        story.append(Spacer(1, 10))

        if content:
            # Split content into paragraphs and add them
            paragraphs = content.split("\n\n")
            for para in paragraphs:
                if para.strip():
                    # Handle headers
                    if para.strip().startswith("#"):
                        lines = para.strip().split("\n")
                        for line in lines:
                            if line.startswith("###"):
                                story.append(Paragraph(line.replace("###", "").strip(), subsection_style))
                            elif line.startswith("##"):
                                story.append(Paragraph(line.replace("##", "").strip(), subsection_style))
                            elif line.startswith("#"):
                                story.append(Paragraph(line.replace("#", "").strip(), section_style))
                            else:
                                # Escape HTML special chars
                                safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                                story.append(Paragraph(safe_line, body_style))
                    else:
                        # Regular paragraph - escape HTML special chars
                        safe_para = para.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                        # Handle line breaks within paragraph
                        safe_para = safe_para.replace("\n", "<br/>")
                        try:
                            story.append(Paragraph(safe_para, body_style))
                        except Exception:
                            # If paragraph fails, try as preformatted
                            story.append(Spacer(1, 5))
        else:
            story.append(Paragraph("<i>No output captured</i>", body_style))

        story.append(PageBreak())

    # Add each section
    add_section(
        "Part 1: Initial Weird Ideas Generation",
        "The mad scientist generates the initial batch of weird ideas...",
        result.generation_output
    )

    add_section(
        "Part 2: First Weirdness Amplification (Blinded)",
        "The first amplifier thinks these are rough drafts and tries to make them weirder...",
        result.amplification_1_output
    )

    add_section(
        "Part 3: Second Amplification - MAXIMUM CHAOS",
        "The second amplifier ALSO thinks these are just preliminary ideas and cranks them to 11...",
        result.amplification_2_output
    )

    add_section(
        "Part 4: Evaluation",
        "Assessing all versions across creativity, feasibility, uniqueness, and impact...",
        result.evaluation_output
    )

    add_section(
        "Part 5: Categorization",
        "Organizing the chaos into meaningful categories and themes...",
        result.categorization_output
    )

    add_section(
        "Part 6: Final Synthesis",
        "Bringing it all together into actionable insights...",
        result.synthesis_output
    )

    # Build PDF
    doc.build(story)
    return output_path
