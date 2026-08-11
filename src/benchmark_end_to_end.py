import json

from confidence import calculate_confidence
from evaluate import compare_results
from extract_fields import extract_nutrition_fields
from ocr_reader import read_text
from validate import validate_results


labels = {
    "label_04": {
        "image": "data/raw/label_04/label_04.png",
        "annotation": "data/annotations/label_04.json"
    },
    "label_05": {
        "image": "data/raw/label_05/label_05.png",
        "annotation": "data/annotations/label_05.json"
    },
    "label_06": {
        "image": "data/raw/label_06/label_06.png",
        "annotation": "data/annotations/label_06.json"
    }
}


for label_name, files in labels.items():

    # Start from the actual image
    ocr_text = read_text(files["image"])

    extracted_results = extract_nutrition_fields(ocr_text)

    warnings = validate_results(extracted_results)

    confidence = calculate_confidence(
        extracted_results,
        warnings
    )

    with open(files["annotation"], "r", encoding="utf-8") as file:
        expected_results = json.load(file)

    evaluation = compare_results(
        expected_results,
        extracted_results
    )

    print("\n", label_name)
    print("Accuracy:", round(evaluation["accuracy"] * 100, 2), "%")
    print("Confidence:", round(confidence * 100, 2), "%")