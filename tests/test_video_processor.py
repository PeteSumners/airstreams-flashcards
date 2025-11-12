"""Unit tests for video processor module."""

import unittest
import numpy as np
import cv2

from src.config import VideoConfig
from src.video_processor import VideoProcessor, FrameInfo


class TestVideoProcessor(unittest.TestCase):
    """Test cases for VideoProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = VideoConfig()
        self.processor = VideoProcessor(self.config)

    def test_detect_blur(self):
        """Test blur detection."""
        # Create a sharp test image
        sharp_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.rectangle(sharp_image, (25, 25), (75, 75), (255, 255, 255), -1)

        blur_score = self.processor.detect_blur(sharp_image)
        self.assertGreater(blur_score, 0)

    def test_check_brightness(self):
        """Test brightness checking."""
        # Create bright image
        bright_image = np.ones((100, 100, 3), dtype=np.uint8) * 200

        is_acceptable, brightness = self.processor.check_brightness(bright_image)
        self.assertTrue(is_acceptable)
        self.assertGreater(brightness, 150)

    def test_detect_motion(self):
        """Test motion detection."""
        # Create two different frames
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2 = np.ones((100, 100, 3), dtype=np.uint8) * 100

        self.processor._previous_frame = None
        has_motion1, score1 = self.processor.detect_motion(frame1)
        self.assertTrue(has_motion1)  # First frame always has motion

        has_motion2, score2 = self.processor.detect_motion(frame2)
        self.assertIsInstance(has_motion2, bool)
        self.assertGreater(score2, 0)

    def test_calculate_quality_score(self):
        """Test quality score calculation."""
        # Create test image
        test_image = np.random.randint(50, 200, (100, 100, 3), dtype=np.uint8)

        quality_score = self.processor.calculate_quality_score(test_image)
        self.assertGreaterEqual(quality_score, 0)
        self.assertLessEqual(quality_score, 100)


class TestFrameInfo(unittest.TestCase):
    """Test cases for FrameInfo class."""

    def test_frame_info_creation(self):
        """Test creating FrameInfo object."""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame_info = FrameInfo(
            frame=frame,
            frame_number=0,
            timestamp=0.0,
            quality_score=85.0,
            motion_score=10.0,
        )

        self.assertEqual(frame_info.frame_number, 0)
        self.assertEqual(frame_info.timestamp, 0.0)
        self.assertEqual(frame_info.quality_score, 85.0)
        self.assertEqual(frame_info.motion_score, 10.0)


if __name__ == "__main__":
    unittest.main()
