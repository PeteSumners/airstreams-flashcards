#!/usr/bin/env python3
"""
Automated Flashcard Generation using Claude Code CLI (Headless Mode)

This script processes slides and generates flashcards using Claude Code's
headless mode - NO API KEY REQUIRED!

Requirements:
    - Claude Code installed and working
    - opencv-python (already installed)

Usage:
    python generate_flashcards_cli.py <slides_directory> <output_file> [--module-name "Module Name"]

Example:
    python generate_flashcards_cli.py "test_output/Capstan Hoist_after_dedup" "modules/capstan-hoist/flashcards.txt" --module-name "Capstan Hoist"
"""

import os
import sys
import glob
import argparse
import subprocess
from pathlib import Path


def generate_flashcards_cli(slides_dir, output_file, module_name=None):
    """
    Generate flashcards from slides using Claude Code CLI (headless mode)

    Args:
        slides_dir: Directory containing slide images
        output_file: Path to save flashcards.txt
        module_name: Optional name of the module for context
    """
    # Get all slide images
    image_extensions = ['*.jpg', '*.jpeg', '*.png']
    slides = []
    for ext in image_extensions:
        slides.extend(glob.glob(os.path.join(slides_dir, ext)))

    slides.sort()

    if not slides:
        print(f"Error: No slides found in {slides_dir}")
        sys.exit(1)

    print(f"Found {len(slides)} slides in {slides_dir}")

    # Create module directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Build the prompt
    module_context = f" for the {module_name} training module" if module_name else ""

    prompt = f"""Please read all {len(slides)} slides in {slides_dir} and create comprehensive flashcards{module_context}.

Save the flashcards to: {output_file}

Use this exact Q&A format:
Q: Question here
A: Answer here

Focus on:
- Testable knowledge (facts, regulations, procedures, definitions)
- Safety requirements and warnings
- Technical specifications and standards
- Equipment features and operation
- Inspection requirements
- Best practices

Guidelines:
- Keep questions clear and concise
- Provide complete, accurate answers
- Include regulation numbers when mentioned (e.g., OSHA 1926.xxx, ANSI standards)
- Avoid yes/no questions - ask for specific information
- Cover all important content from the slides
- Use consistent formatting

Generate comprehensive flashcards covering all key information from the training slides."""

    print(f"\nGenerating flashcards with Claude Code (headless mode)...")
    print("This may take a minute or two...")

    try:
        # Run claude in headless mode with -p flag
        # Use --output-format text for clean output
        result = subprocess.run(
            ['claude', '-p', prompt],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        if result.returncode != 0:
            print(f"\n❌ Error running Claude Code:")
            print(result.stderr)
            sys.exit(1)

        # The output should already be the flashcards
        flashcards_text = result.stdout.strip()

        # Verify we got flashcards
        if 'Q:' not in flashcards_text or 'A:' not in flashcards_text:
            print(f"\n❌ Error: Claude Code output doesn't look like flashcards")
            print("Output preview:")
            print(flashcards_text[:500])
            sys.exit(1)

        # Count flashcards
        card_count = flashcards_text.count('\nQ: ')

        print(f"\n✅ Success! Generated {card_count} flashcards")
        print(f"📝 Saved to: {output_file}")

        return flashcards_text

    except subprocess.TimeoutExpired:
        print(f"\n❌ Timeout: Flashcard generation took too long")
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n❌ Error: 'claude' command not found")
        print("Make sure Claude Code is installed and in your PATH")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Generate flashcards from training slides using Claude Code CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_flashcards_cli.py "test_output/Fire Awareness_after_dedup" "modules/fire-awareness/flashcards.txt"
  python generate_flashcards_cli.py "test_output/Capstan Hoist_after_dedup" "modules/capstan-hoist/flashcards.txt" --module-name "Capstan Hoist"

Note: This uses Claude Code's headless mode (free, no API key needed)
        """
    )

    parser.add_argument('slides_dir', help='Directory containing slide images')
    parser.add_argument('output_file', help='Output file path for flashcards.txt')
    parser.add_argument('--module-name', help='Name of the training module (optional)')

    args = parser.parse_args()

    # Validate inputs
    if not os.path.isdir(args.slides_dir):
        print(f"Error: Slides directory not found: {args.slides_dir}")
        sys.exit(1)

    # Generate flashcards
    generate_flashcards_cli(
        slides_dir=args.slides_dir,
        output_file=args.output_file,
        module_name=args.module_name
    )


if __name__ == "__main__":
    main()
