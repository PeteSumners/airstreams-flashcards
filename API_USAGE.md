# API Usage Guide

Automate slide processing with Claude API.

## Setup

1. **Install dependencies:**
```bash
pip install anthropic
```

2. **Get your API key:**
   - Go to https://console.anthropic.com/
   - Create an API key
   - Set it as an environment variable:

```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "your-api-key-here"

# Windows (CMD)
set ANTHROPIC_API_KEY=your-api-key-here

# Linux/Mac
export ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

### Full Workflow

```bash
# Step 1: Extract slides from video
python extract_slides.py presentation.mp4

# Step 2: Process with Claude API
python process_slides_api.py slides/
```

### Extract Text from Each Slide

```bash
# Process individually (detailed per-slide output)
python process_slides_api.py slides/ -o text.txt --mode extract

# Batch processing (faster, cheaper)
python process_slides_api.py slides/ -o text.txt --mode extract --batch
```

Output format (individual mode):
```
=== Slide 1: slide_0001.jpg ===

[Text from slide 1]

=== Slide 2: slide_0002.jpg ===

[Text from slide 2]
```

### Summarize Entire Presentation

```bash
# Get a comprehensive summary (recommended)
python process_slides_api.py slides/ -o summary.txt --mode summarize --batch
```

Output: A single comprehensive summary of the entire presentation including main themes, key points, and takeaways.

## Options

```
Options:
  -o, --output FILE          Output file (default: presentation_summary.txt)
  --mode [extract|summarize] Extract text or summarize (default: extract)
  --batch                    Process all slides in one request (faster, cheaper)
  --model TEXT              Claude model to use (default: claude-sonnet-4-5)
  --api-key TEXT            API key (or set ANTHROPIC_API_KEY env var)
```

## Cost Considerations

**Claude Sonnet 4.5 Pricing (as of 2025):**
- Input: $3 per million tokens
- Output: $15 per million tokens

**Batch vs Individual:**
- **Batch mode** (recommended): All slides in 1 request
  - Faster
  - Cheaper
  - Better context for summaries
  - Example: 50 slides ≈ 1 request

- **Individual mode**: Each slide = 1 request
  - More detailed per-slide output
  - Good for extraction when you need separate entries
  - Example: 50 slides ≈ 50 requests

**Estimate for a 50-slide presentation:**
- Batch mode: ~$0.50 - $2.00
- Individual mode: ~$5.00 - $10.00

## Examples

### Example 1: Quick Summary

```bash
# Extract slides
python extract_slides.py lecture.mp4 -o slides

# Get summary
python process_slides_api.py slides/ -o summary.txt --mode summarize --batch
```

### Example 2: Detailed Text Extraction

```bash
# Extract slides with conservative dedup
python extract_slides.py presentation.mp4 --threshold 0.98

# Extract text from each slide
python process_slides_api.py slides/ -o full_text.txt --mode extract --batch
```

### Example 3: Book Pages

```bash
# Extract book pages from video
python extract_slides.py book_flip.mp4 --threshold 0.90 -o pages

# Extract text with per-page detail
python process_slides_api.py pages/ -o book_text.txt --mode extract
```

## Python API Usage

You can also use it programmatically:

```python
from pathlib import Path
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Process a single slide
from process_slides_api import process_slide

result = process_slide(
    client,
    Path("slides/slide_0001.jpg"),
    prompt="Extract all text from this slide",
)
print(result)

# Process all slides in batch
from process_slides_api import process_slides_batch

slides = sorted(Path("slides").glob("*.jpg"))
summary = process_slides_batch(
    client,
    slides,
    prompt="Summarize this presentation",
)
print(summary)
```

## Advantages

✅ **Fully automated** - No manual interaction needed
✅ **Batch processing** - Process entire presentations at once
✅ **High accuracy** - Claude's vision is excellent at reading slides
✅ **Flexible output** - Extract text or generate summaries
✅ **Cost effective** - Batch mode minimizes API costs
✅ **Scalable** - Process hundreds of presentations programmatically

## Tips

- Use **batch mode with summarize** for quick presentation overviews
- Use **individual mode with extract** when you need per-slide text separation
- Adjust `--threshold` in extract_slides.py if you're getting too many/few slides
- Set `ANTHROPIC_API_KEY` in your environment to avoid passing it each time
- Check your API usage at https://console.anthropic.com/

## Troubleshooting

**"API key not found"**
```bash
# Make sure to set the environment variable
export ANTHROPIC_API_KEY=your-key-here
```

**"No images found"**
```bash
# Make sure you've extracted slides first
python extract_slides.py your_video.mp4
```

**"Rate limit exceeded"**
- Add delays between requests in individual mode
- Use batch mode to reduce number of API calls
