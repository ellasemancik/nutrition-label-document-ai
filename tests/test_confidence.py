from src.confidence import calculate_confidence


def test_confidence_score():
    results = {
        "calories": None,
        "sodium_mg": 115,
        "protein_g": 6,
        "total_fat_g": 18
    }

    confidence = calculate_confidence(results)

    assert confidence == 0.75