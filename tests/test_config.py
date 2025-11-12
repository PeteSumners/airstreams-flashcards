"""Unit tests for configuration module."""

import unittest

from src.config import Config, VideoConfig, OCRConfig, OutputConfig


class TestVideoConfig(unittest.TestCase):
    """Test cases for VideoConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = VideoConfig()
        self.assertEqual(config.frame_interval, 1.0)
        self.assertIsNone(config.max_frames)
        self.assertTrue(config.enable_motion_detection)
        self.assertTrue(config.enable_blur_detection)

    def test_custom_values(self):
        """Test custom configuration values."""
        config = VideoConfig(
            frame_interval=2.0,
            max_frames=100,
            motion_threshold=10.0,
        )
        self.assertEqual(config.frame_interval, 2.0)
        self.assertEqual(config.max_frames, 100)
        self.assertEqual(config.motion_threshold, 10.0)


class TestOCRConfig(unittest.TestCase):
    """Test cases for OCRConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = OCRConfig()
        self.assertEqual(config.engine, "paddleocr")
        self.assertEqual(config.languages, ["en"])
        self.assertFalse(config.use_gpu)
        self.assertEqual(config.confidence_threshold, 0.5)

    def test_custom_languages(self):
        """Test custom language configuration."""
        config = OCRConfig(languages=["en", "fr", "es"])
        self.assertEqual(len(config.languages), 3)
        self.assertIn("fr", config.languages)


class TestOutputConfig(unittest.TestCase):
    """Test cases for OutputConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = OutputConfig()
        self.assertEqual(config.output_dir, "output")
        self.assertTrue(config.save_frames)
        self.assertTrue(config.save_text)
        self.assertTrue(config.save_json)
        self.assertFalse(config.save_pdf)


class TestConfig(unittest.TestCase):
    """Test cases for main Config."""

    def test_default_initialization(self):
        """Test default configuration initialization."""
        config = Config()
        self.assertIsInstance(config.video, VideoConfig)
        self.assertIsInstance(config.ocr, OCRConfig)
        self.assertIsInstance(config.output, OutputConfig)

    def test_custom_initialization(self):
        """Test custom configuration initialization."""
        video_config = VideoConfig(frame_interval=2.0)
        ocr_config = OCRConfig(engine="easyocr")
        output_config = OutputConfig(output_dir="results")

        config = Config(
            video=video_config,
            ocr=ocr_config,
            output=output_config,
        )

        self.assertEqual(config.video.frame_interval, 2.0)
        self.assertEqual(config.ocr.engine, "easyocr")
        self.assertEqual(config.output.output_dir, "results")


if __name__ == "__main__":
    unittest.main()
