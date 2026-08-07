from src.extract_fields import extract_nutrition_fields


def test_extract_nutrition_fields():
    sample_text = """
    Calories 350
    3 servings per container
    Serving size 2/3 cup (140g)
    Total Fat 18g 23%
    Saturated Fat 11g 55%
    Cholesterol 50mg 17%
    Sodium 115mg 5%
    Total Carb. 43g 16%
    Dietary Fiber 3g 11%
    Total Sugars 37g
    Protein 6g
    """

    result = extract_nutrition_fields(sample_text)

    assert result["calories"] == 350
    assert result["servings_per_container"] == 3
    assert result["serving_size"] == "2/3 cup (140g)"
    assert result["total_fat_g"] == 18
    assert result["saturated_fat_g"] == 11
    assert result["cholesterol_mg"] == 50
    assert result["sodium_mg"] == 115
    assert result["total_carbohydrate_g"] == 43
    assert result["dietary_fiber_g"] == 3
    assert result["total_sugars_g"] == 37
    assert result["protein_g"] == 6


def test_missing_field_returns_none():
    sample_text = """
    Sodium 115mg 5%
    Protein 6g
    """

    result = extract_nutrition_fields(sample_text)

    assert result["total_fat_g"] is None
    assert result["sodium_mg"] == 115