# Changelog

## Version 2.0 - Multi-Module Release (2025-11-13)

### Major Changes

**Split OSHA 10HR Training into 11 Separate Modules**

The original single "Fall Hazards" module (which actually contained all OSHA content) has been restructured into 11 focused modules for better learning:

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

**Total: 371 flashcards** (previously reported as 141, but all content was already there)

### New Features

- **Contact Email Added**: petesumners@outlook.com for flashcard submissions and corrections
- **Community Submissions**: Users can now submit corrections or new flashcards via email
- **Better Organization**: Each module can be studied independently
- **Updated Documentation**: README now reflects true card counts and all modules

### Technical Changes

- Created `split_modules.py` script to automate module separation
- Created `convert_all_modules.py` to batch-convert all modules to web and Quizlet formats
- Updated `docs/modules.json` with all 11 modules and contact information
- Removed unused OCR infrastructure files (src/, tests/, utils/)
- Removed OCR-related documentation (ROADMAP.md, PROJECT_STATUS.md, etc.)
- Archived original combined flashcards file to `modules/_ARCHIVE_OSHA_Flashcards_FULL.txt`

### Files Removed

- `src/` - OCR engine code (not needed, use Claude for text extraction)
- `tests/` - Unit tests for OCR code
- `utils/` - OCR utility scripts
- `setup.py`, `video_ocr.py`, `example_usage.py` - OCR system files
- `ROADMAP.md`, `PROJECT_STATUS.md`, `QUICKSTART.md`, `API_USAGE.md` - OCR documentation
- `CONTRIBUTING.md`, `Makefile`, `run.bat` - Development files
- `anki-installer.exe` - No longer using Anki
- `powerpoint_test.mp4` - Test video

### Files Kept

- `deduplicate_video.py` - Still useful for extracting unique slides from videos
- `add_module.py` - Automation script for adding new modules
- `scripts/create_quizlet_format.py` - Convert flashcards to Quizlet TSV
- `scripts/convert_to_web_format.py` - Convert flashcards to JavaScript for web app
- `docs/` - Complete web application
- `modules/` - All flashcard source files (now properly organized)
- `source-videos/` - Training video source files

### Migration Notes

**For Users:**
- No action needed! All flashcards are still available
- You now have 11 modules instead of 1 giant module
- Each module can be studied separately or all together

**For Developers:**
- Run `python split_modules.py` to recreate modules from archive if needed
- Run `python convert_all_modules.py` to regenerate all web + Quizlet formats
- Module structure: `modules/<module-id>/flashcards.txt`
- Web format: `docs/flashcards-<module-id>.js`
- Quizlet format: `modules/<module-id>/flashcards_quizlet.txt`

---

## Version 1.0 - Initial Release

- Single module with all OSHA 10HR content
- Web-based flashcard system
- Quizlet export support
- Video slide extraction with deduplication
- GitHub Pages hosting
