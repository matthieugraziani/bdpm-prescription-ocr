from unittest.mock import patch

from services.analyzer import analyze_lines, to_dataframe


@patch("services.analyzer.search_medicine")
def test_analyze_lines_matched_calls_bdpm(mock_search):
    mock_search.return_value = {"results": ["DOLIPRANE 1000mg"]}

    results = analyze_lines(["doliprane 1000mg matin"])

    assert len(results) == 1
    assert results[0]["matched"] is True
    assert results[0]["medicament"] == "doliprane"
    assert results[0]["resultat_bdpm"] == {"results": ["DOLIPRANE 1000mg"]}
    mock_search.assert_called_once()


@patch("services.analyzer.search_medicine")
def test_analyze_lines_unmatched_does_not_call_bdpm(mock_search):
    results = analyze_lines(["bonjour comment allez vous"])

    assert len(results) == 1
    assert results[0]["matched"] is False
    assert results[0]["resultat_bdpm"] is None
    mock_search.assert_not_called()


def test_analyze_lines_skips_empty_lines():
    results = analyze_lines(["", "   ", "doliprane"])

    assert len(results) == 1


@patch("services.analyzer.search_medicine")
def test_analyze_lines_records_bdpm_error(mock_search):
    mock_search.return_value = {"error": "API indisponible"}

    results = analyze_lines(["doliprane"])

    assert results[0]["erreur"] == "API indisponible"
    assert results[0]["resultat_bdpm"] is None


@patch("services.analyzer.search_medicine")
def test_to_dataframe_columns(mock_search):
    mock_search.return_value = {"results": []}

    df = to_dataframe(analyze_lines(["doliprane"]))

    expected_columns = {
        "Ligne OCR",
        "Médicament détecté",
        "Score (%)",
        "Reconnu",
        "Résultat BDPM",
    }
    assert expected_columns.issubset(set(df.columns))
    assert len(df) == 1