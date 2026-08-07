import re


def extract_nutrition_fields(text):
    results = {}

    total_fat = re.search(r"Tota[l!]\s+Fat\s+(\d+)g", text, re.IGNORECASE)
    sodium = re.search(r"Sodium\s+(\d+)mg", text, re.IGNORECASE)
    carbohydrates = re.search(r"Total Carb\.\s+(\d+)g", text, re.IGNORECASE)
    protein = re.search(r"Protein\s+(\d+)g", text, re.IGNORECASE)

    if total_fat:
        results["total_fat_g"] = int(total_fat.group(1))

    if sodium:
        results["sodium_mg"] = int(sodium.group(1))

    if carbohydrates:
        results["total_carbohydrate_g"] = int(carbohydrates.group(1))

    if protein:
        results["protein_g"] = int(protein.group(1))

    return results