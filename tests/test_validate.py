from src.validate import validate_results


def test_missing_value_creates_warning():
    results = {
        "calories": None,
        "sodium_mg": 115
    }

    warnings = validate_results(results)

    assert "calories was not found" in warnings


def test_saturated_fat_cannot_be_greater_than_total_fat():
    results = {
        "calories": 300,
        "sodium_mg": 100,
        "total_fat_g": 10,
        "saturated_fat_g": 15,
        "total_carbohydrate_g": 30,
        "dietary_fiber_g": 3,
        "total_sugars_g": 20
    }

    warnings = validate_results(results)

    assert "saturated fat is greater than total fat" in warnings
    

def test_sugars_cannot_be_greater_than_carbohydrates():
    results = {
        "calories": 300,
        "sodium_mg": 100,
        "total_fat_g": 10,
        "saturated_fat_g": 5,
        "total_carbohydrate_g": 20,
        "dietary_fiber_g": 3,
        "total_sugars_g": 30
    }

    warnings = validate_results(results)

    assert "total sugars is greater than total carbohydrate" in warnings