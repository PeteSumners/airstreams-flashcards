#!/usr/bin/env python3
"""
Reorganize modules.json to group flashcard sets by source video/PowerPoint
"""

import json
from pathlib import Path

# Read current modules.json
modules_file = Path("docs/modules.json")
with open(modules_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Group modules by source
osha_module_ids = [
    "fall-hazards", "electrical-safety", "struck-by-hazards", "caught-in-hazards",
    "ppe", "hazardous-materials", "confined-spaces", "hearing-protection",
    "material-handling", "hand-power-tools", "excavations"
]

# Create new structure with sources
new_config = {
    "sources": [
        {
            "id": "osha-10hr",
            "title": "OSHA 10HR Construction Training",
            "description": "Complete OSHA 10HR certification course covering Focus Four hazards and essential construction safety",
            "slidesDownload": "downloads/osha-powerpoint-slides.zip",
            "modules": []
        },
        {
            "id": "fire-awareness",
            "title": "Fire Awareness for Wind Turbines",
            "description": "Fire safety training specific to wind turbine operations and maintenance",
            "slidesDownload": "downloads/fire-awareness-slides.zip",
            "modules": []
        },
        {
            "id": "signalperson",
            "title": "Crane Signalperson Training",
            "description": "NCCCO-compliant signalperson training for crane operations",
            "slidesDownload": "downloads/signalperson-slides.zip",
            "modules": []
        }
    ],
    "settings": config["settings"]
}

# Distribute modules to their sources
for module in config["modules"]:
    # Remove slidesDownload from individual modules (now at source level)
    if "slidesDownload" in module:
        del module["slidesDownload"]

    if module["id"] in osha_module_ids:
        new_config["sources"][0]["modules"].append(module)
    elif module["id"] == "fire-awareness":
        new_config["sources"][1]["modules"].append(module)
    elif module["id"] == "signalperson":
        new_config["sources"][2]["modules"].append(module)

# Calculate totals for each source
for source in new_config["sources"]:
    total_cards = sum(m["cardCount"] for m in source["modules"])
    source["totalCards"] = total_cards
    source["moduleCount"] = len(source["modules"])

# Write new structure
with open(modules_file, 'w', encoding='utf-8') as f:
    json.dump(new_config, f, indent=2)

print("Reorganized modules.json by source video")
print()
for source in new_config["sources"]:
    print(f"{source['title']}")
    print(f"  - {source['moduleCount']} modules")
    print(f"  - {source['totalCards']} flashcards")
    print(f"  - Slides: {source['slidesDownload']}")
    print()
