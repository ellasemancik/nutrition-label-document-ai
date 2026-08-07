from src.evaluate import compare_results


def test_compare_results():
    expected = {
        "calories": 350,
        "sodium_mg": 115
    }

    actual = {
        "calories": None,
        "sodium_mg": 115
    }

    result = compare_results(expected, actual)

    assert result["correct_fields"] == 1
    assert result["total_fields"] == 2
    assert result["accuracy"] == 0.5