#!/usr/bin/env python3
"""
Split OSHA flashcards into separate module files by topic.
Creates individual module directories with flashcard files.
"""

import os
import re
from pathlib import Path

# Module mapping: section headers to module info
MODULES = {
    "fall-hazards": {
        "title": "Fall Hazards & Protection",
        "description": "OSHA 10HR - Fall hazards, PFAS, guardrails, safety nets, rescue planning, ladders",
        "sections": [
            "FALL HAZARDS - STATISTICS & REGULATIONS",
            "FALL PROTECTION METHODS",
            "GUARDRAILS (1926.502)",
            "SAFETY NETS (1926.105)",
            "PERSONAL FALL ARREST SYSTEMS (PFAS)",
            "ANCHORAGE",
            "BODY HARNESS",
            "CONNECTORS & LANYARDS",
            "DECELERATION DEVICES",
            "ARRESTING FORCES",
            "EQUIPMENT INSPECTION",
            "RESCUE PLAN",
            "MAJOR FALL HAZARDS",
            "SPECIFIC SITUATIONS",
            "LADDERS",
            "FALLING OBJECTS",
            "GOOD WORK PRACTICES",
            "TRAINING REQUIREMENTS"
        ]
    },
    "electrical-safety": {
        "title": "Electrical Safety",
        "description": "OSHA 10HR - Electrical hazards, power line clearances, GFCI, grounding, LOTO procedures",
        "sections": [
            "ELECTRICAL HAZARDS"
        ]
    },
    "struck-by-hazards": {
        "title": "Struck-By Hazards",
        "description": "OSHA 10HR - Protection from flying, falling, swinging, and rolling objects",
        "sections": [
            "STRUCK-BY HAZARDS"
        ]
    },
    "caught-in-hazards": {
        "title": "Caught-In/Between Hazards",
        "description": "OSHA 10HR - Machinery hazards, equipment safety, excavation cave-ins",
        "sections": [
            "CAUGHT-IN OR BETWEEN HAZARDS",
            "ACCIDENT PREVENTION"
        ]
    },
    "ppe": {
        "title": "Personal Protective Equipment (PPE)",
        "description": "OSHA 10HR - Head, eye, hearing, foot, hand, and body protection requirements",
        "sections": [
            "PERSONAL PROTECTIVE EQUIPMENT (PPE)",
            "HEAD PROTECTION",
            "EYE PROTECTION",
            "HEARING PROTECTION",
            "FOOT PROTECTION",
            "HAND PROTECTION",
            "BODY PROTECTION",
            "PPE LIMITATIONS AND MAINTENANCE"
        ]
    },
    "hazardous-materials": {
        "title": "Hazardous Materials & Chemical Safety",
        "description": "OSHA 10HR - HazCom, SDS, NFPA labels, chemical routes of entry, respiratory protection",
        "sections": [
            "HAZARDOUS MATERIALS - RIGHT TO KNOW",
            "SAFETY DATA SHEETS (SDS)",
            "HAZARDOUS MATERIALS FIRST AID",
            "CHEMICAL HAZARDS - ROUTES OF ENTRY",
            "HAZARD COMMUNICATION STANDARD",
            "LABELS",
            "NFPA LABELING SYSTEM",
            "SPILLS AND LEAKS",
            "PPE FOR HAZARDOUS MATERIALS",
            "RESPIRATORY PROTECTION",
            "RESPIRATOR FIT-TESTING",
            "DUSTS AND FIBERS IN CONSTRUCTION",
            "CRYSTALLINE SILICA",
            "ASBESTOS",
            "FIBERGLASS INSULATION PPE"
        ]
    },
    "confined-spaces": {
        "title": "Confined Spaces",
        "description": "OSHA 10HR - Permit-required spaces, atmospheric testing, entry procedures",
        "sections": [
            "CONFINED SPACES",
            "PERMIT-REQUIRED CONFINED SPACES DEFINITION",
            "CONFINED SPACE HAZARDS",
            "NON-PERMIT-REQUIRED CONFINED SPACES",
            "ATMOSPHERIC TESTING",
            "CONFINED SPACE WRITTEN PROGRAM"
        ]
    },
    "hearing-protection": {
        "title": "Hearing Conservation",
        "description": "OSHA 10HR - Noise exposure limits, monitoring, hearing protection types, attenuation",
        "sections": [
            "HEARING PROTECTION STANDARDS",
            "PERMISSIBLE NOISE EXPOSURE LIMITS",
            "NOISE MONITORING",
            "HEARING PROTECTION TYPES",
            "HEARING PROTECTOR ATTENUATION",
            "HEARING LOSS"
        ]
    },
    "material-handling": {
        "title": "Material Handling & Storage",
        "description": "OSHA 10HR - Safe lifting, forklifts, cranes, rigging, slings, storage requirements",
        "sections": [
            "MATERIAL HANDLING",
            "SAFE LIFTING TECHNIQUES",
            "MATERIALS HANDLING EQUIPMENT",
            "FORKLIFTS - SAFE OPERATION",
            "EARTHMOVING EQUIPMENT REQUIREMENTS",
            "CRANES - SAFETY REQUIREMENTS",
            "RIGGING EQUIPMENT - SLINGS",
            "STORING MATERIALS - GENERAL REQUIREMENTS",
            "DISPOSAL OF WASTE MATERIALS"
        ]
    },
    "hand-power-tools": {
        "title": "Hand & Power Tools",
        "description": "OSHA 10HR - Tool safety, guards, pneumatic, powder-actuated, abrasive wheels",
        "sections": [
            "HAND AND POWER TOOLS - HAZARDS",
            "POWER TOOLS - TYPES BY POWER SOURCE",
            "ABRASIVE WHEELS AND TOOLS - GUARDS",
            "GUARDING - GENERAL REQUIREMENTS",
            "PNEUMATIC TOOLS",
            "LIQUID FUEL TOOLS",
            "POWDER-ACTUATED TOOLS",
            "JACKS"
        ]
    },
    "excavations": {
        "title": "Excavations & Trenching",
        "description": "OSHA 10HR - Cave-ins, protective systems, shoring, sloping, competent person",
        "sections": [
            "EXCAVATIONS - DEFINITIONS",
            "EXCAVATION HAZARDS",
            "PROTECTIVE SYSTEMS DESIGN",
            "SHORING",
            "PROTECTION FROM VEHICLES",
            "SPOILS",
            "HAZARDOUS ATMOSPHERE",
            "MEANS OF EGRESS",
            "PROTECTION FROM FALLS AND MOBILE EQUIPMENT",
            "COMPETENT PERSON",
            "INSPECTIONS OF EXCAVATIONS",
            "SITE EVALUATION PLANNING"
        ]
    }
}


def parse_flashcards_file(input_file):
    """Parse the master flashcards file into sections."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by section headers (lines with all caps and separators)
    sections = {}
    current_section = None
    current_content = []

    lines = content.split('\n')
    separator_pattern = re.compile(r'^={10,}$')

    for i, line in enumerate(lines):
        # Check if this is a separator line
        if separator_pattern.match(line.strip()):
            # Next line might be a section header
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Check if it's an all-caps section header
                if next_line and next_line.isupper() and len(next_line) > 5:
                    # Save previous section
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content)

                    # Start new section
                    current_section = next_line
                    current_content = [line, next_line]  # Include separator and header
                    continue

        # Add line to current section
        if current_section:
            current_content.append(line)

    # Save last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content)

    return sections


def create_module_files(sections, output_base_dir):
    """Create module directories and files."""
    output_base = Path(output_base_dir)

    # Get header from original file
    header = """# OSHA 10HR Construction Training Flashcards
# Created from Airstreams Renewables Training - Tehachapi, CA
# Format: Q&A pairs compatible with web app and Quizlet
# Contact: petesumners@outlook.com to submit corrections or new cards

"""

    created_modules = []

    for module_id, module_info in MODULES.items():
        module_dir = output_base / module_id
        module_dir.mkdir(parents=True, exist_ok=True)

        # Collect content for this module
        module_content = [header]
        card_count = 0

        for section_name in module_info['sections']:
            if section_name in sections:
                module_content.append(sections[section_name])
                module_content.append('\n')
                # Count Q: lines
                card_count += sections[section_name].count('\nQ:')

        # Write flashcards.txt
        output_file = module_dir / 'flashcards.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(module_content))

        created_modules.append({
            'id': module_id,
            'title': module_info['title'],
            'description': module_info['description'],
            'cardCount': card_count,
            'file': str(output_file)
        })

        print(f"Created {module_id}: {card_count} cards -> {output_file}")

    return created_modules


def main():
    # Paths
    input_file = Path('modules/fall-hazards/OSHA_Flashcards.txt')
    output_base = Path('modules')

    print("=" * 60)
    print("OSHA Flashcards Module Splitter")
    print("=" * 60)
    print()

    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return

    print(f"Reading: {input_file}")
    sections = parse_flashcards_file(input_file)
    print(f"Found {len(sections)} sections")
    print()

    print("Creating module files...")
    created_modules = create_module_files(sections, output_base)
    print()

    print("=" * 60)
    print(f"Successfully created {len(created_modules)} modules!")
    print("=" * 60)
    print()

    print("Module Summary:")
    for module in created_modules:
        print(f"  - {module['title']}: {module['cardCount']} cards")
    print()

    print("Next steps:")
    print("1. Run: python scripts/create_quizlet_format.py for each module")
    print("2. Run: python scripts/convert_to_web_format.py for each module")
    print("3. Update docs/modules.json with all modules")
    print()


if __name__ == '__main__':
    main()
