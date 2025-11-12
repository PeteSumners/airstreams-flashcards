"""Unit tests for OCR engine module."""

import unittest
import numpy as np

from src.config import OCRConfig
from src.ocr_engine import OCRResult, create_ocr_engine


class TestOCRResult(unittest.TestCase):
    """Test cases for OCRResult class."""

    def test_ocr_result_creation(self):
        """Test creating OCRResult object."""
        result = OCRResult(
            text="Hello World",
            confidence=0.95,
            details=[{"text": "Hello World", "confidence": 0.95, "box": []}],
        )

        self.assertEqual(result.text, "Hello World")
        self.assertEqual(result.confidence, 0.95)
        self.assertEqual(len(result.details), 1)

    def test_ocr_result_repr(self):
        """Test OCRResult string representation."""
        result = OCRResult(text="Test", confidence=0.9, details=[])
        repr_str = repr(result)
        self.assertIn("OCRResult", repr_str)
        self.assertIn("0.90", repr_str)


class TestOCREngineFactory(unittest.TestCase):
    """Test cases for OCR engine factory."""

    def test_create_paddleocr_engine(self):
        """Test creating PaddleOCR engine."""
        config = OCRConfig(engine="paddleocr")
        try:
            engine = create_ocr_engine(config)
            self.assertIsNotNone(engine)
            engine.close()
        except ImportError:
            self.skipTest("PaddleOCR not installed")

    def test_create_easyocr_engine(self):
        """Test creating EasyOCR engine."""
        config = OCRConfig(engine="easyocr")
        try:
            engine = create_ocr_engine(config)
            self.assertIsNotNone(engine)
            engine.close()
        except ImportError:
            self.skipTest("EasyOCR not installed")

    def test_invalid_engine(self):
        """Test creating engine with invalid name."""
        config = OCRConfig(engine="invalid_engine")
        with self.assertRaises(ValueError):
            create_ocr_engine(config)


if __name__ == "__main__":
    unittest.main()
