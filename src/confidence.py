def calculate_confidence(results):
    total_fields = len(results)
    found_fields = 0

    for value in results.values():
        if value is not None:
            found_fields += 1

    if total_fields == 0:
        return 0

    return found_fields / total_fields