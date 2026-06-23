import pandas as pd

from api.bdpm_client import search_medicine
from matcher.fuzzy_match import normalize


def analyze_lines(lines, threshold=80):

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

    rows = []

    for result in results:

        bdpm = result["resultat_bdpm"]

        # Transformer la réponse API en texte lisible
        if isinstance(bdpm, list) and len(bdpm) > 0:
            first = bdpm[0]

            bdpm_text = (
                f"{first.get('DENOMINATION', '')} "
                f"(CIS: {first.get('CIS', '')}) - "
                f"{first.get('TITULAIRES', '')}"
            )

        elif isinstance(bdpm, dict):
            bdpm_text = str(bdpm)

        else:
            bdpm_text = result["erreur"] or ""

        rows.append(
            {
                "Ligne OCR": result["ligne_ocr"],
                "Médicament détecté": result["medicament"],
                "Score (%)": result["score_matching"],
                "Reconnu": "Oui" if result["matched"] else "Non",
                "Résultat BDPM": bdpm_text,
            }
        )

    return pd.DataFrame(rows)