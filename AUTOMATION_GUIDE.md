# Automation Guide for Training Module Creation

This guide explains how to automate the flashcard generation process using **Claude Code's headless mode** - completely free, no API key required!

## Overview

There are two automation approaches:

1. **CLI-Based Flashcard Generation** - Automates just the flashcard creation step
2. **Fully Automated Pipeline** - Automates the entire process from video to published module

## Prerequisites

### Requirements

- **Claude Code** installed and working (you're already using it!)
- **Python packages** (already installed for video processing):
  - opencv-python
  - pillow
  - imagehash

That's it! **No API key needed** - Claude Code CLI is completely free!

## Option 1: CLI-Based Flashcard Generation Only

Use this if you want to automate just the flashcard creation step (after slides are already extracted).

### Usage

```bash
python generate_flashcards_cli.py <slides_directory> <output_file> [--module-name "Module Name"]
```

### Example

```bash
python generate_flashcards_cli.py "test_output/Capstan Hoist_after_dedup" "modules/capstan-hoist/flashcards.txt" --module-name "Capstan Hoist"
```

### What It Does

1. Reads all slide images from the directory
2. Uses Claude Code's headless mode (`claude -p`) to analyze slides
3. Generates comprehensive flashcards in Q&A format
4. Saves to the specified output file

**Completely free - no API costs!**

### Manual Steps After

After running this script, you still need to:

1. Convert to web/Quizlet formats:
   ```bash
   python scripts/convert_to_web_format.py modules/capstan-hoist/flashcards.txt
   python scripts/create_quizlet_format.py modules/capstan-hoist/flashcards.txt
   ```

2. Update `docs/modules.json` manually

3. Test and commit

## Option 2: Fully Automated Pipeline (RECOMMENDED)

This is the complete end-to-end automation that handles everything using Claude Code CLI.

### Usage

```bash
python fully_automated_pipeline_cli.py <video_path> \
    --module-id <id> \
    --title "Module Title" \
    --description "Module description" \
    --topics "Topic 1" "Topic 2" "Topic 3"
```

### Example

```bash
python fully_automated_pipeline_cli.py "source-videos/Electrical Safety.mp4" \
    --module-id "electrical-safety" \
    --title "Electrical Safety" \
    --description "OSHA electrical hazards, power line clearances, GFCI, and LOTO procedures" \
    --topics "Power Line Clearances" "GFCI Requirements" "LOTO Procedures" "Arc Flash"
```

### What It Does

This script automates the **entire process**:

1. ✅ Extracts unique slides from video
2. ✅ Generates flashcards using Claude Code CLI (headless mode)
3. ✅ Converts to web format (.js)
4. ✅ Converts to Quizlet format (.txt)
5. ✅ Updates modules.json
6. ✅ Creates slide download ZIP

**Completely FREE - uses Claude Code CLI!**

### After Running

The script tells you what to do next:

```bash
# Test locally
python -m http.server 8000
# Visit: http://localhost:8000/docs/?module=your-module-id

# If everything looks good, commit and push
git add -A
git commit -m "Add Module Name training - XX flashcards"
git push origin master
```

## Comparison: Interactive vs Automated

### Interactive (Current Method)

```bash
# Step 1: Extract slides
python deduplicate_video.py "source-videos/Video.mp4" 0.97

# Step 2: Generate flashcards (MANUAL - requires Claude Code interaction)
# You need to:
# - Start Claude Code
# - Type prompt
# - Wait for response
# - Review flashcards

# Step 3: Convert formats
python scripts/convert_to_web_format.py modules/module-name/flashcards.txt
python scripts/create_quizlet_format.py modules/module-name/flashcards.txt

# Step 4: Update modules.json (MANUAL - edit JSON file)

# Step 5: Test and commit
```

**Time:** ~10-15 minutes (with manual interaction)

### Automated (New Method)

```bash
# ONE COMMAND - does everything (FREE!)
python fully_automated_pipeline_cli.py "source-videos/Video.mp4" \
    --module-id "module-name" \
    --title "Module Title" \
    --description "Description" \
    --topics "Topic 1" "Topic 2"

# Test and commit
python -m http.server 8000
git add -A && git commit -m "Add module" && git push
```

**Time:** ~3-5 minutes (fully automated)
**Cost:** FREE (uses Claude Code CLI)

## Tips for Best Results

### 1. Good Slide Extraction

Use appropriate threshold:
- **0.97** (default) - Captures all content, some duplicates
- **0.95** - More aggressive deduplication
- **0.98** - Very conservative, keeps almost everything

### 2. Module Naming

Use consistent naming:
- Module ID: `lowercase-with-hyphens` (e.g., `electrical-safety`)
- Title: `Title Case` (e.g., `Electrical Safety`)
- Description: `Brief sentence describing content`

### 3. Topics

List 4-8 main topics:
```bash
--topics "OSHA Regulations" "Power Line Safety" "GFCI Requirements" "LOTO Procedures"
```

### 4. Review Generated Flashcards

Always review the generated flashcards before publishing:

```bash
# View the flashcards
cat modules/module-name/flashcards.txt | less

# Or open in text editor
code modules/module-name/flashcards.txt
```

## Troubleshooting

### Error: "'claude' command not found"

Make sure Claude Code is installed and in your PATH. Try running:
```bash
claude --version
```

If that doesn't work, check your Claude Code installation.

### Error: "No slides found"

Check the slides directory path:
```bash
ls test_output/*_after_dedup/
```

### Flashcards are low quality

Claude Code works best with clear, text-heavy slides. If slides are:
- Too blurry
- Mostly images/diagrams with little text
- Video screenshots

Then you may get lower quality flashcards. Consider reviewing and editing the flashcards after generation, or using interactive Claude Code for better results.

## Batch Processing Multiple Videos

You can process multiple videos in a loop:

```bash
#!/bin/bash
# process_all_videos.sh

for video in source-videos/*.mp4; do
    # Extract base name
    basename=$(basename "$video" .mp4)
    module_id=$(echo "$basename" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

    echo "Processing: $basename"

    python fully_automated_pipeline_cli.py "$video" \
        --module-id "$module_id" \
        --title "$basename" \
        --description "Training module for $basename" \
        --topics "Safety" "Procedures" "Regulations"

    echo "Completed: $basename"
    echo "---"
done

echo "All videos processed!"
```

Run it:
```bash
chmod +x process_all_videos.sh
./process_all_videos.sh
```

## Hybrid Approach

You can also use a **hybrid approach**:

1. Use CLI for initial flashcard generation
2. Review and edit flashcards manually
3. Re-run conversion scripts

```bash
# Generate initial flashcards
python generate_flashcards_cli.py "test_output/Module_after_dedup" "modules/module-name/flashcards.txt"

# Edit the flashcards
code modules/module-name/flashcards.txt

# Re-convert to web/Quizlet after editing
python scripts/convert_to_web_format.py modules/module-name/flashcards.txt
python scripts/create_quizlet_format.py modules/module-name/flashcards.txt
```

## Questions?

For issues or questions:
- GitHub Issues: https://github.com/PeteSumners/airstreams-flashcards/issues
- Email: petesumners@outlook.com

## Summary

**For maximum automation (ONE COMMAND):**
```bash
python fully_automated_pipeline_cli.py "source-videos/Video.mp4" \
    --module-id "module-id" \
    --title "Module Title" \
    --description "Description" \
    --topics "Topic 1" "Topic 2"
```

**For just automating flashcard generation:**
```bash
python generate_flashcards_cli.py "test_output/Video_after_dedup" "modules/module-id/flashcards.txt"
```

**Cost:** FREE (uses Claude Code CLI headless mode!)

**Time saved:** ~5-10 minutes per module

Happy automating! 🚀
