#!/usr/bin/env python3
"""Weird AI Experiment Ideator - generates interesting, buildable AI experiment ideas."""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

from src.crew import run_ideation_session
from src.config import OUTPUT_DIR, JSON_DIR, MARKDOWN_DIR, DEFAULT_MODEL


def main():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    Path(JSON_DIR).mkdir(parents=True, exist_ok=True)
    Path(MARKDOWN_DIR).mkdir(parents=True, exist_ok=True)

    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY not set")
        sys.exit(1)

    try:
        result = run_ideation_session()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Get clean model name for display
        model_display = DEFAULT_MODEL.split("/")[-1] if "/" in DEFAULT_MODEL else DEFAULT_MODEL

        # Save markdown
        md_file = Path(MARKDOWN_DIR) / f"{timestamp}_ideas.md"
        with open(md_file, "w") as f:
            f.write("# Weird AI Experiment Ideas\n\n")
            f.write(f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} using {model_display}*\n\n")

            f.write("---\n\n")
            f.write("## Stage 1: Initial Generation\n\n")
            f.write("*The first agent was tasked with generating original, surprising AI experiment ideas. ")
            f.write("It was instructed to avoid generic applications and focus on playful, thought-provoking concepts.*\n\n")
            f.write(result.generation_output or "*empty*")

            f.write("\n\n---\n\n")
            f.write("## Stage 2: Blind Review — Interest & Surprise\n\n")
            f.write("*This agent received ONLY the original ideas above. It did not know any other agent had reviewed them. ")
            f.write("Its task was to make each idea more interesting and surprising.*\n\n")
            f.write(result.amplified_1_output or "*empty*")

            f.write("\n\n---\n\n")
            f.write("## Stage 3: Blind Review — Shareability\n\n")
            f.write("*This agent also received ONLY the original ideas (Stage 1). It was completely blinded from Stage 2's output. ")
            f.write("Its task was to find the most compelling, buildable, shareable version of each idea.*\n\n")
            f.write(result.amplified_2_output or "*empty*")

            f.write("\n\n---\n\n")
            f.write("## Stage 4: Final Synthesis\n\n")
            f.write("*The final agent received all previous outputs and selected the 10 best ideas, ")
            f.write("synthesizing the different perspectives into concrete, buildable plans.*\n\n")
            f.write(result.final_output or "*empty*")

        # Save JSON
        json_file = Path(JSON_DIR) / f"{timestamp}_ideas.json"
        with open(json_file, "w") as f:
            json.dump({"timestamp": timestamp, "model": DEFAULT_MODEL, **result.to_dict()}, f, indent=2)

        print(f"\n📄 Markdown: {md_file}")
        print(f"📊 JSON: {json_file}")
        print(f"\n💡 PDF: python convert_to_pdf.py {md_file}")

    except KeyboardInterrupt:
        print("\n⚠️ Interrupted")
    except Exception as e:
        print(f"\n❌ {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
