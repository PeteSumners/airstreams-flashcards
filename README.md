# Airstreams Training Flashcards

Multi-module flashcard system for all Airstreams Renewables training courses.

**Live App:** https://petesumners.github.io/airstreams-flashcards/

Built for Airstreams Renewables - Tehachapi, CA

## What Is This?

A complete system to:
1. Extract slides from any training video
2. Convert them to flashcards with AI
3. Study on any device (web, phone, tablet)
4. Share with your training cohort

Perfect for OSHA certifications, technical training, safety courses, and any video-based learning.

**100% Open Source** - All formats are simple text files (JSON, TSV, JavaScript) that anyone can read and modify!

## Features

✅ **Multi-Module Support** - Unlimited training courses in one place
✅ **Web-Based** - No installation, works on any device
✅ **Mobile-Friendly** - Study on your phone
✅ **Easy Sharing** - Just share the URL
✅ **Open Formats** - JSON, TSV, JavaScript - easy to read and modify
✅ **Quizlet Compatible** - Export to Quizlet for mobile apps
✅ **Free Forever** - Host on GitHub Pages for free

## Quick Start

### For Students (Just Want to Study)

1. Visit: https://petesumners.github.io/airstreams-flashcards/
2. Select a training module
3. Start studying!

**Keyboard Shortcuts:**
- Space/Enter: Flip card
- Arrow Right/N: Next card
- Arrow Left/P: Previous card
- S: Shuffle
- Escape: Back to modules

### For Trainers (Want to Add Content)

See [ADD_NEW_MODULE.md](ADD_NEW_MODULE.md) for complete guide.

**Quick version:**
```bash
# 1. Extract slides from video
python deduplicate_video.py "training-videos/YourVideo.mp4" 0.97

# 2. Create flashcards with Claude Code
# (Ask Claude to generate flashcards from the extracted slides)

# 3. Convert to web format
python scripts/convert_to_web_format.py modules/your-module/flashcards.txt

# 4. Add to docs/modules.json

# 5. Push to GitHub
git add . && git commit -m "Add new training module" && git push
```

## Current Modules

### OSHA 10HR Construction - Fall Hazards
141 flashcards covering:
- Fall statistics and regulations
- Guardrails (1926.502)
- Safety Nets (1926.105)
- Personal Fall Arrest Systems (PFAS)
- Anchorage requirements
- Body harness vs body belts
- Equipment inspection
- Rescue planning

### Coming Soon
- Excavations & Trenching
- Electrical Safety
- Struck-By & Caught-In Hazards
- PPE Requirements
- Confined Spaces
- *...and more as you add them!*

## Study Options

### 1. Web App (Recommended)
**URL:** https://petesumners.github.io/airstreams-flashcards/

✅ No installation
✅ Works on any device
✅ Perfect for GroupMe sharing
✅ Mobile-friendly
✅ Keyboard shortcuts
✅ Auto-flip mode
✅ Progress tracking

### 2. Quizlet (For Mobile Apps)
- Popular platform with mobile apps
- Study games and social features
- Free to use

**Import to Quizlet:**
1. Go to https://quizlet.com/
2. Create → Study set → Import
3. Copy/paste from `modules/[module]/flashcards_quizlet.txt`
4. Set delimiter to: **Tab**
5. Share the set with your cohort!

## Open Source Formats

All flashcards are stored in simple, open formats:

### 1. Plain Text Q&A (`flashcards.txt`)
```
Q: What is the minimum clearance for power lines up to 50 kV?
A: 10 feet.

Q: What does PFAS stand for?
A: Personal Fall Arrest System.
```
- Human-readable
- Easy to edit in any text editor
- Works with Claude Code for AI generation

### 2. Tab-Separated Values (`flashcards_quizlet.txt`)
```
Question[TAB]Answer
Question 2[TAB]Answer 2
```
- Compatible with Quizlet, Excel, Google Sheets
- Simple CSV-like format
- Easy to import/export

### 3. JavaScript (`flashcards-module.js`)
```javascript
const flashcards = [
    { question: "...", answer: "..." },
    { question: "...", answer: "..." }
];
```
- Powers the web app
- Easy to read and modify
- No build step needed - just vanilla JavaScript

### 4. JSON (`modules.json`)
```json
{
  "id": "fall-hazards",
  "title": "Fall Hazards & Protection",
  "cardCount": 141,
  "enabled": true
}
```
- Module configuration
- Easy to parse programmatically
- Industry standard format

**Why These Formats?**
- ✅ No proprietary software needed
- ✅ Easy to version control with Git
- ✅ Anyone can read and modify
- ✅ Compatible with many tools
- ✅ Future-proof

## Project Structure

```
airstreams-flashcards/
├── modules/                      # Training modules
│   └── fall-hazards/
│       ├── flashcards.txt        # Original Q&A (human-readable)
│       └── flashcards_quizlet.txt # TSV for Quizlet import
│
├── docs/                         # Web app (GitHub Pages)
│   ├── index.html                # Main page
│   ├── app.js                    # App logic (vanilla JS)
│   ├── style.css                 # Styling
│   ├── modules.json              # Module definitions (JSON)
│   └── flashcards-*.js           # Flashcards per module (JS)
│
├── training-videos/              # Source videos (optional)
│   └── *.mp4
│
├── scripts/                      # Helper scripts
│   └── convert_to_web_format.py  # Convert Q&A to JS
│
├── deduplicate_video.py          # Extract slides from video
├── ADD_NEW_MODULE.md             # Guide for adding modules
└── README.md                     # This file
```

## Technology Stack

- **Video Processing:** OpenCV + Python
- **OCR & Flashcard Generation:** Claude Code (AI)
- **Web App:** Vanilla JavaScript (no frameworks, no build step)
- **Hosting:** GitHub Pages (free)
- **Formats:** JSON, TSV, plain text, JavaScript

**No build tools, no npm, no webpack** - just simple, readable code!

## How It Works

### 1. Extract Slides
```bash
python deduplicate_video.py "video.mp4" 0.97
```
- Extracts frames every 0.9 seconds
- Uses perceptual hashing to remove duplicates
- Threshold 0.97 keeps all unique content
- Output: Unique slide images

### 2. Generate Flashcards
Ask Claude Code:
```
Read all slides in test_output/2_after_dedup/ and create flashcards.
Format as Q&A pairs. Focus on testable knowledge.
```
Claude creates simple text format:
```
Q: Question here
A: Answer here
```

### 3. Convert Formats
```bash
# Create Quizlet format (TSV)
python scripts/create_quizlet_format.py modules/module-name/flashcards.txt

# Create web format (JavaScript)
python scripts/convert_to_web_format.py modules/module-name/flashcards.txt
```

### 4. Publish
```bash
git add docs/ modules/
git commit -m "Add new module"
git push
```
Live in ~2 minutes at GitHub Pages!

## Adding New Modules

See [ADD_NEW_MODULE.md](ADD_NEW_MODULE.md) for the complete guide.

**Essential steps:**
1. Process your training video with `deduplicate_video.py`
2. Generate flashcards with Claude Code
3. Run conversion scripts
4. Add module to `docs/modules.json`
5. Push to GitHub

Example `modules.json` entry:
```json
{
  "id": "electrical-safety",
  "title": "Electrical Safety",
  "description": "OSHA electrical hazards, clearances, and LOTO",
  "cardCount": 85,
  "topics": ["Power Line Clearances", "GFCI", "LOTO"],
  "flashcardsFile": "flashcards-electrical-safety.js",
  "enabled": true
}
```

## Sharing with Your Cohort

### Share Main Page
```
https://petesumners.github.io/airstreams-flashcards/
```

### Share Specific Module
```
https://petesumners.github.io/airstreams-flashcards/?module=fall-hazards
```

### GroupMe Message Template
```
🎓 Training Flashcards Ready!

Study for [Module Name]:
https://petesumners.github.io/airstreams-flashcards/

📱 Works on any device
🔀 Shuffle feature
⌨️ Keyboard shortcuts

Let's ace this test! 💪
```

## Modifying the Code

Everything is designed to be easy to understand and modify!

### Change Colors/Styling
Edit `docs/style.css` - simple CSS, no preprocessors

### Add Features
Edit `docs/app.js` - vanilla JavaScript with clear comments

### Change Module Info
Edit `docs/modules.json` - standard JSON format

### Edit Flashcards
Edit `modules/[module]/flashcards.txt` - plain text, then regenerate

### Add New Format
Create a new conversion script in `scripts/` - Python is easy to read!

## Installation (For Development)

```bash
# Clone the repo
git clone https://github.com/PeteSumners/airstreams-flashcards.git
cd airstreams-flashcards

# Install dependencies (just OpenCV)
pip install -r requirements.txt

# Process a video
python deduplicate_video.py "your-video.mp4" 0.97

# Generate flashcards with Claude Code
# (manual step - ask Claude to create flashcards)

# Convert formats
python scripts/convert_to_web_format.py modules/module-name/flashcards.txt

# Test locally (no build step needed!)
python -m http.server 8000
# Visit: http://localhost:8000/docs/

# Push to GitHub Pages
git add .
git commit -m "Add module"
git push
```

## Customization

### Branding
Edit `docs/modules.json`:
```json
"settings": {
  "projectName": "Your Company Training",
  "organization": "Your Company",
  "location": "Your Location"
}
```

### Styling
Edit `docs/style.css` - change colors, fonts, layout

### Features
Edit `docs/app.js` - add your own functionality

**No build step required!** Just edit and refresh.

## Troubleshooting

### Module doesn't appear
- Check `docs/modules.json` syntax with a JSON validator
- Ensure `enabled: true`
- Check browser console (F12) for errors

### Flashcards don't load
- Verify filename in `modules.json` matches file in `docs/`
- Check browser console for 404 errors
- Make sure flashcards array is properly formatted

### Local testing issues
```bash
# Always use a local server, not file:// URLs
python -m http.server 8000
# or
python3 -m http.server 8000
```

## FAQ

**Q: Why no build tools?**
A: Keep it simple! Anyone can read and modify the code without learning webpack, npm, etc.

**Q: Can I use this for non-OSHA training?**
A: Yes! Any training video → flashcards workflow works.

**Q: How many modules can I add?**
A: Unlimited. The web app dynamically loads any modules in `modules.json`.

**Q: Do I need to know JavaScript?**
A: No. The conversion scripts handle everything. For advanced customization, the JavaScript is simple and well-commented.

**Q: Can I make this private?**
A: Yes. Change GitHub repo to private. The web app still works for collaborators.

**Q: What about copyrighted training materials?**
A: Only process videos you have rights to use. Flashcards are for personal/team study.

**Q: Why Quizlet instead of Anki?**
A: Quizlet is more accessible with mobile apps and uses a simple open format (TSV). You can still convert to Anki if you want!

## Contributing

Pull requests welcome! Especially:
- New conversion scripts
- Additional study modes
- Mobile app improvements
- Documentation
- Keep it simple!

## Support

- **Issues:** https://github.com/PeteSumners/airstreams-flashcards/issues
- **Discussions:** https://github.com/PeteSumners/airstreams-flashcards/discussions

## License

Apache 2.0 - Free to use and modify.

All dependencies are also open source and permissively licensed.

## Credits

Built with:
- **OpenCV** - Video processing (Apache 2.0)
- **Claude Code** - OCR & flashcard generation (AI)
- **GitHub Pages** - Free hosting
- **Vanilla JavaScript** - No frameworks, just clean code

Created for **Airstreams Renewables** training in Tehachapi, CA.

---

**Made with ❤️ for better training and safer workplaces**

**Keep it open. Keep it simple. Keep it accessible.**

Good luck with your certifications! 🏗️ ⚡ 🦺
