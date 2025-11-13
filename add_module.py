#!/usr/bin/env python3
"""
Easy module addition for Airstreams Training Flashcards

Usage:
    python add_module.py

Interactive script that guides you through adding a new training module.
Just answer a few questions and it handles the rest!
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header(text):
    """Print a nice header."""
    print("\n" + "="*60)
    print(text)
    print("="*60 + "\n")

def get_video_files():
    """Find video files in source-videos folder."""
    video_dir = Path("source-videos")
    if not video_dir.exists():
        video_dir.mkdir()
        return []

    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    videos = []
    for ext in video_extensions:
        videos.extend(video_dir.glob(f"*{ext}"))

    return sorted(videos)

def slugify(text):
    """Convert text to slug (lowercase with hyphens)."""
    import re
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = text.strip('-')
    return text

def run_command(cmd, description):
    """Run a command and show progress."""
    print(f"⏳ {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    print(f"✅ {description} - Done!")
    return True

def main():
    print_header("Airstreams Training - Add New Module")

    # Step 1: Find video
    print("Step 1: Select Training Video")
    print("-" * 40)

    videos = get_video_files()

    if not videos:
        print("📹 No videos found in source-videos/ folder")
        print("\nPlace your source video in source-videos/ and run again.")
        print("Example: source-videos/Electrical-Safety.mp4")
        sys.exit(0)

    print("Found videos:")
    for i, video in enumerate(videos, 1):
        print(f"  {i}. {video.name}")

    if len(videos) == 1:
        choice = 1
        print(f"\n✅ Auto-selected: {videos[0].name}")
    else:
        choice = int(input(f"\nSelect video (1-{len(videos)}): "))

    video_path = videos[choice - 1]
    video_name = video_path.stem

    # Step 2: Get module info
    print_header("Step 2: Module Information")

    default_id = slugify(video_name)
    module_id = input(f"Module ID [{default_id}]: ").strip() or default_id

    default_title = video_name.replace('-', ' ').replace('_', ' ').title()
    module_title = input(f"Module Title [{default_title}]: ").strip() or default_title

    module_description = input("Short description: ").strip()

    # Step 3: Extract slides
    print_header("Step 3: Extract Slides from Video")

    threshold = input("Deduplication threshold [0.97]: ").strip() or "0.97"

    cmd = f'python deduplicate_video.py "{video_path}" {threshold}'
    if not run_command(cmd, "Extracting slides from video"):
        sys.exit(1)

    # Count extracted slides
    slides_dir = Path("test_output/2_after_dedup")
    if slides_dir.exists():
        slide_count = len(list(slides_dir.glob("*.jpg")))
        print(f"📊 Extracted {slide_count} unique slides")
    else:
        print("❌ No slides extracted. Check video file.")
        sys.exit(1)

    # Step 4: Generate flashcards
    print_header("Step 4: Generate Flashcards with Claude")

    print("Next step: Use Claude Code to create flashcards")
    print("\nTell Claude:")
    print(f'"""')
    print(f'Please read all slides in test_output/2_after_dedup/ and create')
    print(f'flashcards for {module_title}.')
    print(f'')
    print(f'Format as Q&A pairs:')
    print(f'Q: Question here')
    print(f'A: Answer here')
    print(f'')
    print(f'Focus on testable knowledge, regulations, and key concepts.')
    print(f'Save to: modules/{module_id}/flashcards.txt')
    print(f'"""')

    input("\n✋ Press Enter once you've created the flashcards...")

    # Step 5: Verify flashcards exist
    module_dir = Path(f"modules/{module_id}")
    flashcards_file = module_dir / "flashcards.txt"

    if not flashcards_file.exists():
        print(f"❌ Flashcards not found at: {flashcards_file}")
        print("\nPlease create the flashcards file and run again.")
        sys.exit(1)

    # Count flashcards
    with open(flashcards_file, 'r', encoding='utf-8') as f:
        content = f.read()
        card_count = content.count('Q:')

    print(f"✅ Found {card_count} flashcards")

    # Step 6: Convert formats
    print_header("Step 6: Convert to Web Format")

    # Create Quizlet format
    cmd = f'python scripts/create_quizlet_format.py modules/{module_id}/flashcards.txt'
    run_command(cmd, "Creating Quizlet format")

    # Create web format
    cmd = f'python scripts/convert_to_web_format.py modules/{module_id}/flashcards.txt'
    if not run_command(cmd, "Creating web format"):
        sys.exit(1)

    # Step 7: Update modules.json
    print_header("Step 7: Update Module Configuration")

    modules_file = Path("docs/modules.json")
    with open(modules_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Create new module entry
    new_module = {
        "id": module_id,
        "title": module_title,
        "description": module_description,
        "cardCount": card_count,
        "topics": [],
        "flashcardsFile": f"flashcards-{module_id}.js",
        "enabled": True
    }

    # Add to modules list
    config["modules"].append(new_module)

    # Save updated config
    with open(modules_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    print(f"✅ Added module to configuration")

    # Step 8: Summary
    print_header("🎉 Module Added Successfully!")

    print(f"Module ID: {module_id}")
    print(f"Title: {module_title}")
    print(f"Flashcards: {card_count}")
    print(f"\nFiles created:")
    print(f"  • modules/{module_id}/flashcards.txt")
    print(f"  • modules/{module_id}/flashcards_quizlet.txt")
    print(f"  • docs/flashcards-{module_id}.js")
    print(f"\nUpdated:")
    print(f"  • docs/modules.json")

    # Step 9: Git
    print_header("Step 9: Publish to GitHub")

    print("Ready to publish?")
    publish = input("Push to GitHub? (y/n) [y]: ").strip().lower() or 'y'

    if publish == 'y':
        print("\n⏳ Publishing to GitHub...")

        # Git add
        subprocess.run(["git", "add", f"modules/{module_id}/", "docs/"])

        # Git commit
        commit_msg = f"Add {module_title} training module\n\n{card_count} flashcards covering {module_description}"
        subprocess.run(["git", "commit", "-m", commit_msg])

        # Git push
        result = subprocess.run(["git", "push", "origin", "master"], capture_output=True)

        if result.returncode == 0:
            print("✅ Published to GitHub!")
            print("\n🌐 Live in ~2 minutes at:")
            print("   https://petesumners.github.io/airstreams-flashcards/")
        else:
            print("❌ Push failed. Run manually: git push origin master")
    else:
        print("\nTo publish later, run:")
        print(f"  git add modules/{module_id}/ docs/")
        print(f"  git commit -m 'Add {module_title} module'")
        print("  git push origin master")

    print_header("✨ All Done!")
    print(f"Share with your cohort:")
    print(f"https://petesumners.github.io/airstreams-flashcards/?module={module_id}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
