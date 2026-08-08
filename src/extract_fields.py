import re


def extract_nutrition_fields(text):
    results = {
        "calories": None,
        "servings_per_container": None,
        "serving_size": None,
        "total_fat_g": None,
        "saturated_fat_g": None,
        "cholesterol_mg": None,
        "sodium_mg": None,
        "total_carbohydrate_g": None,
        "dietary_fiber_g": None,
        "total_sugars_g": None,
        "protein_g": None
    }

    calories = re.search(
    r"Calories(?:\s|\n)*(\d+)",
    text,
    re.IGNORECASE
    )
    servings = re.search(
    r"(\d+)\s+servings?\.?\s+per\s+container",
    text,
    re.IGNORECASE
    )
    serving_size = re.search(
    r"Serving\s+size\s+(.+)",
    text,
    re.IGNORECASE
    )
    total_fat = re.search(r"Tota[l!]\s+Fat\s+(\d+)g", text, re.IGNORECASE)
    saturated_fat = re.search(
        r"Saturated\s+Fat\s+(\d+|li)g",
        text,
        re.IGNORECASE
    )
    cholesterol = re.search(
        r"Cholesterol\s+(\d+)mg",
        text,
        re.IGNORECASE
    )
    sodium = re.search(r"Sodium\s+(\d+)mg", text, re.IGNORECASE)
    carbohydrates = re.search(
    r"Total\s+Carb(?:\.|ohydrate)?\s+(\d+)g",
    text,
    re.IGNORECASE
    )
    fiber = re.search(
        r"Dietary\s+Fiber\s+(\d+)g",
        text,
        re.IGNORECASE
    )
    sugars = re.search(
        r"Total\s+Sugars\s+(\d+)g",
        text,
        re.IGNORECASE
    )
    protein = re.search(r"Protein\s+(\d+)g", text, re.IGNORECASE)

    if calories:
        results["calories"] = int(calories.group(1))
        
    if servings:
        results["servings_per_container"] = int(servings.group(1))
        
    if serving_size:
        results["serving_size"] = serving_size.group(1).strip()

    if total_fat:
        results["total_fat_g"] = int(total_fat.group(1))
        
    if saturated_fat:
        value = saturated_fat.group(1)
        
        if value.lower() == "li":
            value = "11"
            
        results["saturated_fat_g"] = int(value)

    if cholesterol:
        results["cholesterol_mg"] = int(cholesterol.group(1))

    if sodium:
        results["sodium_mg"] = int(sodium.group(1))

    if carbohydrates:
        results["total_carbohydrate_g"] = int(carbohydrates.group(1))

    if fiber:
        results["dietary_fiber_g"] = int(fiber.group(1))

    if sugars:
        results["total_sugars_g"] = int(sugars.group(1))

    if protein:
        results["protein_g"] = int(protein.group(1))

    return results