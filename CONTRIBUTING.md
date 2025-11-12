# Contributing to Video OCR System

Thank you for your interest in contributing to the Video OCR System! This document provides guidelines and instructions for contributing.

## Project Status

Currently: **Phase 1 Complete** - Core infrastructure with video frame extraction and OCR

See [ROADMAP.md](ROADMAP.md) for planned features and upcoming phases.

## Ways to Contribute

### 1. Code Contributions

Areas where contributions are especially welcome:

#### Phase 2: Page/Slide Detection (High Priority)
- Frame-to-frame comparison algorithms (SSIM, histogram comparison)
- Slide transition detection
- Perceptual hashing for deduplication
- Smart frame grouping

#### Phase 3: Document Processing
- Perspective correction and deskewing
- Advanced image enhancement
- Layout analysis and structure preservation
- Multi-column text handling

#### Phase 4: Output Formats
- Searchable PDF generation
- Markdown with structure preservation
- Better metadata management

#### Phase 5: User Interface
- Enhanced CLI features
- Optional GUI (Qt, Tkinter, or web-based)
- Configuration file support improvements

#### Phase 6: Optimizations
- Multi-threading for frame processing
- Memory-efficient streaming
- GPU acceleration improvements
- Caching mechanisms

### 2. Testing and Bug Reports

- Test the system with different video types
- Report bugs with detailed reproduction steps
- Suggest improvements based on real-world usage

### 3. Documentation

- Improve README and guides
- Add tutorials and examples
- Write blog posts or articles about usage
- Translate documentation to other languages

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ocr
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

   # For development
   pip install pytest black flake8
   ```

4. **Run tests:**
   ```bash
   python -m pytest tests/ -v
   ```

## Code Style

We follow Python best practices and PEP 8 with some modifications:

- Line length: 88 characters (Black default)
- Use Black for code formatting
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Formatting

```bash
# Format code
black src/ tests/ *.py

# Check formatting
black --check src/ tests/ *.py
```

### Linting

```bash
flake8 src/ tests/ --max-line-length=88 --ignore=E203,W503
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_video_processor.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

- Write unit tests for new features
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

Example:
```python
def test_feature_name_expected_behavior(self):
    """Test that feature behaves correctly when condition X."""
    # Arrange
    config = VideoConfig()
    processor = VideoProcessor(config)

    # Act
    result = processor.some_method()

    # Assert
    self.assertEqual(result, expected_value)
```

## Submitting Changes

### Pull Request Process

1. **Fork the repository**

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes:**
   - Write code
   - Add/update tests
   - Update documentation

4. **Test your changes:**
   ```bash
   python -m pytest tests/ -v
   black src/ tests/ *.py
   flake8 src/ tests/
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request:**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in PR template

### Commit Messages

Use clear, descriptive commit messages:

```
Add feature: brief description

Longer explanation of what changed and why.
Include relevant issue numbers.

Fixes #123
```

### Pull Request Guidelines

- One feature/fix per PR
- Include tests for new features
- Update documentation as needed
- Ensure all tests pass
- Follow code style guidelines
- Add entry to CHANGELOG (if exists)

## Project Structure

Understanding the codebase:

```
ocr/
├── src/                      # Main source code
│   ├── config.py            # Configuration classes
│   ├── video_processor.py   # Video frame extraction
│   ├── ocr_engine.py        # OCR implementations
│   └── pipeline.py          # Main processing pipeline
├── tests/                   # Unit tests
├── utils/                   # Utility scripts
├── video_ocr.py            # CLI entry point
└── example_usage.py        # Usage examples
```

### Key Components

1. **VideoProcessor** (`src/video_processor.py`)
   - Frame extraction
   - Motion detection
   - Quality filtering

2. **OCREngine** (`src/ocr_engine.py`)
   - OCR abstraction layer
   - PaddleOCR and EasyOCR implementations

3. **Pipeline** (`src/pipeline.py`)
   - Coordinates video processing and OCR
   - Manages results and output

## Coding Guidelines

### General Principles

1. **Keep it simple** - Prefer clear code over clever code
2. **DRY** - Don't Repeat Yourself
3. **SOLID** - Follow SOLID principles
4. **Test** - Write tests for your code
5. **Document** - Write clear docstrings and comments

### Specific Guidelines

#### Error Handling

```python
def process_video(video_path: str):
    """Process video file."""
    if not Path(video_path).exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    try:
        # Processing logic
        pass
    except cv2.error as e:
        logger.error(f"OpenCV error: {e}")
        raise
```

#### Logging

```python
import logging

logger = logging.getLogger(__name__)

# Use appropriate log levels
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
```

#### Configuration

- Use dataclasses for configuration
- Provide sensible defaults
- Document all configuration options

## Performance Considerations

- Profile code before optimizing
- Use generators for large datasets
- Consider memory usage with large videos
- Document performance characteristics

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.

## Getting Help

- Check existing issues and PRs
- Read the documentation
- Ask questions in issues (tag with "question")

## Recognition

Contributors will be recognized in:
- README contributors section
- Release notes
- Project documentation

Thank you for contributing to Video OCR System! 🚀
