from matcher.fuzzy_match import normalize

def test_norm():
    normalized, score, matched = normalize("doliprane")

    assert normalized == "doliprane"
    assert score == 100.0
    assert matched is True
