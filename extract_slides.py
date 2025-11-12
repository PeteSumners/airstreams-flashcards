#!/usr/bin/env python3
"""
Extract and deduplicate slides from PowerPoint/lecture videos.

Outputs clean images ready for Claude Code to read and extract text.
"""

import logging
import sys
from pathlib import Path
import json

import click
from tqdm import tqdm
import cv2

from src.config import VideoConfig, DeduplicationConfig
from src.video_processor import VideoProcessor
from src.deduplication import FrameDeduplicator


def setup_logging(verbose: bool):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


@click.command()
@click.argument("video_path", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output",
    "output_dir",
    default="slides",
    help="Output directory for extracted slides",
)
@click.option(
    "--threshold",
    "dedup_threshold",
    default=0.95,
    type=float,
    help="Deduplication similarity threshold 0-1 (default: 0.95, higher=keep more)",
)
@click.option(
    "--interval",
    "frame_interval",
    default=1.0,
    type=float,
    help="Extract frame every N seconds (default: 1.0)",
)
@click.option(
    "--method",
    "dedup_method",
    type=click.Choice(["phash", "histogram"], case_sensitive=False),
    default="phash",
    help="Deduplication method (default: phash)",
)
@click.option(
    "--no-dedup",
    is_flag=True,
    help="Disable deduplication (extract all frames)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose logging",
)
def main(
    video_path: str,
    output_dir: str,
    dedup_threshold: float,
    frame_interval: float,
    dedup_method: str,
    no_dedup: bool,
    verbose: bool,
):
    """
    Extract unique slides from PowerPoint/lecture videos.

    \b
    Examples:
        extract_slides.py presentation.mp4
        extract_slides.py lecture.mp4 --threshold 0.98
        extract_slides.py video.mp4 -o my_slides --no-dedup
    """
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    logger.info("🎬 Video Slide Extractor")
    logger.info(f"Processing: {video_path}")
    logger.info(f"Output: {output_dir}")
    logger.info(f"Deduplication: {'disabled' if no_dedup else f'enabled (threshold={dedup_threshold})'}")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Configure video processing
    video_config = VideoConfig(
        frame_interval=frame_interval,
        enable_motion_detection=True,
        motion_threshold=10.0,
        enable_blur_detection=True,
        blur_threshold=150.0,
    )

    # Step 1: Extract frames
    logger.info("\n📹 Step 1: Extracting frames from video...")
    processor = VideoProcessor(video_config)

    pbar = None

    def progress_callback(current, total):
        nonlocal pbar
        if pbar is None:
            pbar = tqdm(total=total, desc="Extracting", unit="frame")
        pbar.n = current
        pbar.refresh()

    try:
        frames = processor.extract_frames(video_path, progress_callback)
        if pbar:
            pbar.close()

        logger.info(f"✓ Extracted {len(frames)} frames")

        # Step 2: Deduplicate
        if not no_dedup:
            logger.info(f"\n🔄 Step 2: Deduplicating frames (method={dedup_method})...")
            deduplicator = FrameDeduplicator(
                similarity_threshold=dedup_threshold,
                method=dedup_method,
                hash_size=8,
            )

            unique_frames = deduplicator.deduplicate_sequential(
                frames, window_size=10
            )

            logger.info(
                f"✓ Removed {len(frames) - len(unique_frames)} duplicates, "
                f"{len(unique_frames)} unique slides found"
            )
            frames = unique_frames
        else:
            logger.info("\n⏭️  Step 2: Skipping deduplication")

        # Step 3: Save frames
        logger.info(f"\n💾 Step 3: Saving {len(frames)} slides...")
        video_name = Path(video_path).stem

        for idx, frame_info in enumerate(tqdm(frames, desc="Saving", unit="slide")):
            output_file = output_path / f"slide_{idx + 1:04d}.jpg"
            cv2.imwrite(str(output_file), frame_info.frame)

        # Save metadata
        metadata = {
            "video": video_path,
            "total_slides": len(frames),
            "settings": {
                "deduplication_enabled": not no_dedup,
                "similarity_threshold": dedup_threshold,
                "frame_interval": frame_interval,
                "method": dedup_method,
            },
            "slides": [
                {
                    "number": idx + 1,
                    "file": f"slide_{idx + 1:04d}.jpg",
                    "timestamp": frame_info.timestamp,
                    "quality_score": frame_info.quality_score,
                }
                for idx, frame_info in enumerate(frames)
            ],
        }

        metadata_file = output_path / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

        # Print summary
        print("\n" + "=" * 60)
        print("✅ EXTRACTION COMPLETE!")
        print("=" * 60)
        print(f"Video: {video_path}")
        print(f"Slides extracted: {len(frames)}")
        if not no_dedup:
            print(f"Duplicates removed: {metadata['total_slides'] - len(frames)}")
            print(f"Similarity threshold: {dedup_threshold}")
        print(f"\n📁 Output directory: {output_path.absolute()}")
        print(f"   - {len(frames)} slide images")
        print(f"   - metadata.json with slide info")
        print("\n🤖 Next step: Ask Claude Code to read the slides!")
        print(f'   "Please read all images in {output_path.absolute()} and extract the text from each slide"')
        print("=" * 60)

    except Exception as e:
        logger.error(f"Error processing video: {e}", exc_info=verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()
