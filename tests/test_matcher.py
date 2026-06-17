from matcher.fuzzy_match import normalize

def test_norm():
    assert normalize("doliprane")=="doliprane"
