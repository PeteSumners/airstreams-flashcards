#!/usr/bin/env python3
"""
Fully Automated Training Module Pipeline (Using Claude Code CLI)

This script automates the entire process from video to published flashcards:
1. Extract slides from video
2. Generate flashcards using Claude Code headless mode (FREE - no API key!)
3. Convert to web and Quizlet formats
4. Update modules.json
5. Ready to commit and push

Requirements:
    - Claude Code installed
    - opencv-python, imagehash, pillow (already installed)

Usage:
    python fully_automated_pipeline_cli.py <video_path> --module-id <id> --title "Module Title" --description "Description"

Example:
    python fully_automated_pipeline_cli.py "source-videos/Capstan Hoist.mp4" \\
        --module-id "capstan-hoist" \\
        --title "Capstan Hoist Operations" \\
        --description "Safe capstan hoist operation for telecommunications tower work" \\
        --topics "ANSI A10.48" "Lifting Devices" "Safe Operations"
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path


def run_command(cmd, description, shell=False):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"[*] {description}")
    print(f"{'='*60}")

    if isinstance(cmd, list):
        print(f"Running: {' '.join(cmd)}")
    else:
        print(f"Running: {cmd}")

    result = subprocess.run(cmd, capture_output=True, text=True, shell=shell)

    if result.returncode != 0:
        print(f"ERROR: {description} failed")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout)
    return result.stdout


def extract_slides(video_path, threshold=0.97):
    """Step 1: Extract slides from video"""
    cmd = ["python", "deduplicate_video.py", video_path, str(threshold)]
    output = run_command(cmd, "Extracting slides from video")

    # Parse output to find slides directory
    for line in output.split('\n'):
        if 'After dedup:' in line:
            slides_dir = line.split('After dedup:')[1].strip()
            # Remove trailing slash/backslash
            slides_dir = slides_dir.rstrip('/\\')
            return slides_dir

    # Fallback: construct path from video name
    video_name = Path(video_path).stem
    slides_dir = f"test_output/{video_name}_after_dedup"

    if not os.path.exists(slides_dir):
        print(f"ERROR: Could not find slides directory: {slides_dir}")
        sys.exit(1)

    return slides_dir


def generate_flashcards_cli(slides_dir, module_id, module_name):
    """Step 2: Generate flashcards using Claude Code CLI (headless mode)"""
    output_file = f"modules/{module_id}/flashcards.txt"

    # Create module directory
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Count slides
    import glob
    slides = glob.glob(os.path.join(slides_dir, "*.jpg"))
    slides.extend(glob.glob(os.path.join(slides_dir, "*.jpeg")))
    slides.extend(glob.glob(os.path.join(slides_dir, "*.png")))
    num_slides = len(slides)

    print(f"\n{'='*60}")
    print(f"[*] Generating flashcards using Claude Code CLI (headless)")
    print(f"{'='*60}")
    print(f"Slides: {num_slides} images")
    print(f"Output: {output_file}")
    print("This may take a minute or two...")

    # Build prompt
    prompt = f"""Please read all {num_slides} slides in {slides_dir} and create comprehensive flashcards for the {module_name} training module.

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

    try:
        # Run claude in headless mode
        # On Windows, need to use shell=True to resolve .cmd files
        # When using shell=True, pass command as string
        cmd = f'claude -p "{prompt.replace(chr(34), chr(39))}"'  # Replace " with ' in prompt
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
            shell=True  # Needed on Windows to resolve .cmd files
        )

        if result.returncode != 0:
            print(f"ERROR running Claude Code:")
            print(result.stderr)
            sys.exit(1)

        print(result.stdout)

        # Verify file was created
        if not os.path.exists(output_file):
            print(f"ERROR: Flashcards file was not created at {output_file}")
            sys.exit(1)

        return output_file

    except subprocess.TimeoutExpired:
        print(f"ERROR: Timeout - Flashcard generation took too long")
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERROR: 'claude' command not found")
        print("Make sure Claude Code is installed and in your PATH")
        sys.exit(1)


def convert_formats(flashcards_file):
    """Step 3: Convert to web and Quizlet formats"""
    run_command(
        ["python", "scripts/convert_to_web_format.py", flashcards_file],
        "Converting to web format"
    )

    run_command(
        ["python", "scripts/create_quizlet_format.py", flashcards_file],
        "Converting to Quizlet format"
    )


def count_flashcards(flashcards_file):
    """Count number of flashcards in file"""
    with open(flashcards_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return content.count('\nQ: ')


def update_modules_json(module_id, title, description, topics, card_count, source_name):
    """Step 4: Update modules.json"""
    modules_file = "docs/modules.json"

    with open(modules_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if module already exists
    for source in data["sources"]:
        if source["id"] == module_id:
            print(f"WARNING: Module {module_id} already exists in modules.json")
            print("Updating existing module...")
            source["modules"][0]["cardCount"] = card_count
            source["totalCards"] = card_count

            # Save updated modules.json
            with open(modules_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            print(f"SUCCESS: Updated modules.json with {module_id} module ({card_count} cards)")
            return

    # Create new module entry
    new_module = {
        "id": module_id,
        "title": title,
        "description": description,
        "slidesDownload": f"downloads/{module_id}-slides.zip",
        "modules": [
            {
                "id": module_id,
                "title": title,
                "description": description,
                "cardCount": card_count,
                "topics": topics if topics else [],
                "flashcardsFile": f"flashcards-{module_id}.js",
                "enabled": True
            }
        ],
        "totalCards": card_count,
        "moduleCount": 1
    }

    # Add to sources
    data["sources"].append(new_module)

    # Save updated modules.json
    with open(modules_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"\nSUCCESS: Updated modules.json with {module_id} module ({card_count} cards)")


def main():
    parser = argparse.ArgumentParser(
        description='Fully automated training module pipeline (using Claude Code CLI - FREE!)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python fully_automated_pipeline_cli.py "source-videos/Electrical Safety.mp4" \\
      --module-id "electrical-safety" \\
      --title "Electrical Safety" \\
      --description "OSHA electrical hazards, power line clearances, GFCI, and LOTO procedures" \\
      --topics "Power Line Clearances" "GFCI Requirements" "LOTO Procedures" "Electrical Hazards"

Note: This uses Claude Code's headless mode - NO API KEY NEEDED!
        """
    )

    parser.add_argument('video_path', help='Path to training video')
    parser.add_argument('--module-id', required=True, help='Module ID (lowercase-with-hyphens)')
    parser.add_argument('--title', required=True, help='Module title')
    parser.add_argument('--description', required=True, help='Module description')
    parser.add_argument('--topics', nargs='*', help='List of topics covered')
    parser.add_argument('--threshold', type=float, default=0.97, help='Deduplication threshold (default: 0.97)')
    parser.add_argument('--source-name', help='Source name for grouping (default: standalone module)')

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.video_path):
        print(f"ERROR: Video file not found: {args.video_path}")
        sys.exit(1)

    print("\n" + "="*60)
    print("FULLY AUTOMATED TRAINING MODULE PIPELINE")
    print("(Using Claude Code CLI - FREE, no API key!)")
    print("="*60)
    print(f"Video: {args.video_path}")
    print(f"Module ID: {args.module_id}")
    print(f"Title: {args.title}")
    print("="*60)

    try:
        # Step 1: Extract slides
        slides_dir = extract_slides(args.video_path, args.threshold)

        # Step 2: Generate flashcards using Claude Code CLI
        flashcards_file = generate_flashcards_cli(slides_dir, args.module_id, args.title)

        # Step 3: Convert formats
        convert_formats(flashcards_file)

        # Step 4: Count cards and update modules.json
        card_count = count_flashcards(flashcards_file)
        update_modules_json(
            args.module_id,
            args.title,
            args.description,
            args.topics,
            card_count,
            args.source_name
        )

        # Success summary
        print("\n" + "="*60)
        print("PIPELINE COMPLETE!")
        print("="*60)
        print(f"Generated {card_count} flashcards")
        print(f"Module files created:")
        print(f"   - modules/{args.module_id}/flashcards.txt")
        print(f"   - modules/{args.module_id}/flashcards_quizlet.txt")
        print(f"   - docs/flashcards-{args.module_id}.js")
        print(f"   - docs/downloads/{args.module_id}-slides.zip")
        print(f"\nNext steps:")
        print(f"   1. Test locally: python -m http.server 8000")
        print(f"      Visit: http://localhost:8000/docs/?module={args.module_id}")
        print(f"   2. Commit and push:")
        print(f"      git add -A")
        print(f"      git commit -m \"Add {args.title} training module - {card_count} flashcards\"")
        print(f"      git push origin master")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\nERROR: Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
