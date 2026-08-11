import json

from evaluate import compare_results
from extract_fields import extract_nutrition_fields


labels = {
    "label_02": {
        "ocr": "data/outputs/label_02/label_02_threshold_140_ocr.txt",
        "annotation": "data/annotations/label_02.json"
    },
    "label_03": {
        "ocr": "data/outputs/label_03/label_03_psm_11_ocr.txt",
        "annotation": "data/annotations/label_03.json"
    },
    "label_04": {
        "ocr": "data/outputs/label_04/label_04_ocr.txt",
        "annotation": "data/annotations/label_04.json"
    }
}


benchmark_results = {}
total_accuracy = 0


for label_name, files in labels.items():

    with open(files["ocr"], "r", encoding="utf-8") as file:
        ocr_text = file.read()

    with open(files["annotation"], "r", encoding="utf-8") as file:
        expected_results = json.load(file)

    extracted_results = extract_nutrition_fields(ocr_text)

    evaluation = compare_results(
        expected_results,
        extracted_results
    )

    accuracy = evaluation["accuracy"] * 100
    total_accuracy += accuracy

    benchmark_results[label_name] = {
        "correct_fields": evaluation["correct_fields"],
        "total_fields": evaluation["total_fields"],
        "accuracy": round(accuracy, 2)
    }

    print("\n", label_name)
    print("Correct:", evaluation["correct_fields"])
    print("Total:", evaluation["total_fields"])
    print("Accuracy:", round(accuracy, 2), "%")


average_accuracy = total_accuracy / len(labels)

benchmark_results["average_accuracy"] = round(
    average_accuracy,
    2
)


output_file = "data/outputs/multi_label_benchmark.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(benchmark_results, file, indent=2)


print("\nAverage accuracy:")
print(round(average_accuracy, 2), "%")

print("\nBenchmark saved to:", output_file)