import json

from evaluate import compare_results
from extract_fields import extract_nutrition_fields
from validate import validate_results
from confidence import calculate_confidence

# Files used for this label
ocr_file = "data/outputs/label_02/label_02_threshold_140_ocr.txt"
annotation_file = "data/annotations/label_02.json"

json_output = "data/outputs/label_02/label_02_extracted.json"
evaluation_output = "data/outputs/label_02/label_02_evaluation.json"

# Read the OCR text that Tesseract created
with open(ocr_file, "r", encoding="utf-8") as file:
    ocr_text = file.read()

# Turn the text into nutrition fields
extracted_results = extract_nutrition_fields(ocr_text)

# Check for missing or unrealistic values
validation_warnings = validate_results(extracted_results)

if len(validation_warnings) == 0:
    validation_status = "passed"
else:
    validation_status = "warning"

# Simple score based on how many fields found
confidence_score = calculate_confidence(
    extracted_results,
    validation_warnings
)

# Combines the extracted data and extra info
final_results = {
    "fields": extracted_results,
    "validation_status": validation_status,
    "validation_warnings": validation_warnings,
    "confidence_score": confidence_score
}

# Save final extraction result
with open(json_output, "w", encoding="utf-8") as file:
    json.dump(final_results, file, indent=2)

# Load the manually entered correct values
with open(annotation_file, "r", encoding="utf-8") as file:
    expected_results = json.load(file)

# Compare extraction against correct answer
evaluation = compare_results(expected_results, extracted_results)

# Save report
with open(evaluation_output, "w", encoding="utf-8") as file:
    json.dump(evaluation, file, indent=2)

# Print stuff
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

print("\nConfidence score:")
print(round(confidence_score * 100, 2), "%")

print("\nValidation status:")
print(validation_status)