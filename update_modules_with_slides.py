#!/usr/bin/env python3
"""
Add slidesDownload field to all modules in modules.json
"""

import json
from pathlib import Path

# Read modules.json
modules_file = Path("docs/modules.json")
with open(modules_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

# OSHA modules (first 11) all use the same slides
osha_modules = [
    "fall-hazards", "electrical-safety", "struck-by-hazards", "caught-in-hazards",
    "ppe", "hazardous-materials", "confined-spaces", "hearing-protection",
    "material-handling", "hand-power-tools", "excavations"
]

# Add slidesDownload to each module
for module in config["modules"]:
    if module["id"] in osha_modules:
        module["slidesDownload"] = "downloads/osha-powerpoint-slides.zip"
    elif module["id"] == "fire-awareness":
        module["slidesDownload"] = "downloads/fire-awareness-slides.zip"
    elif module["id"] == "signalperson":
        module["slidesDownload"] = "downloads/signalperson-slides.zip"

# Write back
with open(modules_file, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)

print("Updated modules.json with slide download links")
print(f"   - {len([m for m in config['modules'] if 'slidesDownload' in m])} modules have slide downloads")
