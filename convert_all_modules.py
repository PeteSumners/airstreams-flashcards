#!/usr/bin/env python3
"""
Convert all module flashcards to Quizlet and web formats.
"""

import subprocess
import sys
from pathlib import Path

MODULES = [
    "fall-hazards",
    "electrical-safety",
    "struck-by-hazards",
    "caught-in-hazards",
    "ppe",
    "hazardous-materials",
    "confined-spaces",
    "hearing-protection",
    "material-handling",
    "hand-power-tools",
    "excavations"
]

def main():
    print("=" * 60)
    print("Converting All Modules to Quizlet + Web Formats")
    print("=" * 60)
    print()

    errors = []

    for module in MODULES:
        module_file = Path(f"modules/{module}/flashcards.txt")

        if not module_file.exists():
            print(f"SKIP: {module} (file not found)")
            errors.append(f"{module}: file not found")
            continue

        print(f"Processing: {module}")
        print("-" * 40)

        # Create Quizlet format
        try:
            result = subprocess.run(
                [sys.executable, "scripts/create_quizlet_format.py", str(module_file)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  Quizlet: OK")
            else:
                print(f"  Quizlet: FAILED")
                errors.append(f"{module}: Quizlet conversion failed")
        except Exception as e:
            print(f"  Quizlet: ERROR - {e}")
            errors.append(f"{module}: Quizlet error - {e}")

        # Create web format
        try:
            result = subprocess.run(
                [sys.executable, "scripts/convert_to_web_format.py", str(module_file)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  Web: OK")
            else:
                print(f"  Web: FAILED")
                errors.append(f"{module}: Web conversion failed")
        except Exception as e:
            print(f"  Web: ERROR - {e}")
            errors.append(f"{module}: Web error - {e}")

        print()

    print("=" * 60)
    if errors:
        print(f"Completed with {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("All modules converted successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
