# Processing New Training Videos

This guide walks you through adding flashcards from new training videos to the Airstreams Flashcards system.

## Quick Start

For a fully automated experience, use:
```bash
python add_module.py
```

The script will guide you through each step interactively.

## Manual Process (Step-by-Step)

If you prefer to do it manually or need more control, follow these steps:

### Prerequisites

1. Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Place your training video in `source-videos/` folder:
```bash
source-videos/
├── Fire Awareness.mp4
├── Signalperson.mp4
└── Your-New-Video.mp4
```

---

## Step 1: Extract Slides from Video

Run the deduplication script to extract unique slides:

```bash
python deduplicate_video.py "source-videos/Your-Video.mp4" 0.97
```

**Parameters:**
- `0.97` = similarity threshold (0.95-0.98 recommended for training videos)
  - Higher = keeps more slides (less aggressive deduplication)
  - Lower = removes more duplicates (more aggressive)

**Output:**
- `test_output/Your-Video_before_dedup/` - All extracted frames
- `test_output/Your-Video_after_dedup/` - Unique slides only
- `docs/downloads/your-video-slides.zip` - Public download (after git push)

**Example:**
```
============================================================
VIDEO DEDUPLICATION RESULTS
============================================================
Input video: source-videos/Fire Awareness.mp4
Frames extracted: 63
Unique frames: 46
Duplicates removed: 17
Reduction: 27.0%
============================================================
```

---

## Step 2: Create Flashcards with Claude Code

Now use Claude Code to read the slides and create flashcards.

**Prompt to use:**
```
Please read all slides in test_output/Your-Video_after_dedup/ and create
comprehensive flashcards covering all important training content.

Save to: modules/your-module-name/flashcards.txt

Use this Q&A format:
Q: Question here
A: Answer here

Focus on testable knowledge, regulations, procedures, and key concepts.
```

**Claude will:**
1. Read all slide images
2. Extract key information
3. Create Q&A flashcards
4. Save to the module directory

**Expected output structure:**
```
modules/your-module-name/
└── flashcards.txt
```

---

## Step 3: Convert to Web & Quizlet Formats

Run the conversion scripts to create web and Quizlet versions:

```bash
# Create web format (JavaScript for web app)
python scripts/convert_to_web_format.py modules/your-module-name/flashcards.txt

# Create Quizlet format (TSV for import)
python scripts/create_quizlet_format.py modules/your-module-name/flashcards.txt
```

**Output:**
```
modules/your-module-name/
├── flashcards.txt           ← Original Q&A format
└── flashcards_quizlet.txt   ← Quizlet import format

docs/
└── flashcards-your-module-name.js  ← Web app format
```

---

## Step 4: Update Configuration

Edit `docs/modules.json` and add your new module to the `modules` array:

```json
{
  "id": "your-module-name",
  "title": "Your Module Title",
  "description": "Brief description of what this module covers",
  "cardCount": 43,
  "topics": [
    "Topic 1",
    "Topic 2",
    "Topic 3"
  ],
  "flashcardsFile": "flashcards-your-module-name.js",
  "enabled": true
}
```

**Field Guidelines:**
- `id`: Lowercase with hyphens (e.g., "fire-awareness")
- `title`: Display name shown on module card
- `description`: 1-2 sentence overview
- `cardCount`: Count the Q: lines in your flashcards.txt file
- `topics`: Main topics covered (4-8 topics recommended)
- `flashcardsFile`: Must match filename in docs/ (flashcards-{id}.js)
- `enabled`: Set to `true` to make it visible

---

## Step 5: Test Locally

Open the web app in your browser to verify everything works:

```bash
# Windows
start docs/index.html

# Or use a local server
python -m http.server 8000
# Then visit: http://localhost:8000/docs/
```

**Test Checklist:**
- ✅ Module card appears on home screen
- ✅ Can click to open module
- ✅ All flashcards load correctly
- ✅ Navigation works (flip, next, previous)
- ✅ Shuffle works
- ✅ No console errors (F12)

---

## Step 6: Commit and Push

Once tested, commit your changes:

```bash
# Stage all changes
git add -A

# Check what will be committed
git status

# Commit with descriptive message
git commit -m "Add [Module Name] training module

- XX flashcards covering [main topics]
- Topics: [list main topics]
- Extracted from [video name]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub
git push origin master
```

**Your flashcards will be live at:**
```
https://petesumners.github.io/airstreams-flashcards/
```

(Usually takes 2-3 minutes for GitHub Pages to update)

---

## Complete File Structure

After adding a module, your structure should look like:

```
airstreams-flashcards/
├── source-videos/
│   └── Your-Video.mp4                   # Source training video
│
├── test_output/
│   ├── Your-Video_before_dedup/         # All frames
│   │   └── frame_XXXX.jpg
│   └── Your-Video_after_dedup/          # Unique slides only
│       └── unique_XXXX.jpg
│
├── modules/
│   └── your-module-name/
│       ├── flashcards.txt               # Original Q&A format
│       └── flashcards_quizlet.txt       # For Quizlet import
│
└── docs/
    ├── index.html
    ├── modules.json                     # ← Updated with new module
    ├── flashcards-your-module-name.js   # ← New web flashcards
    └── downloads/
        └── your-module-slides.zip       # ← Public slide download
```

---

## Troubleshooting

### Module doesn't appear on website
- Check `modules.json` syntax with a JSON validator
- Verify `enabled: true`
- Check browser console (F12) for errors
- Clear browser cache

### Flashcards don't load
- Verify `flashcardsFile` name matches actual file in `docs/`
- Check that file exports a `flashcards` array
- Look for JavaScript errors in browser console

### Video processing fails
- Ensure `src/` directory exists (contains video processing modules)
- Check that opencv-python is installed: `pip install opencv-python`
- Try a different threshold value (0.90-0.98)

### Too many/few slides extracted
- **Too many duplicates?** Lower threshold (e.g., 0.90)
- **Missing content?** Raise threshold (e.g., 0.98)
- Check `test_output/X_before_dedup/` to see all frames

---

## Tips & Best Practices

### Slide Extraction
- **Training videos:** Use threshold 0.97 (captures all content)
- **Presentations:** Use threshold 0.90-0.95 (more aggressive dedup)
- Always review `test_output/X_after_dedup/` before creating flashcards

### Creating Flashcards
- Focus on **testable knowledge** (facts, regulations, procedures)
- Keep questions clear and concise
- Avoid yes/no questions - ask for specific information
- Include regulation numbers when relevant (e.g., "1926.1404")
- Use consistent formatting

### Module Organization
- **Module ID:** Use lowercase-with-hyphens
- **Topics:** List 4-8 main topics covered
- **Description:** Keep under 100 characters
- **Card Count:** Count carefully - affects UI display

### Version Control
- Commit after each module addition
- Use descriptive commit messages
- Test locally before pushing
- Keep source videos in `source-videos/` for reference

---

## Example: Full Workflow

Here's a complete example from start to finish:

```bash
# 1. Extract slides
python deduplicate_video.py "source-videos/Electrical-Safety.mp4" 0.97

# 2. Create flashcards with Claude Code
# (Use the prompt from Step 2)

# 3. Convert formats
python scripts/convert_to_web_format.py modules/electrical-safety/flashcards.txt
python scripts/create_quizlet_format.py modules/electrical-safety/flashcards.txt

# 4. Edit docs/modules.json
# (Add the module entry)

# 5. Test
start docs/index.html

# 6. Commit and push
git add -A
git commit -m "Add Electrical Safety module - 31 flashcards"
git push origin master
```

---

## Batch Processing Multiple Videos

If you have multiple videos to process:

```bash
# Extract slides from all videos
for video in source-videos/*.mp4; do
    python deduplicate_video.py "$video" 0.97
done

# Then use Claude Code to create flashcards for each
# Then convert all modules:
python convert_all_modules.py
```

---

## Share Your Module

After pushing, share the direct link:

```
https://petesumners.github.io/airstreams-flashcards/?module=your-module-name
```

Or share the main page:
```
https://petesumners.github.io/airstreams-flashcards/
```

---

## Questions or Issues?

- **Documentation:** See README.md and ADD_NEW_MODULE.md
- **Issues:** https://github.com/PeteSumners/airstreams-flashcards/issues
- **Contact:** petesumners@outlook.com

---

## Changelog

### Recent Additions
- **Fire Awareness for Wind Turbines** (43 cards)
- **Crane Signalperson** (44 cards)

### All Modules
1. Fall Hazards & Protection (62 cards)
2. Electrical Safety (31 cards)
3. Struck-By Hazards (20 cards)
4. Caught-In/Between Hazards (10 cards)
5. Personal Protective Equipment (52 cards)
6. Hazardous Materials & Chemical Safety (38 cards)
7. Confined Spaces (14 cards)
8. Hearing Conservation (18 cards)
9. Material Handling & Storage (49 cards)
10. Hand & Power Tools (51 cards)
11. Excavations & Trenching (26 cards)
12. Fire Awareness for Wind Turbines (43 cards)
13. Crane Signalperson (44 cards)

**Total: 458 flashcards**
