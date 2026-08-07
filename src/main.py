import json

from evaluate import compare_results
from extract_fields import extract_nutrition_fields
from validate import validate_results


ocr_file = "data/outputs/label_02/label_02_threshold_140_ocr.txt"
annotation_file = "data/annotations/label_02.json"

json_output = "data/outputs/label_02/label_02_extracted.json"
evaluation_output = "data/outputs/label_02/label_02_evaluation.json"


with open(ocr_file, "r", encoding="utf-8") as file:
    ocr_text = file.read()


extracted_results = extract_nutrition_fields(ocr_text)

validation_warnings = validate_results(extracted_results)


with open(json_output, "w", encoding="utf-8") as file:
    json.dump(extracted_results, file, indent=2)


with open(annotation_file, "r", encoding="utf-8") as file:
    expected_results = json.load(file)


evaluation = compare_results(expected_results, extracted_results)


with open(evaluation_output, "w", encoding="utf-8") as file:
    json.dump(evaluation, file, indent=2)


print("Extracted fields:")
print(extracted_results)

print("\nEvaluation:")
print("Correct fields:", evaluation["correct_fields"])
print("Total fields:", evaluation["total_fields"])
print("Accuracy:", round(evaluation["accuracy"] * 100, 2), "%")

print("\nDifferences:")
print(evaluation["differences"])

print("\nExtracted JSON saved to:", json_output)
print("Evaluation saved to:", evaluation_output)

print("\nValidation warnings:")
print(validation_warnings)