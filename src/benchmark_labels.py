import json

from evaluate import compare_results
from extract_fields import extract_nutrition_fields
from confidence import calculate_confidence
from validate import validate_results


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
    },
    "label_05": {
    "ocr": "data/outputs/label_05/label_05_ocr.txt",
    "annotation": "data/annotations/label_05.json"
    },
    "label_06": {
    "ocr": "data/outputs/label_06/label_06_ocr.txt",
    "annotation": "data/annotations/label_06.json"
}
}


benchmark_results = {}
total_accuracy = 0
total_confidence_error = 0


for label_name, files in labels.items():

    with open(files["ocr"], "r", encoding="utf-8") as file:
        ocr_text = file.read()

    with open(files["annotation"], "r", encoding="utf-8") as file:
        expected_results = json.load(file)

    extracted_results = extract_nutrition_fields(ocr_text)
    
    warnings = validate_results(extracted_results)

    confidence = calculate_confidence(
        extracted_results,
        warnings
    )

    evaluation = compare_results(
        expected_results,
        extracted_results
    )

    accuracy = evaluation["accuracy"] * 100
    confidence_percent = confidence * 100
    
    confidence_error = abs(
        confidence_percent - accuracy
    )
    total_accuracy += accuracy
    total_confidence_error += confidence_error

    benchmark_results[label_name] = {
        "correct_fields": evaluation["correct_fields"],
        "total_fields": evaluation["total_fields"],
        "accuracy": round(accuracy, 2),
        "confidence": round(confidence_percent, 2),
        "confidence_error": round(confidence_error, 2)
    }

    print("\n", label_name)
    print("Correct:", evaluation["correct_fields"])
    print("Total:", evaluation["total_fields"])
    print("Accuracy:", round(accuracy, 2), "%")
    print("Confidence:", round(confidence_percent, 2), "%")
    print("Confidence error:", round(confidence_error, 2), "%")


average_accuracy = total_accuracy / len(labels)
average_confidence_error = total_confidence_error / len(labels)

benchmark_results["average_accuracy"] = round(
    average_accuracy,
    2
)

benchmark_results["average_confidence_error"] = round(
    average_confidence_error,
    2
)


output_file = "data/outputs/multi_label_benchmark.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(benchmark_results, file, indent=2)


print("\nAverage accuracy:")
print(round(average_accuracy, 2), "%")

print("\nAverage confidence error:")
print(round(average_confidence_error, 2), "%")

print("\nBenchmark saved to:", output_file)
