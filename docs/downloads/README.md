# Slide Downloads

This folder contains downloadable zip files of extracted slides from training videos.

## Available Downloads

### OSHA Powerpoint Slides
- **File**: `osha-powerpoint-slides.zip`
- **Size**: 39 MB
- **Slides**: 457 unique slides
- **URL**: https://petesumners.github.io/airstreams-flashcards/downloads/osha-powerpoint-slides.zip

## Using These Files

These zip files contain deduplicated slides extracted from source videos. They're useful for:
- Creating flashcards
- Reference materials
- Study guides
- Presentations

## How Files Are Generated

Files in this folder are automatically created by the `deduplicate_video.py` script when processing source videos.

The script:
1. Extracts frames from the video
2. Removes duplicate frames using perceptual hashing
3. Creates a zip archive of unique slides
4. Copies to this folder for public hosting via GitHub Pages
