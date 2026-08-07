def calculate_confidence(results, warnings):
    total_fields = len(results)

    if total_fields == 0:
        return 0

    found_fields = 0

    for value in results.values():
        if value is not None:
            found_fields += 1

    score = found_fields / total_fields

    # Lower the score a little for each warning
    score = score - (0.05 * len(warnings))

    if score < 0:
        score = 0

    return score