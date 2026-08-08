import json

from confidence import calculate_confidence
from evaluate import compare_results
from extract_fields import extract_nutrition_fields
from validate import validate_results


# Files for label 04
ocr_file = "data/outputs/label_04/label_04_ocr.txt"
annotation_file = "data/annotations/label_04.json"

json_output = "data/outputs/label_04/label_04_extracted.json"
evaluation_output = "data/outputs/label_04/label_04_evaluation.json"


# Read OCR text
with open(ocr_file, "r", encoding="utf-8") as file:
    ocr_text = file.read()


# Extract nutrition fields from the OCR text
extracted_results = extract_nutrition_fields(ocr_text)


# Validate the extracted values
validation_warnings = validate_results(extracted_results)

if len(validation_warnings) == 0:
    validation_status = "passed"
else:
    validation_status = "warning"


# Calculate confidence
confidence_score = calculate_confidence(
    extracted_results,
    validation_warnings
)


# Save the extracted result
final_results = {
    "fields": extracted_results,
    "validation_status": validation_status,
    "validation_warnings": validation_warnings,
    "confidence_score": confidence_score
}

with open(json_output, "w", encoding="utf-8") as file:
    json.dump(final_results, file, indent=2)


# Load the correct answers
with open(annotation_file, "r", encoding="utf-8") as file:
    expected_results = json.load(file)


# Compare the extraction to the correct values
evaluation = compare_results(
    expected_results,
    extracted_results
)

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

print("\nValidation status:")
print(validation_status)

print("\nValidation warnings:")
print(validation_warnings)

print("\nConfidence score:")
print(round(confidence_score * 100, 2), "%")

print("\nExtracted JSON saved to:", json_output)
print("Evaluation saved to:", evaluation_output)