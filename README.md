# Airstreams Training Flashcards

Multi-module flashcard system for all Airstreams Renewables training courses.

**Live App:** https://petesumners.github.io/airstreams-flashcards/

Built for Airstreams Renewables - Tehachapi, CA

## What Is This?

A complete system to:
1. Extract slides from any training video
2. Convert them to flashcards with AI
3. Study on any device (web, phone, Anki, Quizlet)
4. Share with your training cohort

Perfect for OSHA certifications, technical training, safety courses, and any video-based learning.

## Features

✅ **Multi-Module Support** - Unlimited training courses in one place
✅ **Web-Based** - No installation, works on any device
✅ **Mobile-Friendly** - Study on your phone
✅ **Offline Compatible** - Anki & Quizlet exports
✅ **Easy Sharing** - Just share the URL
✅ **Open Source** - Free forever

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

### 1. Web App (Best for Quick Access)
**URL:** https://petesumners.github.io/airstreams-flashcards/

- No installation
- Works on any device
- Perfect for GroupMe sharing
- Mobile-friendly
- Keyboard shortcuts

### 2. Anki (Best for Long-Term Retention)
- Free & open source
- Spaced repetition algorithm
- Desktop + mobile apps
- Works offline

**Import:**
1. Install Anki from https://apps.ankiweb.net/
2. File → Import → Select `modules/[module]/flashcards_anki.txt`
3. Set delimiter to Tab

### 3. Quizlet (Best for Social Learning)
- Popular platform
- Mobile apps
- Study games
- Group features

**Import:**
1. Go to https://quizlet.com/
2. Create → Study set → Import
3. Copy/paste from `modules/[module]/flashcards_quizlet.txt`
4. Set delimiter to Tab

## Project Structure

```
airstreams-flashcards/
├── modules/                      # Training modules
│   ├── fall-hazards/
│   │   ├── flashcards.txt        # Original Q&A
│   │   ├── flashcards_anki.txt   # Anki import
│   │   └── flashcards_quizlet.txt # Quizlet import
│   └── excavations/
│       └── (same structure)
│
├── docs/                         # Web app (GitHub Pages)
│   ├── index.html                # Main page
│   ├── app.js                    # App logic
│   ├── style.css                 # Styling
│   ├── modules.json              # Module definitions
│   └── flashcards-*.js           # Flashcards for each module
│
├── training-videos/              # Source videos (optional)
│   └── *.mp4
│
├── scripts/                      # Helper scripts
│   └── convert_to_web_format.py  # Convert Q&A to JS
│
├── deduplicate_video.py          # Extract slides from video
├── convert_to_anki.py            # Convert to Anki format
├── ADD_NEW_MODULE.md             # Guide for adding modules
└── README.md                     # This file
```

## Technology Stack

- **Video Processing:** OpenCV + Python
- **OCR & Flashcard Generation:** Claude Code (AI)
- **Web App:** Vanilla JavaScript (no frameworks)
- **Hosting:** GitHub Pages (free)
- **Offline Study:** Anki (open source)

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

### 3. Convert Formats
```bash
# For Anki
python convert_to_anki.py flashcards.txt

# For Web
python scripts/convert_to_web_format.py modules/module-name/flashcards.txt
```

### 4. Publish
```bash
git add docs/ modules/
git commit -m "Add new module"
git push
```
Live in ~2 minutes at GitHub Pages URL!

## Adding New Modules

See [ADD_NEW_MODULE.md](ADD_NEW_MODULE.md) for the complete guide.

**Essential steps:**
1. Process your training video
2. Generate flashcards
3. Convert to web format
4. Add to `docs/modules.json`
5. Push to GitHub

Example module entry:
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

## Installation (For Development)

```bash
# Clone the repo
git clone https://github.com/PeteSumners/airstreams-flashcards.git
cd airstreams-flashcards

# Install dependencies
pip install -r requirements.txt

# Process a video
python deduplicate_video.py "your-video.mp4" 0.97

# Generate flashcards with Claude Code
# (manual step - ask Claude to create flashcards)

# Convert formats
python scripts/convert_to_web_format.py modules/module-name/flashcards.txt

# Test locally
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
Edit `docs/style.css` to change colors, fonts, layout.

### Add Features
Edit `docs/app.js` - vanilla JavaScript, no build step needed!

## Troubleshooting

### Module doesn't appear
- Check `docs/modules.json` syntax
- Ensure `enabled: true`
- Check browser console (F12)

### Flashcards don't load
- Verify filename in `modules.json` matches file in `docs/`
- Check browser console for 404 errors

### Local testing
```bash
# Use a local server, not file:// URLs
python -m http.server 8000
```

## FAQ

**Q: Can I use this for non-OSHA training?**
A: Yes! Any training video → flashcards workflow works.

**Q: How many modules can I add?**
A: Unlimited. The web app dynamically loads any modules in `modules.json`.

**Q: Do I need to know JavaScript?**
A: No. The conversion scripts handle everything. Just add videos!

**Q: Can I make this private?**
A: Yes. Change GitHub repo to private. The web app still works for collaborators.

**Q: What about copyrighted training materials?**
A: Only process videos you have rights to use. Flashcards are for personal/team study.

## Contributing

Pull requests welcome! Especially:
- New conversion scripts
- Additional study modes
- Mobile app improvements
- Documentation

## Support

- **Issues:** https://github.com/PeteSumners/airstreams-flashcards/issues
- **Discussions:** https://github.com/PeteSumners/airstreams-flashcards/discussions

## License

Apache 2.0 - Free to use and modify.

All dependencies are also open source and permissively licensed.

## Credits

Built with:
- OpenCV (video processing)
- Claude Code (OCR & flashcard generation)
- GitHub Pages (hosting)
- Vanilla JavaScript (web app)

Created for **Airstreams Renewables** training in Tehachapi, CA.

---

**Made with ❤️ for better training and safer workplaces**

Good luck with your certifications! 🏗️ ⚡ 🦺
