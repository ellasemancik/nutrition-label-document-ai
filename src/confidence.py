def calculate_confidence(results, warnings):
    total_fields = len(results)

    if total_fields == 0:
        return 0

    found_fields = 0

    for value in results.values():
        if value is not None:
            found_fields += 1

    score = found_fields / total_fields

    # Missing fields are already reflected in the coverage score,
    # so only apply a smaller penalty for extra validation problems.
    extra_warnings = 0

    for warning in warnings:
        if "was not found" not in warning:
            extra_warnings += 1

    score = score - (0.05 * extra_warnings)

    if score < 0:
        score = 0

    if score > 1:
        score = 1

    return score