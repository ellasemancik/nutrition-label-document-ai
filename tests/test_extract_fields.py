from src.extract_fields import extract_nutrition_fields


def test_extract_nutrition_fields():
    sample_text = """
    Total Fat 18g 23%
    Sodium 115mg 5%
    Total Carb. 43g 16%
    Protein 6g
    """

    result = extract_nutrition_fields(sample_text)

    assert result["total_fat_g"] == 18
    assert result["sodium_mg"] == 115
    assert result["total_carbohydrate_g"] == 43
    assert result["protein_g"] == 6