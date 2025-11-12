"""Video frame extraction and processing."""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
import logging

from .config import VideoConfig

logger = logging.getLogger(__name__)


class FrameInfo:
    """Information about an extracted frame."""

    def __init__(
        self,
        frame: np.ndarray,
        frame_number: int,
        timestamp: float,
        quality_score: float,
        motion_score: float = 0.0,
    ):
        self.frame = frame
        self.frame_number = frame_number
        self.timestamp = timestamp
        self.quality_score = quality_score
        self.motion_score = motion_score


class VideoProcessor:
    """Processes video files and extracts frames."""

    def __init__(self, config: VideoConfig):
        self.config = config
        self._previous_frame = None

    def load_video(self, video_path: str) -> cv2.VideoCapture:
        """Load a video file."""
        if not Path(video_path).exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video: {video_path}")

        return cap

    def get_video_info(self, cap: cv2.VideoCapture) -> dict:
        """Get video metadata."""
        return {
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "duration": cap.get(cv2.CAP_PROP_FRAME_COUNT)
            / cap.get(cv2.CAP_PROP_FPS),
        }

    def detect_motion(self, current_frame: np.ndarray) -> Tuple[bool, float]:
        """
        Detect motion between current and previous frame.

        Returns:
            Tuple of (has_motion, motion_score)
        """
        if self._previous_frame is None:
            self._previous_frame = current_frame
            return True, float("inf")

        # Convert to grayscale
        gray_current = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        gray_previous = cv2.cvtColor(self._previous_frame, cv2.COLOR_BGR2GRAY)

        # Compute absolute difference
        frame_diff = cv2.absdiff(gray_current, gray_previous)

        # Calculate motion score (mean of differences)
        motion_score = np.mean(frame_diff)

        # Update previous frame
        self._previous_frame = current_frame.copy()

        has_motion = motion_score > self.config.motion_threshold
        return has_motion, motion_score

    def detect_blur(self, frame: np.ndarray) -> float:
        """
        Detect blur using Laplacian variance.

        Returns:
            Blur score (higher = sharper)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var

    def check_brightness(self, frame: np.ndarray) -> Tuple[bool, float]:
        """
        Check if frame brightness is within acceptable range.

        Returns:
            Tuple of (is_acceptable, brightness_value)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)

        is_acceptable = (
            self.config.min_brightness <= brightness <= self.config.max_brightness
        )
        return is_acceptable, brightness

    def calculate_quality_score(self, frame: np.ndarray) -> float:
        """
        Calculate overall quality score for a frame.

        Returns:
            Quality score (0-100, higher is better)
        """
        scores = []

        # Blur score (normalized)
        if self.config.enable_blur_detection:
            blur_score = self.detect_blur(frame)
            # Normalize: anything above threshold is good
            blur_normalized = min(100, (blur_score / self.config.blur_threshold) * 100)
            scores.append(blur_normalized)

        # Brightness score
        if self.config.enable_brightness_check:
            is_acceptable, brightness = self.check_brightness(frame)
            if is_acceptable:
                # Score based on distance from ideal (128)
                brightness_score = 100 - abs(128 - brightness) / 1.28
                scores.append(brightness_score)
            else:
                scores.append(0)

        if not scores:
            return 100.0  # No quality checks enabled

        return sum(scores) / len(scores)

    def extract_frames(
        self, video_path: str, progress_callback=None
    ) -> List[FrameInfo]:
        """
        Extract frames from video based on configuration.

        Args:
            video_path: Path to video file
            progress_callback: Optional callback function(current, total)

        Returns:
            List of FrameInfo objects
        """
        cap = self.load_video(video_path)
        video_info = self.get_video_info(cap)

        logger.info(f"Processing video: {video_path}")
        logger.info(
            f"Video info: {video_info['width']}x{video_info['height']}, "
            f"{video_info['fps']:.2f} fps, "
            f"{video_info['duration']:.2f}s"
        )

        extracted_frames = []
        fps = video_info["fps"]
        frame_interval_count = int(fps * self.config.frame_interval)

        frame_number = 0
        self._previous_frame = None

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Check max frames limit
                if (
                    self.config.max_frames is not None
                    and len(extracted_frames) >= self.config.max_frames
                ):
                    break

                # Only process frames at specified interval
                if frame_number % frame_interval_count != 0:
                    frame_number += 1
                    continue

                timestamp = frame_number / fps

                # Motion detection
                if self.config.enable_motion_detection:
                    has_motion, motion_score = self.detect_motion(frame)
                    if not has_motion:
                        logger.debug(
                            f"Skipping static frame at {timestamp:.2f}s "
                            f"(motion: {motion_score:.2f})"
                        )
                        frame_number += 1
                        continue
                else:
                    motion_score = 0.0

                # Quality filtering
                quality_score = self.calculate_quality_score(frame)

                if self.config.enable_blur_detection and quality_score < 50:
                    logger.debug(
                        f"Skipping low quality frame at {timestamp:.2f}s "
                        f"(quality: {quality_score:.2f})"
                    )
                    frame_number += 1
                    continue

                # Frame passed all filters
                frame_info = FrameInfo(
                    frame=frame,
                    frame_number=frame_number,
                    timestamp=timestamp,
                    quality_score=quality_score,
                    motion_score=motion_score,
                )
                extracted_frames.append(frame_info)

                logger.debug(
                    f"Extracted frame {len(extracted_frames)} at {timestamp:.2f}s "
                    f"(quality: {quality_score:.2f})"
                )

                if progress_callback:
                    progress_callback(frame_number, video_info["frame_count"])

                frame_number += 1

        finally:
            cap.release()

        logger.info(f"Extracted {len(extracted_frames)} frames from video")
        return extracted_frames

    def save_frame(self, frame_info: FrameInfo, output_path: str):
        """Save a frame to disk."""
        cv2.imwrite(output_path, frame_info.frame)
        logger.debug(f"Saved frame to {output_path}")
