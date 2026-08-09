import json

from evaluate import compare_results
from extract_fields import extract_nutrition_fields


annotation_file = "data/annotations/label_03.json"

ocr_files = {
    100: "data/outputs/label_03/label_03_threshold_100_ocr.txt",
    140: "data/outputs/label_03/label_03_threshold_140_ocr.txt",
    180: "data/outputs/label_03/label_03_threshold_180_ocr.txt"
}

benchmark_results = {}


with open(annotation_file, "r", encoding="utf-8") as file:
    expected_results = json.load(file)


for threshold, ocr_file in ocr_files.items():

    with open(ocr_file, "r", encoding="utf-8") as file:
        ocr_text = file.read()

    extracted_results = extract_nutrition_fields(ocr_text)

    evaluation = compare_results(
        expected_results,
        extracted_results
    )

    accuracy = evaluation["accuracy"] * 100

    benchmark_results[str(threshold)] = round(accuracy, 2)

    print("\nThreshold:", threshold)
    print("Correct:", evaluation["correct_fields"])
    print("Total:", evaluation["total_fields"])
    print("Accuracy:", round(accuracy, 2), "%")


output_file = (
    "data/outputs/label_03/"
    "label_03_threshold_benchmark.json"
)

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(benchmark_results, file, indent=2)


print("\nBenchmark saved to:", output_file)