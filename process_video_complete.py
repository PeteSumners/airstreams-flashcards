#!/usr/bin/env python3
"""
Complete Automated Video Processing Pipeline
Handles everything from video input to web-ready flashcards

Usage:
    python process_video_complete.py "source-videos/My-Training.mp4" "my-module" "My Module Title"

Or run interactively:
    python process_video_complete.py
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def slugify(text):
    """Convert text to URL-friendly slug"""
    import re
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def count_flashcards(flashcards_file):
    """Count number of flashcards in a file"""
    with open(flashcards_file, 'r', encoding='utf-8') as f:
        content = f.read()
        return content.count('Q:')

def update_modules_json(module_id, module_title, module_description, card_count, topics, slides_download):
    """Add module to modules.json"""
    modules_file = Path("docs/modules.json")

    with open(modules_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Create new module entry
    new_module = {
        "id": module_id,
        "title": module_title,
        "description": module_description,
        "cardCount": card_count,
        "topics": topics,
        "flashcardsFile": f"flashcards-{module_id}.js",
        "slidesDownload": slides_download,
        "enabled": True
    }

    # Add to modules list
    config["modules"].append(new_module)

    # Write back
    with open(modules_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    print(f"Added module to modules.json: {module_title}")

def main():
    print("=" * 60)
    print("AUTOMATED VIDEO TO FLASHCARDS PIPELINE")
    print("=" * 60)
    print()

    # Get video path
    if len(sys.argv) >= 2:
        video_path = sys.argv[1]
    else:
        print("Available videos in source-videos/:")
        source_dir = Path("source-videos")
        if source_dir.exists():
            videos = list(source_dir.glob("*.mp4"))
            for i, video in enumerate(videos, 1):
                print(f"  {i}. {video.name}")
        print()
        video_path = input("Enter video path (or drag-and-drop file): ").strip().strip('"')

    if not os.path.exists(video_path):
        print(f"Error: Video not found: {video_path}")
        return 1

    video_name = Path(video_path).stem
    print(f"\nProcessing: {video_name}")

    # Get module info
    if len(sys.argv) >= 3:
        module_id = sys.argv[2]
    else:
        default_id = slugify(video_name)
        module_id = input(f"Module ID [{default_id}]: ").strip() or default_id

    if len(sys.argv) >= 4:
        module_title = sys.argv[3]
    else:
        module_title = input(f"Module Title [{video_name}]: ").strip() or video_name

    # STEP 1: Extract slides
    print("\n" + "=" * 60)
    print("STEP 1: Extracting slides from video")
    print("=" * 60)

    threshold = input("Similarity threshold [0.97]: ").strip() or "0.97"

    print(f"\nRunning: deduplicate_video.py \"{video_path}\" {threshold}")
    result = subprocess.run(
        ["python", "deduplicate_video.py", video_path, threshold],
        capture_output=False
    )

    if result.returncode != 0:
        print("Error extracting slides!")
        return 1

    # STEP 2: Create module directory
    print("\n" + "=" * 60)
    print("STEP 2: Creating module directory")
    print("=" * 60)

    module_dir = Path(f"modules/{module_id}")
    module_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created: {module_dir}")

    # STEP 3: Generate flashcards with Claude Code
    print("\n" + "=" * 60)
    print("STEP 3: MANUAL STEP - Generate Flashcards with Claude Code")
    print("=" * 60)

    slides_dir = Path(f"test_output/{video_name}_after_dedup")
    slides_count = len(list(slides_dir.glob("*.jpg")))

    print(f"\nSlides extracted: {slides_count}")
    print(f"Slides location: {slides_dir}")
    print()
    print("=" * 60)
    print("COPY THIS PROMPT FOR CLAUDE CODE:")
    print("=" * 60)
    print()
    print(f'''Please read all {slides_count} slides in {slides_dir}/ and create
comprehensive flashcards covering all important training content.

Save to: {module_dir}/flashcards.txt

Use this exact Q&A format:
Q: Question here
A: Answer here

Focus on:
- Testable knowledge
- Regulations and standards
- Safety procedures
- Key concepts and definitions
- Procedures and protocols

Make sure to cover all important information from the slides.''')
    print()
    print("=" * 60)

    input("\nPress Enter after Claude Code has created the flashcards...")

    # Verify flashcards were created
    flashcards_file = module_dir / "flashcards.txt"
    if not flashcards_file.exists():
        print(f"\nError: Flashcards file not found: {flashcards_file}")
        print("Please create the flashcards file before continuing.")
        return 1

    # Count flashcards
    card_count = count_flashcards(flashcards_file)
    print(f"\nFound {card_count} flashcards!")

    # STEP 4: Convert to web and Quizlet formats
    print("\n" + "=" * 60)
    print("STEP 4: Converting to web and Quizlet formats")
    print("=" * 60)

    print("\nConverting to web format...")
    subprocess.run([
        "python", "scripts/convert_to_web_format.py",
        str(flashcards_file)
    ])

    print("\nConverting to Quizlet format...")
    subprocess.run([
        "python", "scripts/create_quizlet_format.py",
        str(flashcards_file)
    ])

    # STEP 5: Update modules.json
    print("\n" + "=" * 60)
    print("STEP 5: Updating modules.json")
    print("=" * 60)

    module_description = input(f"\nModule description (1-2 sentences): ").strip()

    print("\nEnter main topics (one per line, empty line to finish):")
    topics = []
    while True:
        topic = input(f"  Topic {len(topics) + 1}: ").strip()
        if not topic:
            break
        topics.append(topic)

    if not topics:
        topics = ["Training Content"]

    # Determine slide download path
    slides_download = f"downloads/{slugify(video_name)}-slides.zip"

    update_modules_json(
        module_id=module_id,
        module_title=module_title,
        module_description=module_description,
        card_count=card_count,
        topics=topics,
        slides_download=slides_download
    )

    # STEP 6: Summary
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE!")
    print("=" * 60)

    print(f"\nModule: {module_title}")
    print(f"ID: {module_id}")
    print(f"Flashcards: {card_count}")
    print(f"Slides: {slides_count}")
    print()
    print("Files created:")
    print(f"  - {module_dir}/flashcards.txt")
    print(f"  - {module_dir}/flashcards_quizlet.txt")
    print(f"  - docs/flashcards-{module_id}.js")
    print(f"  - Updated docs/modules.json")
    print()
    print("Next steps:")
    print("  1. Test locally: python -m http.server 8000")
    print("     Visit: http://localhost:8000/docs/")
    print("  2. Commit and push:")
    print("     git add -A")
    print(f'     git commit -m "Add {module_title} module"')
    print("     git push origin master")
    print()
    print("Live in 2-3 minutes at:")
    print("  https://petesumners.github.io/airstreams-flashcards/")
    print()

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
