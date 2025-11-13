#!/usr/bin/env python3
"""
Convert OSHA Flashcards to Anki CSV format
"""

import csv
import re

def parse_flashcards(input_file, output_file):
    """Parse Q&A flashcards and convert to Anki CSV format."""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Q&A pairs
    # Pattern: Q: question text\nA: answer text
    pattern = r'Q:\s*(.*?)\nA:\s*(.*?)(?=\n\nQ:|$)'
    matches = re.findall(pattern, content, re.DOTALL)

    print(f"Found {len(matches)} flashcard pairs")

    # Write to CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')  # Anki uses tab-separated

        for question, answer in matches:
            # Clean up whitespace
            question = question.strip()
            answer = answer.strip()

            # Skip empty cards
            if question and answer:
                writer.writerow([question, answer])

    print(f"Successfully created {output_file} with {len(matches)} flashcards")
    print(f"\nReady to import into Anki!")

if __name__ == "__main__":
    parse_flashcards("OSHA_Flashcards.txt", "OSHA_Flashcards_Anki.txt")
