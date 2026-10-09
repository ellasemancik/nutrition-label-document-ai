
from pathlib import Path

from extract_fields import extract_nutrition_fields

output_dir = Path("data/outputs/ocr_tests")

tests = {
    "Original PSM 6": "original_psm6.txt",
    "Original PSM 11": "original_psm11.txt",
    "Grayscale PSM 6": "grayscale_psm6.txt",
    "Enlarged PSM 6": "large_psm6.txt",
    "Enlarged PSM 11": "large_psm11.txt",
    "Threshold PSM 6": "threshold_psm6.txt",
    "Threshold PSM 11": "threshold_psm11.txt",
}

for name, filename in tests.items():
    text = (output_dir / filename).read_text(encoding="utf-8")
    fields = extract_nutrition_fields(text)

    found = {key: value for key, value in fields.items() if value is not None}

    print(f"\n{name}: {len(found)}/11 fields")
    for key, value in found.items():
        print(f"  {key}: {value}")
