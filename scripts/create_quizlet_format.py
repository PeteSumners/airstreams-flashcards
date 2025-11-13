#!/usr/bin/env python3
"""
Convert flashcards to Quizlet TSV format.

Usage:
    python scripts/create_quizlet_format.py modules/module-name/flashcards.txt

Output:
    modules/module-name/flashcards_quizlet.txt
"""

import re
import sys
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_quizlet_format.py modules/module-name/flashcards.txt")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    # Generate output filename
    output_file = input_file.parent / "flashcards_quizlet.txt"

    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse flashcards
    flashcards = parse_flashcards(content)

    if len(flashcards) == 0:
        print("Error: No flashcards found. Check file format.")
        sys.exit(1)

    # Write TSV format (tab-separated)
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        for card in flashcards:
            # Tab-separated: Question[TAB]Answer
            f.write(f"{card['question']}\t{card['answer']}\n")

    print(f"✅ Created: {output_file}")
    print(f"📊 {len(flashcards)} flashcards ready for Quizlet import")

if __name__ == "__main__":
    main()
