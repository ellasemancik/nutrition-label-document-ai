def validate_results(results):
    warnings = []

    for field, value in results.items():
        if value is None:
            warnings.append(f"{field} was not found")

        elif value < 0:
            warnings.append(f"{field} cannot be negative")

    if results["calories"] is not None and results["calories"] > 2000:
        warnings.append("calories looks unusually high")

    if results["sodium_mg"] is not None and results["sodium_mg"] > 5000:
        warnings.append("sodium looks unusually high")

    return warnings