import json

from evaluate import compare_results
from extract_fields import extract_nutrition_fields


annotation_file = "data/annotations/label_03.json"

ocr_files = {
    6: "data/outputs/label_03/label_03_psm_6_ocr.txt",
    11: "data/outputs/label_03/label_03_psm_11_ocr.txt"
}


with open(annotation_file, "r", encoding="utf-8") as file:
    expected_results = json.load(file)


for psm, ocr_file in ocr_files.items():

    with open(ocr_file, "r", encoding="utf-8") as file:
        ocr_text = file.read()

    extracted_results = extract_nutrition_fields(ocr_text)

    evaluation = compare_results(
        expected_results,
        extracted_results
    )

    accuracy = evaluation["accuracy"] * 100

    print("\nPSM:", psm)
    print("Correct:", evaluation["correct_fields"])
    print("Total:", evaluation["total_fields"])
    print("Accuracy:", round(accuracy, 2), "%")

    print("Differences:")
    print(evaluation["differences"])