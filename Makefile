# Makefile for Video OCR System

.PHONY: help install install-dev test clean format lint run-example generate-test-video

help:
	@echo "Video OCR System - Available Commands"
	@echo "======================================"
	@echo "install           - Install dependencies"
	@echo "install-dev       - Install with development dependencies"
	@echo "test              - Run unit tests"
	@echo "clean             - Remove generated files and caches"
	@echo "format            - Format code with black"
	@echo "lint              - Run linting with flake8"
	@echo "run-example       - Generate and process test video"
	@echo "generate-test-video - Generate a test video"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest black flake8

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf build/ dist/ output/ test_video.mp4

format:
	black src/ tests/ *.py utils/

lint:
	flake8 src/ tests/ --max-line-length=88 --ignore=E203,W503

generate-test-video:
	python utils/generate_test_video.py

run-example: generate-test-video
	python video_ocr.py test_video.mp4 -v
