#!/usr/bin/env python3
"""
Generate a simple test video with text for testing the OCR system.

This creates a video with text slides that can be used to verify
the OCR pipeline works correctly.
"""

import cv2
import numpy as np
from pathlib import Path


def create_text_frame(text: str, size=(1280, 720), bg_color=(255, 255, 255)):
    """Create a frame with text."""
    frame = np.full((size[1], size[0], 3), bg_color, dtype=np.uint8)

    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    thickness = 3
    color = (0, 0, 0)

    # Calculate text size and position
    lines = text.split('\n')
    y_offset = size[1] // 2 - (len(lines) * 60) // 2

    for i, line in enumerate(lines):
        text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
        x = (size[0] - text_size[0]) // 2
        y = y_offset + i * 60

        cv2.putText(frame, line, (x, y), font, font_scale, color, thickness)

    return frame


def generate_test_video(
    output_path: str = "test_video.mp4",
    fps: int = 30,
    duration_per_slide: int = 3,
):
    """
    Generate a test video with multiple text slides.

    Args:
        output_path: Path to save the video
        fps: Frames per second
        duration_per_slide: How long to show each slide (seconds)
    """
    # Define test slides
    slides = [
        "Video OCR Test\nSlide 1",
        "The quick brown fox\njumps over the lazy dog",
        "Machine Learning\nArtificial Intelligence\nComputer Vision",
        "1234567890\nABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz",
        "Python Programming\nOpenCV + OCR\nAutomation",
        "Test Complete\nThank You!",
    ]

    # Video properties
    size = (1280, 720)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Create video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, size)

    if not out.isOpened():
        raise RuntimeError(f"Failed to create video: {output_path}")

    print(f"Generating test video: {output_path}")
    print(f"  Resolution: {size[0]}x{size[1]}")
    print(f"  FPS: {fps}")
    print(f"  Slides: {len(slides)}")
    print(f"  Duration per slide: {duration_per_slide}s")

    frames_per_slide = fps * duration_per_slide
    total_frames = frames_per_slide * len(slides)

    # Generate video
    for slide_idx, slide_text in enumerate(slides):
        print(f"  Creating slide {slide_idx + 1}/{len(slides)}: {slide_text.split()[0]}...")

        # Create frame for this slide
        frame = create_text_frame(slide_text, size)

        # Write frame multiple times
        for _ in range(frames_per_slide):
            out.write(frame)

    out.release()

    # Verify file was created
    if Path(output_path).exists():
        file_size = Path(output_path).stat().st_size / 1024 / 1024  # MB
        print(f"\n✓ Video created successfully!")
        print(f"  Path: {Path(output_path).absolute()}")
        print(f"  Size: {file_size:.2f} MB")
        print(f"  Duration: {len(slides) * duration_per_slide}s")
        print(f"  Total frames: {total_frames}")
    else:
        print("\n✗ Failed to create video file")


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate test video for OCR system"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="test_video.mp4",
        help="Output video path (default: test_video.mp4)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second (default: 30)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=3,
        help="Duration per slide in seconds (default: 3)",
    )

    args = parser.parse_args()

    try:
        generate_test_video(
            output_path=args.output,
            fps=args.fps,
            duration_per_slide=args.duration,
        )
        print("\nYou can now test the OCR system with:")
        print(f"  python video_ocr.py {args.output}")
    except Exception as e:
        print(f"\nError: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
