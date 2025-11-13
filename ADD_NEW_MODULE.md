# Adding a New Training Module

This guide shows you how to add new training flashcards to the Airstreams Training system.

## Quick Overview

1. Extract slides from your training video
2. Create flashcards with Claude Code
3. Convert to web format
4. Add to modules.json
5. Push to GitHub

## Detailed Steps

### Step 1: Extract Slides from Training Video

Place your training video in the `training-videos/` folder, then run:

```bash
python deduplicate_video.py "training-videos/YourVideo.mp4" 0.97
```

This will create:
- `test_output/1_before_dedup/` - All extracted frames
- `test_output/2_after_dedup/` - Unique slides only

**Tip:** Use threshold 0.97 for training videos to capture all content

### Step 2: Create Flashcards with Claude Code

Ask Claude Code to generate flashcards:

```
Please read all slides in test_output/2_after_dedup/ and create flashcards
in Q&A format for [Topic Name]. Focus on testable knowledge, regulations,
definitions, and safety procedures.
```

Save the output as:
```
modules/[module-name]/flashcards.txt
```

### Step 3: Convert to Web Format

Run the conversion script to create both Anki and web formats:

```bash
# First, copy flashcards to the module folder
mkdir -p modules/[module-name]
cp flashcards.txt modules/[module-name]/

# Convert for Anki (tab-separated)
python convert_to_anki.py modules/[module-name]/flashcards.txt

# Convert for web (JavaScript)
python scripts/convert_to_web_format.py modules/[module-name]/flashcards.txt
```

This creates:
- `modules/[module-name]/flashcards_anki.txt` - For Anki import
- `modules/[module-name]/flashcards_quizlet.txt` - For Quizlet
- `docs/flashcards-[module-name].js` - For web app

### Step 4: Add Module to Configuration

Edit `docs/modules.json` and add your new module:

```json
{
  "id": "module-name",
  "title": "Your Module Title",
  "description": "Brief description of what this module covers",
  "cardCount": 150,
  "topics": [
    "Topic 1",
    "Topic 2",
    "Topic 3"
  ],
  "flashcardsFile": "flashcards-module-name.js",
  "enabled": true
}
```

**Important fields:**
- `id`: Use lowercase with hyphens (e.g., "electrical-safety")
- `title`: Display name shown on module card
- `description`: 1-2 sentence description
- `cardCount`: Number of flashcards
- `flashcardsFile`: Must match the filename in `docs/`
- `enabled`: Set to `true` to make it available

### Step 5: Test Locally

Open `docs/index.html` in your browser to test:

```bash
# Windows
start docs/index.html

# Or use a local server
python -m http.server 8000
# Then visit: http://localhost:8000/docs/
```

Verify:
- ✅ Module card appears on home screen
- ✅ Can click to open module
- ✅ All flashcards load correctly
- ✅ Navigation works (flip, next, previous)
- ✅ Shuffle works

### Step 6: Push to GitHub

```bash
git add modules/ docs/
git commit -m "Add [Module Name] training flashcards"
git push origin master
```

Your flashcards will be live at:
```
https://petesumners.github.io/airstreams-flashcards/
```

## File Structure

After adding a module, your structure should look like:

```
airstreams-flashcards/
├── modules/
│   └── module-name/
│       ├── flashcards.txt           # Original Q&A format
│       ├── flashcards_anki.txt      # For Anki import
│       └── flashcards_quizlet.txt   # For Quizlet import
├── docs/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── modules.json                 # ← Add your module here
│   └── flashcards-module-name.js    # ← Your web flashcards
└── training-videos/
    └── YourVideo.mp4                # Optional: keep source videos
```

## Example: Adding "Electrical Safety" Module

```bash
# 1. Extract slides
python deduplicate_video.py "training-videos/Electrical-Safety.mp4" 0.97

# 2. Create flashcards with Claude
# (manually create: modules/electrical-safety/flashcards.txt)

# 3. Convert formats
mkdir -p modules/electrical-safety
python convert_to_anki.py modules/electrical-safety/flashcards.txt
python scripts/convert_to_web_format.py modules/electrical-safety/flashcards.txt

# 4. Edit docs/modules.json and add:
{
  "id": "electrical-safety",
  "title": "Electrical Safety",
  "description": "OSHA electrical hazards, clearances, GFCI, and LOTO procedures",
  "cardCount": 85,
  "topics": [
    "Electrical Hazards",
    "Power Line Clearances",
    "GFCI Requirements",
    "Extension Cord Safety",
    "Lockout/Tagout (LOTO)"
  ],
  "flashcardsFile": "flashcards-electrical-safety.js",
  "enabled": true
}

# 5. Test locally
start docs/index.html

# 6. Push to GitHub
git add .
git commit -m "Add Electrical Safety training module"
git push
```

## Troubleshooting

### Module doesn't appear

- Check `modules.json` syntax (use JSON validator)
- Make sure `enabled: true`
- Check browser console for errors (F12)

### Flashcards don't load

- Verify `flashcardsFile` name matches actual file in `docs/`
- Check browser console for 404 errors
- Make sure file exports `flashcards` array

### Cards display incorrectly

- Check quotes are properly escaped in JavaScript file
- Verify Q&A format in source file
- Test conversion script on sample data

## Tips

- **Naming Convention:** Use lowercase-with-hyphens for IDs
- **Card Count:** Count flashcards before adding to modules.json
- **Testing:** Always test locally before pushing
- **Backup:** Keep original video files in `training-videos/`
- **Version Control:** Commit after each module addition

## Share with Your Cohort

After pushing, share the direct module URL:

```
https://petesumners.github.io/airstreams-flashcards/?module=module-name
```

Or just share the main page:
```
https://petesumners.github.io/airstreams-flashcards/
```

## Questions?

Create an issue on GitHub:
https://github.com/PeteSumners/airstreams-flashcards/issues
