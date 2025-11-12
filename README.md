# Training Video Flashcards

Extract slides from training presentation videos and convert them into flashcards for study and sharing.

Perfect for creating study materials from safety training, OSHA courses, technical training, and any video-based presentations. Designed for Airstreams Renewables training in Tehachapi, CA.

## Why This Tool?

Training videos contain tons of information, but it's hard to study from them. This tool:

1. **Extracts all unique slides** from your training videos automatically
2. **Removes duplicates** so you only get unique content
3. **Makes flashcards easy to create** - extracted slides are ready for OCR and conversion
4. **Shareable** - Export text-based flashcards perfect for GroupMe, text messages, or study groups

## Quick Start

### Extract Slides from a Training Video

```bash
# Process a full training video
python deduplicate_video.py "OSHA Powerpoint.mp4"

# Adjust sensitivity (0.97 is good for most training videos)
python deduplicate_video.py "Safety Training.mp4" 0.97
```

This will create:
- `test_output/1_before_dedup/` - All extracted frames
- `test_output/2_after_dedup/` - Unique slides only

### Create Flashcards

Once you have extracted slides, use Claude Code to convert them to flashcards:

```
Please read all the slides in test_output/2_after_dedup/ and create
flashcards in Q&A format. Make them easy to share in GroupMe.
```

Claude will create text-based flashcards you can easily copy/paste into:
- GroupMe chats with your training cohort
- Text messages
- Study notes
- Anki or Quizlet

## Features

- **Full Video Processing**: Processes entire training videos (no frame limits)
- **Smart Deduplication**: Removes duplicate slides while keeping all unique content
- **Conservative Settings**: Set to capture all training content (threshold 0.97)
- **Minimal Filtering**: Disabled motion/blur detection to ensure no slides are missed
- **High Quality Output**: Saves slides as clear JPG images ready for OCR

## Installation

```bash
pip install -r requirements.txt
```

No C++ compilers needed - just Python and OpenCV!

## Usage Examples

### Basic Usage

```bash
# Process your training video
python deduplicate_video.py "OSHA Fall Protection.mp4"
```

### Custom Settings

```bash
# More aggressive deduplication (removes more similar slides)
python deduplicate_video.py "Training.mp4" 0.95

# More conservative (keeps more slides - better for training)
python deduplicate_video.py "Training.mp4" 0.99

# Limit number of frames (for testing)
python deduplicate_video.py "Training.mp4" 0.97 200
```

### Parameters

```
python deduplicate_video.py <video_file> [threshold] [max_frames]

  video_file    - Path to your training video
  threshold     - Similarity threshold (default: 0.90, recommend 0.97 for training)
  max_frames    - Max frames to process (default: None = process entire video)
```

### Threshold Guide

- **0.99**: Ultra-conservative - keeps almost everything (may have near-duplicates)
- **0.97**: Recommended for training videos - good balance
- **0.95**: Balanced - removes obvious duplicates
- **0.90**: Aggressive - may remove some similar but unique slides

**For training videos, use 0.97 or higher** to ensure you don't miss any content.

## Output

After running, you'll get organized directories:

```
test_output/
├── 1_before_dedup/          # All extracted frames
│   └── frame_0000.jpg ... frame_NNNN.jpg
└── 2_after_dedup/           # Unique slides only (use these!)
    └── unique_0000.jpg ... unique_NNNN.jpg
```

Use the files in `2_after_dedup/` for your flashcards.

## Creating Shareable Flashcards

### For GroupMe / Text Sharing

Extract slides, then ask Claude:

```
Read all slides in test_output/2_after_dedup/ and create flashcards.
Format them as:

Q: [Question based on slide content]
A: [Answer]

Make them concise and easy to share in GroupMe.
```

### For Anki or Quizlet

```
Read all slides and create flashcards in CSV format:
Question,Answer
[content from slide 1]
[content from slide 2]
```

## Example Workflow

1. **Extract slides from your training video**:
   ```bash
   python deduplicate_video.py "OSHA 10HR Fall Hazards.mp4" 0.97
   ```

2. **Review the output**:
   - Check `test_output/2_after_dedup/`
   - You should see all unique slides from the training

3. **Create flashcards with Claude**:
   ```
   Please create study flashcards from the slides in test_output/2_after_dedup/.
   Make them in Q&A format, suitable for sharing in GroupMe with my training group.
   ```

4. **Share with your group**:
   - Copy the flashcards
   - Paste into GroupMe
   - Help everyone study!

## Use Cases

- OSHA 10-hour/30-hour training courses
- Safety certification training
- Technical training presentations
- Company onboarding videos
- Any PowerPoint-style training video

## Project Structure

```
training-video-flashcards/
├── src/                     # Core processing code
│   ├── config.py           # Video and deduplication config
│   ├── video_processor.py  # Frame extraction
│   └── deduplication.py    # Smart deduplication
├── deduplicate_video.py    # Main tool (use this!)
├── extract_slides.py       # Alternative extraction tool
├── process_slides_api.py   # Automated OCR with Claude API
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Advanced: Automated Flashcard Creation

For batch processing with the Claude API:

```bash
# Extract slides
python deduplicate_video.py "Training.mp4" 0.97

# Auto-generate flashcards using Claude API
python process_slides_api.py test_output/2_after_dedup/ -o flashcards.txt --mode summarize
```

Requires: `ANTHROPIC_API_KEY` environment variable. See `API_USAGE.md` for details.

## Troubleshooting

### Too many duplicate slides in output

Lower the threshold:
```bash
python deduplicate_video.py video.mp4 0.95
```

### Missing some slides from the training

Raise the threshold:
```bash
python deduplicate_video.py video.mp4 0.99
```

When in doubt, **use 0.97** - it's a good balance for training content.

## Technical Details

### How It Works

1. **Frame Extraction**: Samples video every 0.9 seconds
2. **No Filtering**: Motion and blur detection disabled to capture all content
3. **Perceptual Hashing**: Compares frames using phash algorithm
4. **Sequential Deduplication**: Compares frames in sequence within a sliding window
5. **Quality Output**: Saves unique frames as high-quality JPGs

### Why This Approach?

Traditional OCR libraries (PaddleOCR, EasyOCR) require C++ compilation which is problematic on Windows. Instead:
- ✅ Extract and deduplicate slides (fast, automated)
- ✅ Use Claude for OCR (accurate, understands context)
- ✅ Create shareable flashcards (perfect for GroupMe)

## Built For

**Airstreams Renewables Training** - Tehachapi, CA

Making it easier to study and share training materials with your cohort!

## License

Apache 2.0 - See LICENSE file.

## Contributing

Pull requests welcome! This tool is designed to help training cohorts learn together.
