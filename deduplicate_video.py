#!/usr/bin/env python3
"""
Frame deduplication for full videos WITHOUT OCR.

Processes entire videos to extract and deduplicate frames.
Saves both the original extracted frames and deduplicated unique frames.
"""

import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

try:
    from src.config import VideoConfig, DeduplicationConfig
    from src.video_processor import VideoProcessor
    from src.deduplication import FrameDeduplicator
    import cv2
except ImportError as e:
    logger.error(f"Missing dependency: {e}")
    logger.error("Run: pip install opencv-python")
    sys.exit(1)


def deduplicate_video(
    video_path: str,
    output_dir: str = "test_output",
    similarity_threshold: float = 0.90,
    max_frames: int = None
):
    """Deduplicate frames from a full video."""
    logger.info(f"Processing video: {video_path}")
    logger.info(f"Similarity threshold: {similarity_threshold}")
    if max_frames:
        logger.info(f"Max frames limit: {max_frames}")
    else:
        logger.info("Processing entire video (no frame limit)")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Configure - minimal filtering to capture all frames
    video_config = VideoConfig(
        frame_interval=0.9,  # Slightly more frequent to capture more frames
        max_frames=max_frames,
        enable_motion_detection=False,  # Disable to capture all frames
        motion_threshold=5.0,
        enable_blur_detection=False,  # Disable blur detection to get all frames
        blur_threshold=100.0,
    )

    dedup_config = DeduplicationConfig(
        enable_deduplication=True,
        similarity_threshold=similarity_threshold,
        method="phash",
        use_sequential=True,
        window_size=10,
    )

    # Step 1: Extract frames
    logger.info("Step 1: Extracting frames...")
    processor = VideoProcessor(video_config)
    frames = processor.extract_frames(video_path)
    logger.info(f"Extracted {len(frames)} frames")

    # Save extracted frames
    frames_before = output_path / "1_before_dedup"
    frames_before.mkdir(exist_ok=True)
    for idx, frame_info in enumerate(frames):
        frame_path = frames_before / f"frame_{idx:04d}.jpg"
        cv2.imwrite(str(frame_path), frame_info.frame)
    logger.info(f"Saved {len(frames)} frames to {frames_before}")

    # Step 2: Deduplicate
    logger.info("\nStep 2: Deduplicating frames...")
    deduplicator = FrameDeduplicator(
        similarity_threshold=dedup_config.similarity_threshold,
        method=dedup_config.method,
        hash_size=dedup_config.hash_size,
    )

    if dedup_config.use_sequential:
        unique_frames = deduplicator.deduplicate_sequential(
            frames, window_size=dedup_config.window_size
        )
    else:
        unique_frames = deduplicator.deduplicate(frames)

    logger.info(f"After deduplication: {len(unique_frames)} unique frames")
    logger.info(f"Removed {len(frames) - len(unique_frames)} duplicate frames")

    # Save unique frames
    frames_after = output_path / "2_after_dedup"
    frames_after.mkdir(exist_ok=True)
    for idx, frame_info in enumerate(unique_frames):
        frame_path = frames_after / f"unique_{idx:04d}.jpg"
        cv2.imwrite(str(frame_path), frame_info.frame)
    logger.info(f"Saved {len(unique_frames)} unique frames to {frames_after}")

    # Summary
    print("\n" + "=" * 60)
    print("VIDEO DEDUPLICATION RESULTS")
    print("=" * 60)
    print(f"Input video: {video_path}")
    print(f"Frames extracted: {len(frames)}")
    print(f"Unique frames: {len(unique_frames)}")
    print(f"Duplicates removed: {len(frames) - len(unique_frames)}")
    print(f"Reduction: {(1 - len(unique_frames)/len(frames))*100:.1f}%")
    print(f"\nOutput saved to: {output_path.absolute()}")
    print(f"  - Before dedup: {frames_before}/")
    print(f"  - After dedup: {frames_after}/")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deduplicate_video.py <video_file> [threshold] [max_frames]")
        print("\nExamples:")
        print("  python deduplicate_video.py presentation.mp4")
        print("  python deduplicate_video.py presentation.mp4 0.95")
        print("  python deduplicate_video.py presentation.mp4 0.98 100")
        print("\nParameters:")
        print("  video_file    - Path to the video file to process")
        print("  threshold     - Similarity threshold (default: 0.90)")
        print("  max_frames    - Max frames to process (default: None = process all)")
        print("\nThreshold guide:")
        print("  0.80-0.85 = Aggressive (removes similar slides)")
        print("  0.90      = Default (balanced)")
        print("  0.95-0.98 = Conservative (keeps more slides)")
        sys.exit(1)

    video_path = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.90
    max_frames = int(sys.argv[3]) if len(sys.argv) > 3 else None

    if not Path(video_path).exists():
        print(f"Error: Video file not found: {video_path}")
        sys.exit(1)

    deduplicate_video(video_path, similarity_threshold=threshold, max_frames=max_frames)
