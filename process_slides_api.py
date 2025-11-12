#!/usr/bin/env python3
"""
Process extracted slides using Claude API.

Reads all slide images and uses Claude's vision to extract text or create summaries.
"""

import base64
import json
from pathlib import Path
from typing import List, Dict, Optional
import anthropic
import click
from tqdm import tqdm


def encode_image(image_path: Path) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def get_image_media_type(image_path: Path) -> str:
    """Get media type from file extension."""
    ext = image_path.suffix.lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return media_types.get(ext, "image/jpeg")


def process_slide(
    client: anthropic.Anthropic,
    image_path: Path,
    prompt: str,
    model: str = "claude-sonnet-4-5-20250929",
    max_tokens: int = 1024,
) -> str:
    """Process a single slide image with Claude."""
    image_data = encode_image(image_path)
    media_type = get_image_media_type(image_path)

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    return message.content[0].text


def process_slides_batch(
    client: anthropic.Anthropic,
    image_paths: List[Path],
    prompt: str,
    model: str = "claude-sonnet-4-5-20250929",
    max_tokens: int = 4096,
) -> str:
    """Process multiple slides in a single request (more efficient for summaries)."""
    content = []

    # Add all images
    for idx, image_path in enumerate(image_paths):
        image_data = encode_image(image_path)
        media_type = get_image_media_type(image_path)

        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_data,
                },
            }
        )
        content.append({"type": "text", "text": f"[Slide {idx + 1}]"})

    # Add the prompt
    content.append({"type": "text", "text": prompt})

    message = client.messages.create(
        model=model, max_tokens=max_tokens, messages=[{"role": "user", "content": content}]
    )

    return message.content[0].text


@click.command()
@click.argument("slides_dir", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output",
    "output_file",
    default="presentation_summary.txt",
    help="Output file for results",
)
@click.option(
    "--mode",
    type=click.Choice(["extract", "summarize"], case_sensitive=False),
    default="extract",
    help="Mode: 'extract' text from each slide, or 'summarize' entire presentation",
)
@click.option(
    "--batch",
    is_flag=True,
    help="Process all slides in one request (faster, better for summaries)",
)
@click.option(
    "--model",
    default="claude-sonnet-4-5-20250929",
    help="Claude model to use",
)
@click.option(
    "--api-key",
    envvar="ANTHROPIC_API_KEY",
    required=True,
    help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
)
def main(
    slides_dir: str,
    output_file: str,
    mode: str,
    batch: bool,
    model: str,
    api_key: str,
):
    """
    Process extracted slides using Claude API.

    \b
    Examples:
        # Extract text from each slide
        process_slides_api.py slides/ -o text.txt --mode extract

        # Summarize entire presentation (batch mode)
        process_slides_api.py slides/ -o summary.txt --mode summarize --batch

        # Extract text in batch mode (faster)
        process_slides_api.py slides/ --batch
    """
    slides_path = Path(slides_dir)

    # Find all slide images
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    slides = sorted(
        [f for f in slides_path.iterdir() if f.suffix.lower() in image_extensions]
    )

    if not slides:
        click.echo(f"❌ No images found in {slides_dir}")
        return

    click.echo(f"📚 Found {len(slides)} slides")
    click.echo(f"🤖 Using model: {model}")
    click.echo(f"📝 Mode: {mode}")
    click.echo(f"⚡ Batch processing: {batch}")

    # Initialize Claude client
    client = anthropic.Anthropic(api_key=api_key)

    # Define prompts
    prompts = {
        "extract": "Please extract all text from this slide. Preserve the structure and formatting as much as possible.",
        "summarize": "Please provide a comprehensive summary of this presentation based on all the slides shown. Include:\n1. Main topic and key themes\n2. Important points from each section\n3. Conclusions or takeaways",
    }

    results = []

    if batch:
        # Process all slides in one request
        click.echo(f"\n🔄 Processing all {len(slides)} slides in batch...")
        prompt = prompts[mode]
        result = process_slides_batch(client, slides, prompt, model=model)
        results.append(result)

    else:
        # Process each slide individually
        click.echo(f"\n🔄 Processing {len(slides)} slides individually...")
        prompt = prompts["extract"]  # Individual mode always extracts

        for idx, slide_path in enumerate(tqdm(slides, desc="Processing", unit="slide")):
            try:
                result = process_slide(client, slide_path, prompt, model=model)
                results.append(f"=== Slide {idx + 1}: {slide_path.name} ===\n\n{result}\n")
            except Exception as e:
                error_msg = f"❌ Error processing {slide_path.name}: {e}"
                click.echo(error_msg)
                results.append(f"=== Slide {idx + 1}: {slide_path.name} ===\n\n{error_msg}\n")

    # Save results
    output_path = Path(output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        if batch:
            f.write(results[0])
        else:
            f.write("\n".join(results))

    click.echo(f"\n✅ Results saved to: {output_path.absolute()}")
    click.echo(f"📄 Total slides processed: {len(slides)}")

    # Show preview
    preview = results[0][:500] if batch else results[0][:500]
    click.echo(f"\n📖 Preview:\n{preview}...")


if __name__ == "__main__":
    main()
