import json

from extract_fields import extract_nutrition_fields


ocr_file = "data/outputs/label_02/label_02_threshold_140_ocr.txt"
json_output = "data/outputs/label_02/label_02_extracted.json"


with open(ocr_file, "r", encoding="utf-8") as file:
    ocr_text = file.read()


results = extract_nutrition_fields(ocr_text)


with open(json_output, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2)


print("Extracted fields:")
print(results)
print("Saved to:", json_output)