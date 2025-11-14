"""Frame deduplication using perceptual hashing and similarity comparison."""

import logging
from typing import List, Tuple
import numpy as np
import cv2

from .video_processor import FrameInfo

logger = logging.getLogger(__name__)


class FrameDeduplicator:
    """Deduplicate similar frames and keep only unique ones."""

    def __init__(
        self,
        similarity_threshold: float = 0.95,
        method: str = "phash",
        hash_size: int = 8,
    ):
        """
        Initialize deduplicator.

        Args:
            similarity_threshold: Threshold for considering frames similar (0-1)
                                For phash: lower threshold (0.85-0.95)
                                For ssim: higher threshold (0.95-0.99)
            method: Comparison method - "phash" (fast) or "ssim" (accurate)
            hash_size: Size for perceptual hash (only used if method="phash")
        """
        self.similarity_threshold = similarity_threshold
        self.method = method
        self.hash_size = hash_size

    def compute_phash(self, frame: np.ndarray) -> np.ndarray:
        """
        Compute perceptual hash of a frame.

        Args:
            frame: Image as numpy array

        Returns:
            Perceptual hash as binary array
        """
        # Convert to grayscale
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        # Resize to hash_size x hash_size
        resized = cv2.resize(gray, (self.hash_size, self.hash_size))

        # Compute DCT (Discrete Cosine Transform)
        dct = cv2.dct(np.float32(resized))

        # Keep only top-left 8x8 (low frequencies)
        dct_low = dct[:self.hash_size, :self.hash_size]

        # Compute median
        median = np.median(dct_low)

        # Create hash: 1 if > median, 0 otherwise
        hash_array = dct_low > median

        return hash_array.flatten()

    def compare_phash(self, hash1: np.ndarray, hash2: np.ndarray) -> float:
        """
        Compare two perceptual hashes.

        Args:
            hash1, hash2: Perceptual hashes to compare

        Returns:
            Similarity score (0-1, higher = more similar)
        """
        # Hamming distance (number of different bits)
        hamming_distance = np.sum(hash1 != hash2)

        # Convert to similarity (0-1)
        max_distance = len(hash1)
        similarity = 1.0 - (hamming_distance / max_distance)

        return similarity

    def compare_ssim(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """
        Compare two frames using Structural Similarity Index (SSIM).

        Args:
            frame1, frame2: Images to compare

        Returns:
            SSIM score (0-1, higher = more similar)
        """
        try:
            from skimage.metrics import structural_similarity as ssim
        except ImportError:
            raise ImportError(
                "scikit-image is required for SSIM method. "
                "Install with: pip install scikit-image\n"
                "Or use --dedup-method phash instead (default, faster)."
            )

        # Convert to grayscale
        if len(frame1.shape) == 3:
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        else:
            gray1 = frame1

        if len(frame2.shape) == 3:
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        else:
            gray2 = frame2

        # Resize to same size if needed
        if gray1.shape != gray2.shape:
            h, w = min(gray1.shape[0], gray2.shape[0]), min(
                gray1.shape[1], gray2.shape[1]
            )
            gray1 = cv2.resize(gray1, (w, h))
            gray2 = cv2.resize(gray2, (w, h))

        # Compute SSIM
        score = ssim(gray1, gray2)

        return score

    def compute_histogram_similarity(
        self, frame1: np.ndarray, frame2: np.ndarray
    ) -> float:
        """
        Compare frames using histogram comparison.

        Args:
            frame1, frame2: Images to compare

        Returns:
            Similarity score (0-1, higher = more similar)
        """
        # Convert to HSV for better color comparison
        hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

        # Compute histograms
        hist1 = cv2.calcHist([hsv1], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
        hist2 = cv2.calcHist([hsv2], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])

        # Normalize
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()

        # Compare using correlation
        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

        return similarity

    def are_frames_similar(
        self, frame_info1: FrameInfo, frame_info2: FrameInfo
    ) -> Tuple[bool, float]:
        """
        Check if two frames are similar.

        Args:
            frame_info1, frame_info2: FrameInfo objects to compare

        Returns:
            Tuple of (is_similar, similarity_score)
        """
        if self.method == "phash":
            # Perceptual hash comparison (fast)
            hash1 = self.compute_phash(frame_info1.frame)
            hash2 = self.compute_phash(frame_info2.frame)
            similarity = self.compare_phash(hash1, hash2)
        elif self.method == "ssim":
            # SSIM comparison (accurate but slower)
            similarity = self.compare_ssim(frame_info1.frame, frame_info2.frame)
        elif self.method == "histogram":
            # Histogram comparison (good for color changes)
            similarity = self.compute_histogram_similarity(
                frame_info1.frame, frame_info2.frame
            )
        else:
            raise ValueError(f"Unknown comparison method: {self.method}")

        is_similar = similarity >= self.similarity_threshold

        return is_similar, similarity

    def deduplicate(self, frames: List[FrameInfo]) -> List[FrameInfo]:
        """
        Deduplicate frames, keeping only unique ones.

        For each group of similar frames, keeps the one with highest quality score.

        Args:
            frames: List of FrameInfo objects to deduplicate

        Returns:
            List of unique FrameInfo objects
        """
        if not frames:
            return []

        if len(frames) == 1:
            return frames

        logger.info(
            f"Deduplicating {len(frames)} frames "
            f"(method={self.method}, threshold={self.similarity_threshold})"
        )

        unique_frames = []
        processed = set()

        for i, frame_i in enumerate(frames):
            if i in processed:
                continue

            # Start a new group with this frame
            similar_group = [frame_i]
            processed.add(i)

            # Find all frames similar to this one
            for j in range(i + 1, len(frames)):
                if j in processed:
                    continue

                frame_j = frames[j]
                is_similar, similarity = self.are_frames_similar(frame_i, frame_j)

                if is_similar:
                    similar_group.append(frame_j)
                    processed.add(j)
                    logger.debug(
                        f"Frames {i} and {j} are similar (score: {similarity:.3f})"
                    )

            # Select best frame from group (highest quality)
            best_frame = max(similar_group, key=lambda f: f.quality_score)
            unique_frames.append(best_frame)

            logger.debug(
                f"Group {len(unique_frames)}: {len(similar_group)} similar frames, "
                f"kept frame at {best_frame.timestamp:.2f}s "
                f"(quality: {best_frame.quality_score:.2f})"
            )

        logger.info(
            f"Deduplication complete: {len(frames)} -> {len(unique_frames)} frames "
            f"({len(frames) - len(unique_frames)} duplicates removed)"
        )

        return unique_frames

    def deduplicate_sequential(
        self, frames: List[FrameInfo], window_size: int = 5
    ) -> List[FrameInfo]:
        """
        Deduplicate frames using a sequential approach (faster).

        Only compares each frame with the next few frames in sequence,
        rather than all frames. Good for videos where duplicates are sequential.

        Args:
            frames: List of FrameInfo objects to deduplicate
            window_size: How many subsequent frames to compare with

        Returns:
            List of unique FrameInfo objects
        """
        if not frames:
            return []

        if len(frames) == 1:
            return frames

        logger.info(
            f"Sequential deduplication: {len(frames)} frames "
            f"(window={window_size}, method={self.method})"
        )

        unique_frames = [frames[0]]  # Always keep first frame

        for i in range(1, len(frames)):
            current_frame = frames[i]
            is_duplicate = False

            # Compare with recent unique frames (within window)
            for j in range(
                max(0, len(unique_frames) - window_size), len(unique_frames)
            ):
                reference_frame = unique_frames[j]

                is_similar, similarity = self.are_frames_similar(
                    current_frame, reference_frame
                )

                if is_similar:
                    is_duplicate = True
                    logger.debug(
                        f"Frame {i} is duplicate of frame {reference_frame.frame_number} "
                        f"(similarity: {similarity:.3f})"
                    )

                    # If current frame has better quality, replace the reference
                    if current_frame.quality_score > reference_frame.quality_score:
                        logger.debug(
                            f"Replacing with better quality frame "
                            f"({current_frame.quality_score:.2f} > "
                            f"{reference_frame.quality_score:.2f})"
                        )
                        unique_frames[j] = current_frame

                    break

            if not is_duplicate:
                unique_frames.append(current_frame)

        logger.info(
            f"Sequential deduplication complete: {len(frames)} -> {len(unique_frames)} "
            f"frames ({len(frames) - len(unique_frames)} duplicates removed)"
        )

        return unique_frames
