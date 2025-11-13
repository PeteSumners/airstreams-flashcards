# Quick Start: Add a Training Module

Super simple! Just 3 steps:

## 1. Drop Your Video

Put your training video in the `training-videos/` folder:

```
training-videos/
└── Electrical-Safety.mp4  ← Your video here
```

## 2. Run One Command

```bash
python add_module.py
```

The script will:
- ✅ Find your video automatically
- ✅ Ask you a few simple questions
- ✅ Extract all the slides
- ✅ Pause for you to generate flashcards with Claude
- ✅ Convert to all formats (web, Quizlet)
- ✅ Update the module configuration
- ✅ Push to GitHub (optional)

## 3. Generate Flashcards with Claude

When the script pauses, tell Claude Code:

```
Please read all slides in test_output/2_after_dedup/ and create
flashcards for [Your Module Name].

Format as Q&A pairs:
Q: Question here
A: Answer here

Focus on testable knowledge, regulations, and key concepts.
Save to: modules/[module-id]/flashcards.txt
```

Press Enter when done, and the script handles the rest!

---

## Example Session

```bash
$ python add_module.py

============================================================
Airstreams Training - Add New Module
============================================================

Step 1: Select Training Video
----------------------------------------
Found videos:
  1. Electrical-Safety.mp4

✅ Auto-selected: Electrical-Safety.mp4

============================================================
Step 2: Module Information
============================================================

Module ID [electrical-safety]:
Module Title [Electrical Safety]:
Short description: OSHA electrical hazards and safety procedures

============================================================
Step 3: Extract Slides from Video
============================================================

Deduplication threshold [0.97]:
⏳ Extracting slides from video...
✅ Extracting slides from video - Done!
📊 Extracted 127 unique slides

============================================================
Step 4: Generate Flashcards with Claude
============================================================

Next step: Use Claude Code to create flashcards

Tell Claude:
"""
Please read all slides in test_output/2_after_dedup/ and create
flashcards for Electrical Safety.

Format as Q&A pairs:
Q: Question here
A: Answer here

Focus on testable knowledge, regulations, and key concepts.
Save to: modules/electrical-safety/flashcards.txt
"""

✋ Press Enter once you've created the flashcards...

[You create the flashcards with Claude, then press Enter]

✅ Found 95 flashcards

============================================================
Step 6: Convert to Web Format
============================================================

⏳ Creating Quizlet format...
✅ Creating Quizlet format - Done!
⏳ Creating web format...
✅ Creating web format - Done!

============================================================
Step 7: Update Module Configuration
============================================================

✅ Added module to configuration

============================================================
🎉 Module Added Successfully!
============================================================

Module ID: electrical-safety
Title: Electrical Safety
Flashcards: 95

Files created:
  • modules/electrical-safety/flashcards.txt
  • modules/electrical-safety/flashcards_quizlet.txt
  • docs/flashcards-electrical-safety.js

Updated:
  • docs/modules.json

============================================================
Step 9: Publish to GitHub
============================================================

Ready to publish?
Push to GitHub? (y/n) [y]: y

⏳ Publishing to GitHub...
✅ Published to GitHub!

🌐 Live in ~2 minutes at:
   https://petesumners.github.io/airstreams-flashcards/

============================================================
✨ All Done!
============================================================

Share with your cohort:
https://petesumners.github.io/airstreams-flashcards/?module=electrical-safety
```

---

## That's It!

No manual file editing. No command-line juggling. Just:

1. **Drop video** in `training-videos/`
2. **Run** `python add_module.py`
3. **Generate flashcards** with Claude when prompted
4. **Done!**

Your module is live and ready to share!

---

## Tips

- **Video Format:** Works with MP4, AVI, MOV, MKV, WMV
- **Threshold:** 0.97 is good for most training videos (keeps all content)
- **Module ID:** Auto-generated from video filename (lowercase-with-hyphens)
- **Flashcards:** Claude Code creates them in seconds - just copy/paste the template

---

## Troubleshooting

**Script can't find video?**
- Check the video is in `training-videos/` folder
- Make sure it has a common video extension (.mp4, etc)

**No slides extracted?**
- Video might be corrupted or in unsupported format
- Try converting to MP4 first

**Flashcards not found?**
- Make sure Claude saved to the exact path shown
- Check the file exists: `modules/[module-id]/flashcards.txt`

**Push failed?**
- Run manually: `git push origin master`
- You might need to authenticate with GitHub first

---

## Manual Method

If you prefer doing it step-by-step yourself, see [ADD_NEW_MODULE.md](ADD_NEW_MODULE.md) for the detailed manual process.
