#!/usr/bin/env python3
"""
Test frame deduplication WITHOUT OCR.

This lets you test the deduplication feature immediately
without waiting for PaddleOCR/EasyOCR to install.
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


def test_deduplication(
    video_path: str,
    output_dir: str = "test_output",
    similarity_threshold: float = 0.90,
    max_frames: int = 50
):
    """Test deduplication on a video."""
    logger.info(f"Testing deduplication on: {video_path}")
    logger.info(f"Similarity threshold: {similarity_threshold}")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Configure
    video_config = VideoConfig(
        frame_interval=1.0,
        max_frames=max_frames,
        enable_motion_detection=True,
        motion_threshold=10.0,
        enable_blur_detection=True,
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
    print("DEDUPLICATION TEST RESULTS")
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
        print("Usage: python test_dedup_only.py <video_file> [threshold] [max_frames]")
        print("\nExamples:")
        print("  python test_dedup_only.py powerpoint_test.mp4")
        print("  python test_dedup_only.py powerpoint_test.mp4 0.95")
        print("  python test_dedup_only.py powerpoint_test.mp4 0.98 100")
        print("\nThreshold guide:")
        print("  0.80-0.85 = Aggressive (removes similar slides)")
        print("  0.90      = Default (balanced)")
        print("  0.95-0.98 = Conservative (keeps more slides)")
        sys.exit(1)

    video_path = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.90
    max_frames = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    if not Path(video_path).exists():
        print(f"Error: Video file not found: {video_path}")
        sys.exit(1)

    test_deduplication(video_path, similarity_threshold=threshold, max_frames=max_frames)
