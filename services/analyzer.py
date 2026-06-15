import pandas as pd

from api.bdpm_client import search_medicine
from matcher.fuzzy_match import normalize


def analyze_lines(lines, threshold=80):
    """
    Analyse une liste de lignes de texte (OCR ou saisie manuelle).

    Pour chaque ligne non vide :
    - normalise le texte et tente de le faire correspondre à un nom de
      médicament de référence (fuzzy matching) ;
    - si une correspondance suffisamment fiable est trouvée, interroge
      l'API BDPM pour récupérer les informations associées.

    Args:
        lines: liste de chaînes de texte (une par ligne d'ordonnance).
        threshold: seuil de confiance transmis à `normalize()`.

    Returns:
        Une liste de dicts, un par ligne non vide, avec les clés :
        "ligne_ocr", "medicament", "score_matching", "matched",
        "resultat_bdpm", "erreur".
    """
    results = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        matched_name, score, matched = normalize(line, threshold=threshold)

        entry = {
            "ligne_ocr": line,
            "medicament": matched_name,
            "score_matching": score,
            "matched": matched,
            "resultat_bdpm": None,
            "erreur": None,
        }

        if matched:
            bdpm_result = search_medicine(matched_name)
            if isinstance(bdpm_result, dict) and "error" in bdpm_result:
                entry["erreur"] = bdpm_result["error"]
            else:
                entry["resultat_bdpm"] = bdpm_result

        results.append(entry)

    return results


def to_dataframe(results):
    """
    Convertit une liste de résultats d'analyse (issus de `analyze_lines`)
    en DataFrame pandas, prête à être affichée ou exportée en CSV.

    NOTE: la colonne "Résultat BDPM" contient le JSON brut renvoyé par
    l'API (ou le message d'erreur). Une fois le schéma exact de l'API BDPM
    confirmé, il est préférable d'extraire ici des colonnes dédiées
    (ex. dénomination, dosage, code CIS, etc.) plutôt que le JSON brut.
    """
    rows = []

    for result in results:
        rows.append(
            {
                "Ligne OCR": result["ligne_ocr"],
                "Médicament détecté": result["medicament"],
                "Score (%)": result["score_matching"],
                "Reconnu": "Oui" if result["matched"] else "Non",
                "Résultat BDPM": result["resultat_bdpm"]
                if result["resultat_bdpm"] is not None
                else result["erreur"] or "",
            }
        )

    return pd.DataFrame(rows)