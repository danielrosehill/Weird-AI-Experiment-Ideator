#!/usr/bin/env python3
"""Main entry point for the Weird AI Experiment Ideator."""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

from src.crew import run_ideation_session, IdeationResult
from src.config import OUTPUT_DIR, JSON_DIR, PDF_DIR, MARKDOWN_DIR
from src.pdf_generator import generate_full_run_pdf


def save_individual_outputs(result: IdeationResult, base_path: Path, timestamp: str):
    """Save each agent's output as a separate markdown file."""
    outputs = {
        "01_generation": result.generation_output,
        "02_amplification_pass1": result.amplification_1_output,
        "03_amplification_pass2_MAXIMUM_CHAOS": result.amplification_2_output,
        "04_evaluation": result.evaluation_output,
        "05_categorization": result.categorization_output,
        "06_synthesis": result.synthesis_output,
    }

    saved_files = []
    for name, content in outputs.items():
        if content:
            file_path = base_path / f"{timestamp}_{name}.md"
            with open(file_path, "w") as f:
                f.write(f"# {name.split('_')[1].title()} Output\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(content)
            saved_files.append(file_path)
            print(f"  ✓ {file_path.name}")

    return saved_files


def main():
    """Run the ideation session and save results."""
    # Ensure output directories exist
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    Path(JSON_DIR).mkdir(parents=True, exist_ok=True)
    Path(PDF_DIR).mkdir(parents=True, exist_ok=True)
    Path(MARKDOWN_DIR).mkdir(parents=True, exist_ok=True)

    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ Error: OPENROUTER_API_KEY not found in environment variables.")
        print("Please copy .env.example to .env and add your OpenRouter API key.")
        sys.exit(1)

    try:
        # Run the ideation session
        print("🚀 Running ideation session...")
        result = run_ideation_session()

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"ideation_{timestamp}"

        # Save individual agent outputs
        print("\n📝 Saving individual agent outputs...")
        markdown_path = Path(MARKDOWN_DIR)
        saved_files = save_individual_outputs(result, markdown_path, timestamp)

        # Save combined markdown report
        print("\n📝 Saving combined markdown report...")
        combined_file = markdown_path / f"{base_name}_COMPLETE.md"
        with open(combined_file, "w") as f:
            f.write("# Weird AI Experiment Ideation - Complete Run\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("**Pipeline:** Generator → Amplifier #1 (blinded) → Amplifier #2 (blinded) → Evaluator → Categorizer → Synthesizer\n\n")
            f.write("---\n\n")

            f.write("# Part 1: Initial Weird Ideas Generation\n\n")
            f.write("*The mad scientist generates the initial batch of weird ideas...*\n\n")
            f.write(result.generation_output or "*No output captured*")
            f.write("\n\n---\n\n")

            f.write("# Part 2: First Weirdness Amplification (Blinded)\n\n")
            f.write("*The first amplifier thinks these are rough drafts and tries to make them weirder...*\n\n")
            f.write(result.amplification_1_output or "*No output captured*")
            f.write("\n\n---\n\n")

            f.write("# Part 3: Second Weirdness Amplification - MAXIMUM CHAOS (Also Blinded!)\n\n")
            f.write("*The second amplifier ALSO thinks these are just preliminary ideas and cranks them to 11...*\n\n")
            f.write(result.amplification_2_output or "*No output captured*")
            f.write("\n\n---\n\n")

            f.write("# Part 4: Evaluation\n\n")
            f.write("*Assessing all versions across all dimensions...*\n\n")
            f.write(result.evaluation_output or "*No output captured*")
            f.write("\n\n---\n\n")

            f.write("# Part 5: Categorization\n\n")
            f.write("*Organizing the chaos into meaningful categories...*\n\n")
            f.write(result.categorization_output or "*No output captured*")
            f.write("\n\n---\n\n")

            f.write("# Part 6: Final Synthesis\n\n")
            f.write("*Bringing it all together...*\n\n")
            f.write(result.synthesis_output or "*No output captured*")

        print(f"  ✓ {combined_file.name}")

        # Save JSON data
        print("\n📊 Saving structured JSON data...")
        json_file = Path(JSON_DIR) / f"{base_name}.json"
        json_data = {
            "timestamp": timestamp,
            "generated_at": datetime.now().isoformat(),
            "outputs": result.to_dict(),
        }
        with open(json_file, "w") as f:
            json.dump(json_data, f, indent=2)
        print(f"  ✓ {json_file.name}")

        # Generate PDF with full run
        print("\n📄 Generating PDF with complete run...")
        pdf_file = Path(PDF_DIR) / f"{base_name}.pdf"
        try:
            generate_full_run_pdf(result, str(pdf_file))
            print(f"  ✓ {pdf_file.name}")
        except Exception as pdf_error:
            print(f"  ⚠ PDF generation failed: {pdf_error}")
            pdf_file = None

        # Print summary
        print("\n" + "=" * 80)
        print("📁 Output Summary")
        print("=" * 80)

        print(f"\nIndividual Agent Outputs ({len(saved_files)} files):")
        for f in saved_files:
            print(f"  • {f.name} ({f.stat().st_size / 1024:.1f} KB)")

        print(f"\nCombined Report:")
        print(f"  • {combined_file.name} ({combined_file.stat().st_size / 1024:.1f} KB)")

        print(f"\nJSON Data:")
        print(f"  • {json_file.name} ({json_file.stat().st_size / 1024:.1f} KB)")

        if pdf_file and pdf_file.exists():
            print(f"\nPDF Report:")
            print(f"  • {pdf_file.name} ({pdf_file.stat().st_size / 1024:.1f} KB)")

        print("=" * 80)
        print("✅ All outputs saved successfully!")

    except Exception as e:
        print(f"\n❌ Error during ideation session: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
