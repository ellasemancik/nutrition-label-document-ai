from src.validate import validate_results


def test_missing_value_creates_warning():
    results = {
        "calories": None,
        "sodium_mg": 115
    }

    warnings = validate_results(results)

    assert "calories was not found" in warnings