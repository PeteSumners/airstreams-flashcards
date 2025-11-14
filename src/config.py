"""Configuration management for Video OCR System."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoConfig:
    """Video processing configuration."""

    # Frame extraction
    frame_interval: float = 1.0  # Extract frame every N seconds
    max_frames: Optional[int] = None  # Maximum frames to extract (None = all)

    # Motion detection
    enable_motion_detection: bool = True
    motion_threshold: float = 5.0  # Threshold for detecting motion

    # Quality filtering
    enable_blur_detection: bool = True
    blur_threshold: float = 100.0  # Lower = more blurry
    enable_brightness_check: bool = True
    min_brightness: float = 30.0
    max_brightness: float = 225.0


@dataclass
class OCRConfig:
    """OCR processing configuration."""

    # OCR engine selection
    engine: str = "paddleocr"  # "paddleocr" or "easyocr"

    # Language support
    languages: list = None  # Default: ['en']

    # Processing
    use_gpu: bool = False
    batch_size: int = 1
    confidence_threshold: float = 0.5

    def __post_init__(self):
        if self.languages is None:
            self.languages = ['en']


@dataclass
class DeduplicationConfig:
    """Frame deduplication configuration."""

    # Deduplication settings
    enable_deduplication: bool = True
    similarity_threshold: float = 0.90  # 0-1, higher = more strict
    method: str = "phash"  # "phash" (fast), "ssim" (accurate), "histogram"
    hash_size: int = 8  # For phash method
    use_sequential: bool = True  # Use sequential dedup (faster for videos)
    window_size: int = 10  # For sequential dedup


@dataclass
class OutputConfig:
    """Output configuration."""

    output_dir: str = "output"
    save_frames: bool = True
    save_text: bool = True
    save_json: bool = True
    save_pdf: bool = False


@dataclass
class Config:
    """Main configuration container."""

    video: VideoConfig = None
    ocr: OCRConfig = None
    deduplication: DeduplicationConfig = None
    output: OutputConfig = None

    def __post_init__(self):
        if self.video is None:
            self.video = VideoConfig()
        if self.ocr is None:
            self.ocr = OCRConfig()
        if self.deduplication is None:
            self.deduplication = DeduplicationConfig()
        if self.output is None:
            self.output = OutputConfig()
