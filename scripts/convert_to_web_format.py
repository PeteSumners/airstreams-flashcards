#!/usr/bin/env python3
"""
Convert flashcards from Q&A text format to web JavaScript format.

Usage:
    python scripts/convert_to_web_format.py modules/module-name/flashcards.txt

Output:
    docs/flashcards-module-name.js
"""

import re
import sys
import json
from pathlib import Path

def parse_flashcards(content):
    """Parse Q&A flashcards from text content."""
    # Pattern: Q: question text\nA: answer text
    pattern = r'Q:\s*(.*?)\nA:\s*(.*?)(?=\n\nQ:|$)'
    matches = re.findall(pattern, content, re.DOTALL)

    flashcards = []
    for question, answer in matches:
        question = question.strip()
        answer = answer.strip()

        if question and answer:
            flashcards.append({
                'question': question,
                'answer': answer
            })

    return flashcards

def escape_js_string(s):
    """Escape string for JavaScript."""
    # Replace backslash first
    s = s.replace('\\', '\\\\')
    # Replace quotes
    s = s.replace('"', '\\"')
    s = s.replace("'", "\\'")
    # Replace newlines
    s = s.replace('\n', '\\n')
    return s

def convert_to_javascript(flashcards, module_name, module_title):
    """Convert flashcards to JavaScript format."""

    js_content = f'''// Flashcards for: {module_title}
// Module ID: {module_name}
// Auto-generated - Do not edit directly
// Generated from: modules/{module_name}/flashcards.txt

flashcards = [
'''

    for i, card in enumerate(flashcards):
        question = escape_js_string(card['question'])
        answer = escape_js_string(card['answer'])

        js_content += f'    {{\n'
        js_content += f'        question: "{question}",\n'
        js_content += f'        answer: "{answer}"\n'
        js_content += f'    }}'

        if i < len(flashcards) - 1:
            js_content += ','

        js_content += '\n'

    js_content += '];\n'
    js_content += f'\nconsole.log("Loaded {len(flashcards)} flashcards for {module_title}");\n'

    return js_content

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/convert_to_web_format.py modules/module-name/flashcards.txt")
        print("\nExample:")
        print("  python scripts/convert_to_web_format.py modules/fall-hazards/flashcards.txt")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    # Extract module name from path
    # modules/module-name/flashcards.txt -> module-name
    module_name = input_file.parent.name

    # Generate output filename
    output_file = Path('docs') / f'flashcards-{module_name}.js'

    # Read input file
    print(f"Reading flashcards from: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse flashcards
    flashcards = parse_flashcards(content)
    print(f"Found {len(flashcards)} flashcard pairs")

    if len(flashcards) == 0:
        print("Error: No flashcards found. Check file format.")
        print("Expected format:")
        print("Q: Question text here")
        print("A: Answer text here")
        print()
        print("Q: Another question")
        print("A: Another answer")
        sys.exit(1)

    # Get module title (capitalize and format nicely)
    module_title = module_name.replace('-', ' ').title()

    # Convert to JavaScript
    js_content = convert_to_javascript(flashcards, module_name, module_title)

    # Write output file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Created: {output_file}")
    print(f"{len(flashcards)} flashcards ready for web app")
    print()
    print("Next steps:")
    print(f"1. Add module to docs/modules.json:")
    print(f'   - id: "{module_name}"')
    print(f'   - flashcardsFile: "flashcards-{module_name}.js"')
    print(f'   - cardCount: {len(flashcards)}')
    print("2. Test locally by opening docs/index.html")
    print("3. Push to GitHub to publish")

if __name__ == "__main__":
    main()
