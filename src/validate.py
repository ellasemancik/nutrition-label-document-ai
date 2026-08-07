def validate_results(results):
    warnings = []

    for field, value in results.items():
        if value is None:
            warnings.append(f"{field} was not found")

        elif isinstance(value, (int, float)) and value < 0:
            warnings.append(f"{field} cannot be negative")

    calories = results.get("calories")
    sodium = results.get("sodium_mg")

    if calories is not None and calories > 2000:
        warnings.append("calories looks unusually high")

    if sodium is not None and sodium > 5000:
        warnings.append("sodium looks unusually high")

    # Cross-field checks
    total_fat = results.get("total_fat_g")
    saturated_fat = results.get("saturated_fat_g")

    if total_fat is not None and saturated_fat is not None:
        if saturated_fat > total_fat:
            warnings.append("saturated fat is greater than total fat")

    carbohydrates = results.get("total_carbohydrate_g")
    fiber = results.get("dietary_fiber_g")
    sugars = results.get("total_sugars_g")

    if carbohydrates is not None and fiber is not None:
        if fiber > carbohydrates:
            warnings.append("dietary fiber is greater than total carbohydrate")

    if carbohydrates is not None and sugars is not None:
        if sugars > carbohydrates:
            warnings.append("total sugars is greater than total carbohydrate")
            
    serving_size = results.get("serving_size")

    if serving_size is not None:
        if "(" in serving_size and ")" not in serving_size:
            warnings.append("serving size looks incomplete")

    return warnings