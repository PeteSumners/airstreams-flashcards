# Quick Start Guide

Get slides from your PowerPoint/lecture videos in 2 simple steps!

## Step 1: Extract Slides

```bash
python extract_slides.py your_presentation.mp4
```

Done! Your unique slides are now in the `slides/` directory.

## Step 2: Read with Claude

### Option A: Interactive (Claude Code)

Tell Claude Code:

```
Please read all images in the slides/ directory and extract the text from each slide.
Save everything to presentation_text.txt
```

### Option B: Automated (Claude API)

```bash
# Install the API client
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY=your-key-here

# Summarize the presentation
python process_slides_api.py slides/ -o summary.txt --mode summarize --batch
```

See `API_USAGE.md` for more details.

That's it! 🎉

## Common Use Cases

### PowerPoint Presentation

```bash
python extract_slides.py presentation.mp4 --threshold 0.95
```

### Lecture Video

```bash
python extract_slides.py lecture.mp4 --interval 2.0 --threshold 0.98
```

### Book Page Flipping

```bash
python extract_slides.py book_video.mp4 --threshold 0.90
```

## Tips

- **Too many duplicates?** Lower threshold: `--threshold 0.90`
- **Missing slides?** Raise threshold: `--threshold 0.98`
- **Want ALL frames?** Disable dedup: `--no-dedup`

## What You Get

After running extract_slides.py:
- `slides/slide_0001.jpg` - First slide
- `slides/slide_0002.jpg` - Second slide
- etc.
- `slides/metadata.json` - Slide info

Then Claude reads them and gives you the text!

## Advantages

- ✅ No OCR installation headaches
- ✅ Works on any OS
- ✅ Handles any language
- ✅ Understands layout and context
- ✅ Can summarize or reorganize content

Ready? Run your first extraction now!
