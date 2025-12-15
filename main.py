#!/usr/bin/env python3
"""Main entry point for the Weird AI Experiment Ideator."""
import os
import sys
from datetime import datetime
from pathlib import Path

from src.crew import run_ideation_session
from src.config import OUTPUT_DIR


def main():
    """Run the ideation session and save results."""
    # Ensure output directory exists
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ Error: OPENROUTER_API_KEY not found in environment variables.")
        print("Please copy .env.example to .env and add your OpenRouter API key.")
        sys.exit(1)

    try:
        # Run the ideation session
        result = run_ideation_session()

        # Save the result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path(OUTPUT_DIR) / f"ideation_report_{timestamp}.md"

        with open(output_file, "w") as f:
            f.write(result)

        print(f"\n📄 Report saved to: {output_file}")
        print(f"📊 File size: {output_file.stat().st_size / 1024:.2f} KB")

    except Exception as e:
        print(f"\n❌ Error during ideation session: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
