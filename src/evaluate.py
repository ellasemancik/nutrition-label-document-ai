def compare_results(expected, actual):
    correct = 0
    total = 0
    differences = {}

    for field, expected_value in expected.items():
        if field == "image":
            continue

        total += 1
        actual_value = actual.get(field)

        if actual_value == expected_value:
            correct += 1
        else:
            differences[field] = {
                "expected": expected_value,
                "actual": actual_value
            }

    accuracy = correct / total if total > 0 else 0

    return {
        "correct_fields": correct,
        "total_fields": total,
        "accuracy": accuracy,
        "differences": differences
    }