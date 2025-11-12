"""Setup script for Video OCR System."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="video-ocr-system",
    version="0.1.0",
    description="Extract text from video documents using intelligent frame extraction and OCR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Video OCR Contributors",
    license="Apache 2.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "paddleocr>=2.7.0",
        "easyocr>=1.7.0",
        "Pillow>=10.0.0",
        "scikit-image>=0.21.0",
        "click>=8.1.0",
        "tqdm>=4.66.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "gpu": ["paddlepaddle-gpu>=2.5.0"],
        "dev": ["pytest>=7.0.0", "black>=23.0.0", "flake8>=6.0.0"],
    },
    entry_points={
        "console_scripts": [
            "video-ocr=video_ocr:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    keywords="ocr video text-extraction computer-vision document-processing",
)
