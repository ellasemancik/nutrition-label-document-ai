import json

from confidence import calculate_confidence
from evaluate import compare_results
from extract_fields import extract_nutrition_fields
from ocr_reader import read_text
from preprocess import make_thresholded
from validate import validate_results


labels = {
    "label_02": {
        "image": "data/raw/label_02/label_02_per_serving_only.png",
        "annotation": "data/annotations/label_02.json",
        "mode": "threshold"
    },
    "label_03": {
        "image": "data/raw/label_03/label_03.png",
        "annotation": "data/annotations/label_03.json",
        "mode": "psm11"
    },
    "label_04": {
        "image": "data/raw/label_04/label_04.png",
        "annotation": "data/annotations/label_04.json",
        "mode": "normal"
    },
    "label_05": {
        "image": "data/raw/label_05/label_05.png",
        "annotation": "data/annotations/label_05.json",
        "mode": "normal"
    },
    "label_06": {
        "image": "data/raw/label_06/label_06.png",
        "annotation": "data/annotations/label_06.json",
        "mode": "normal"
    }
}


benchmark_results = {}

total_accuracy = 0
total_confidence = 0
total_confidence_error = 0


for label_name, files in labels.items():

    # Run the OCR setup chosen for this label
    if files["mode"] == "threshold":
        threshold_image = (
            f"data/outputs/{label_name}/"
            f"{label_name}_benchmark_threshold.png"
        )

        make_thresholded(
            files["image"],
            threshold_image,
            140
        )

        ocr_text = read_text(threshold_image)

    elif files["mode"] == "psm11":
        ocr_text = read_text(
            files["image"],
            config="--psm 11"
        )

    else:
        ocr_text = read_text(files["image"])


    # Extract and check the fields
    extracted_results = extract_nutrition_fields(ocr_text)

    warnings = validate_results(extracted_results)

    confidence = calculate_confidence(
        extracted_results,
        warnings
    )


    # Load the manually entered correct values
    with open(files["annotation"], "r", encoding="utf-8") as file:
        expected_results = json.load(file)


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
    total_confidence += confidence_percent
    total_confidence_error += confidence_error


    benchmark_results[label_name] = {
        "correct_fields": evaluation["correct_fields"],
        "total_fields": evaluation["total_fields"],
        "accuracy": round(accuracy, 2),
        "confidence": round(confidence_percent, 2),
        "confidence_error": round(confidence_error, 2)
    }


    print("\n", label_name)
    print("Accuracy:", round(accuracy, 2), "%")
    print("Confidence:", round(confidence_percent, 2), "%")


average_accuracy = total_accuracy / len(labels)
average_confidence = total_confidence / len(labels)

average_confidence_error = (
    total_confidence_error / len(labels)
)


benchmark_results["average_accuracy"] = round(
    average_accuracy,
    2
)

benchmark_results["average_confidence"] = round(
    average_confidence,
    2
)

benchmark_results["average_confidence_error"] = round(
    average_confidence_error,
    2
)

output_file = "data/outputs/end_to_end_benchmark.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(benchmark_results, file, indent=2)


print("\nAverage accuracy:")
print(round(average_accuracy, 2), "%")

print("\nAverage confidence:")
print(round(average_confidence, 2), "%")

print("\nAverage confidence error:")
print(round(average_confidence_error, 2), "%")

print("\nBenchmark saved to:", output_file)